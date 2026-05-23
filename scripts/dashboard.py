"""
Morning Market Briefing — CLI Dashboard
Usage: python dashboard.py
"""

import yfinance as yf
import numpy as np
import pandas as pd
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings, zoneinfo, json, os, time
warnings.filterwarnings('ignore')

CACHE_FILE = os.path.expanduser('~/.dashboard_cache.json')
CACHE_TTL  = 900  # 15 minutes

WATCHLIST = ['IGV','WCLD','SMH','CIBR','GRID','NLR','SMR','OKLO','B','IWM','IWR','TOPT']

THEMES = {
    'IGV':'Software', 'WCLD':'Cloud',   'SMH':'Semis',      'CIBR':'Cyber',
    'GRID':'Grid',    'NLR':'NuclearETF','SMR':'SMR',        'OKLO':'OKLO',
    'B':'Mining',     'IWM':'SmallCap', 'IWR':'MidCap',
    'TOPT':'Top20ETF',
}

GROUPS = [
    ('TECH  ★',  ['IGV','WCLD','SMH','CIBR']),
    ('ENERGY',   ['GRID','NLR','SMR','OKLO']),
    ('MARKET',   ['IWM','IWR']),
    ('COMMODIT', ['B']),
    ('BENCHMARK',['TOPT']),
]

# ANSI colors
G  = '\033[92m'   # green
R  = '\033[91m'   # red
Y  = '\033[93m'   # yellow
GR = '\033[90m'   # grey
B  = '\033[94m'   # blue
RS = '\033[0m'    # reset

def after_close():
    et = datetime.now(zoneinfo.ZoneInfo('America/New_York'))
    return et.hour >= 16

def load_cache():
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE) as f:
                c = json.load(f)
            if time.time() - c.get('_ts', 0) < CACHE_TTL:
                return c
    except:
        pass
    return {}

def save_cache(data):
    try:
        data['_ts'] = time.time()
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
    except:
        pass

def fetch(ticker, period, interval):
    return yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)

def above_ma(ticker, interval, period, ma):
    try:
        df = fetch(ticker, period, interval)
        if len(df) < ma + 1: return None
        return float(df['Close'].iloc[-1]) > float(df['Close'].rolling(ma).mean().iloc[-1])
    except:
        return None

def get_data(ticker):
    try:
        df = fetch(ticker, '3mo', '1d')
        if df is None or len(df) < 6:
            return None

        price   = float(df['Close'].iloc[-1])
        prev    = float(df['Close'].iloc[-2])
        day_chg = (price - prev) / prev * 100

        avg_vol = float(df['Volume'].iloc[-21:-1].mean())
        vol_idx = -1 if after_close() else -2
        vol_lbl = 'T' if after_close() else 'P'
        vol_rat = float(df['Volume'].iloc[vol_idx]) / avg_vol if avg_vol > 0 else 0

        chg5    = (price - float(df['Close'].iloc[-6])) / float(df['Close'].iloc[-6]) * 100
        trend   = '↑' if chg5 > 0.5 else ('↓' if chg5 < -0.5 else '→')

        ma50    = float(df['Close'].rolling(50).mean().iloc[-1])
        ma20    = float(df['Close'].rolling(20).mean().iloc[-1])
        ma_dist = (price - ma20) / ma20 * 100

        d_above = price > ma50
        w_above  = above_ma(ticker, '1wk', '2y', 20)
        m10_above = above_ma(ticker, '1mo', '5y', 10)
        m20_above = above_ma(ticker, '1mo', '5y', 20)

        return dict(
            ticker=ticker, theme=THEMES[ticker], price=price,
            day_chg=day_chg, vol_rat=vol_rat, vol_lbl=vol_lbl,
            trend=trend, ma_dist=ma_dist,
            d=d_above, w=w_above, m10=m10_above, m20=m20_above
        )
    except Exception as e:
        print(f"  {ticker} error: {e}")
        return None

def fmt_chg(v):
    c = G if v > 0 else R
    return f"{c}{v:+.2f}%{RS}"

def fmt_vol(v, lbl):
    c = Y if v > 1.5 else (GR if v < 0.5 else '')
    return f"{c}{v:.2f}x({lbl}){RS}"

def fmt_ma(v):
    c = G if v > 0 else R
    return f"{c}{v:+.1f}%{RS}"

def fmt_tf(above):
    if above is None: return f"{GR}?{RS}"
    return f"{G}▲{RS}" if above else f"{R}▼{RS}"

def momentum_score(d):
    return sum(1 for x in [d['d'], d['w'], d['m10'], d['m20']] if x)

def fmt_score(s):
    c = G if s == 4 else (G if s == 3 else (Y if s == 2 else R))
    return f"{c}[{s}/4]{RS}"

def signal(d):
    above = momentum_score(d)
    if above == 4:                                         return f"{G}ALIGNED{RS}"
    if d['m20'] and d['w'] and not d['d']:                 return f"{B}PULLBACK{RS}"
    if not d['m20'] and not d['w']:                        return f"{R}AVOID{RS}"
    if d['day_chg'] < -2.0 and d['vol_rat'] > 1.5:        return f"{R}SELLING{RS}"
    if d['day_chg'] < -1.5 and d['vol_rat'] < 0.5:        return f"{GR}DRIFT{RS}"
    if d['ma_dist'] > 12   and d['day_chg'] > 1.5:        return f"{Y}EXTENDED{RS}"
    return ''

def signal_html(d):
    above = momentum_score(d)
    if above == 4:                                        return '<span style="color:#3fb950;font-weight:700">ALIGNED</span>'
    if d['m20'] and d['w'] and not d['d']:               return '<span style="color:#58a6ff;font-weight:700">PULLBACK</span>'
    if not d['m20'] and not d['w']:                      return '<span style="color:#f85149;font-weight:700">AVOID</span>'
    if d['day_chg'] < -2.0 and d['vol_rat'] > 1.5:      return '<span style="color:#f85149;font-weight:700">SELLING</span>'
    if d['day_chg'] < -1.5 and d['vol_rat'] < 0.5:      return '<span style="color:#8b949e;font-weight:700">DRIFT</span>'
    if d['ma_dist'] > 12   and d['day_chg'] > 1.5:      return '<span style="color:#e3b341;font-weight:700">EXTENDED</span>'
    return '—'

def score_html(s):
    c = '#3fb950' if s >= 3 else ('#e3b341' if s == 2 else '#f85149')
    return f'<span style="color:{c};font-weight:700">{s}/4</span>'

def tf_html(above):
    if above is None: return '<span style="color:#484f58">?</span>'
    return '<span style="color:#3fb950">▲</span>' if above else '<span style="color:#f85149">▼</span>'

def chg_html(v):
    c = '#3fb950' if v > 0 else '#f85149'
    return f'<span style="color:{c}">{v:+.2f}%</span>'

def vol_html(v, lbl):
    c = '#e3b341' if v > 1.5 else ('#484f58' if v < 0.5 else '#8b949e')
    return f'<span style="color:{c}">{v:.2f}x({lbl})</span>'

def ma_html(v):
    c = '#3fb950' if v > 0 else '#f85149'
    return f'<span style="color:{c}">{v:+.1f}%</span>'

def build_html(data):
    now  = datetime.now().strftime('%B %d, %Y  %H:%M')
    rows = ''
    for group, tickers in GROUPS:
        rows += f'<tr><td colspan="13" style="padding:14px 10px 4px;color:#8b949e;font-size:10px;text-transform:uppercase;letter-spacing:.08em;border-bottom:none">{group}</td></tr>'
        for t in tickers:
            d = data.get(t)
            if not d:
                rows += f'<tr><td class="ticker">{t}</td><td colspan="12" style="color:#484f58">— no data</td></tr>'
                continue
            rows += f"""<tr>
              <td class="ticker">{d['ticker']}</td>
              <td style="color:#8b949e;font-size:11px">{d['theme']}</td>
              <td>${d['price']:.2f}</td>
              <td>{chg_html(d['day_chg'])}</td>
              <td>{vol_html(d['vol_rat'], d['vol_lbl'])}</td>
              <td style="color:#e6edf3">{d['trend']}</td>
              <td>{ma_html(d['ma_dist'])}</td>
              <td>{tf_html(d['d'])}</td>
              <td>{tf_html(d['w'])}</td>
              <td>{tf_html(d['m10'])}</td>
              <td>{tf_html(d['m20'])}</td>
              <td>{score_html(momentum_score(d))}</td>
              <td>{signal_html(d)}</td>
            </tr>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Market Selective Briefing — {now}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'SF Mono','Fira Code',monospace; background: #0d1117; color: #e6edf3; padding: 28px; font-size: 12px; }}
  h1 {{ font-size: 18px; font-weight: 700; color: #58a6ff; margin-bottom: 4px; }}
  .subtitle {{ color: #8b949e; margin-bottom: 20px; font-size: 11px; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{ text-align: left; padding: 8px 10px; color: #8b949e; font-weight: 500;
        border-bottom: 2px solid #21262d; font-size: 10px; text-transform: uppercase; letter-spacing: .05em; }}
  td {{ padding: 7px 10px; border-bottom: 1px solid #161b22; }}
  tr:hover td {{ background: #161b22; }}
  .ticker {{ font-weight: 700; color: #e6edf3; }}
  .legend {{ color: #484f58; font-size: 10px; margin-top: 16px; }}
</style>
</head>
<body>
<h1>Market Selective Briefing</h1>
<div class="subtitle">{now}</div>
<table>
  <thead>
    <tr>
      <th>Ticker</th><th>Theme</th><th>Price</th><th>Day%</th><th>Vol/Avg</th>
      <th>5D</th><th>vs20D</th><th>50D</th><th>20W</th><th>10M</th><th>20M</th>
      <th>Mom</th><th>Signal</th>
    </tr>
  </thead>
  <tbody>{rows}</tbody>
</table>
<div class="legend">▲ above MA &nbsp;▼ below MA &nbsp;|&nbsp; 50D=50DayMA &nbsp;20W=20WeekMA &nbsp;10M=10MonthMA &nbsp;20M=20MonthMA &nbsp;|&nbsp; Vol: T=today P=prev session</div>
</body>
</html>"""

def print_dashboard(data):
    now = datetime.now().strftime('%b %d %Y  %H:%M')
    w   = 95
    hdr = f"  {'TICKER':<6}  {'THEME':<10}  {'PRICE':>7}  {'DAY%':>8}  {'VOL/AVG':>10}  {'5D':>2}  {'vs20D':>6}   50D  20W  10M  20M   MOM   SIGNAL"
    print()
    print(f"  {B}MARKET SELECTIVE BRIEFING  —  {now}{RS}")
    print('─' * w)
    print(hdr)

    for group, tickers in GROUPS:
        print(f"\n  {GR}{group}{RS}")
        for t in tickers:
            d = data.get(t)
            if not d:
                print(f"  {t:<6}  — no data")
                continue
            print(
                f"  {d['ticker']:<6}  "
                f"{d['theme']:<10}  "
                f"${d['price']:>7.2f}  "
                f"{fmt_chg(d['day_chg']):>8}  "
                f"{fmt_vol(d['vol_rat'], d['vol_lbl']):>10}  "
                f"{d['trend']:>2}  "
                f"{fmt_ma(d['ma_dist']):>6}   "
                f"{fmt_tf(d['d'])} {fmt_tf(d['w'])} {fmt_tf(d['m10'])} {fmt_tf(d['m20'])}   "
                f"{fmt_score(momentum_score(d))}  "
                f"{signal(d)}"
            )

    print()
    print('─' * w)
    print(f"  {GR}▲ above MA  ▼ below MA  |  50D=50DayMA  20W=20WeekMA  10M=10MonthMA  20M=20MonthMA  |  Vol: T=today P=prev session{RS}")
    print()

if __name__ == '__main__':
    import sys, webbrowser
    force = '--refresh' in sys.argv
    cache = {} if force else load_cache()
    if cache:
        age = int((time.time() - cache['_ts']) / 60)
        print(f"\n  Using cached data ({age}m old) — run with --refresh to force update")
        cache.pop('_ts', None)
        data = cache
    else:
        print("\n  Loading", end='', flush=True)
        data = {}
        with ThreadPoolExecutor(max_workers=11) as ex:
            futures = {ex.submit(get_data, t): t for t in WATCHLIST}
            for f in as_completed(futures):
                print('.', end='', flush=True)
                t = futures[f]
                data[t] = f.result()
        print()
        save_cache({k: v for k, v in data.items() if v})

    print_dashboard(data)

    path = os.path.expanduser('~/market_briefing.html')
    with open(path, 'w') as f:
        f.write(build_html(data))
    print(f"  Saved → {path}")
    webbrowser.open(f'file://{path}')
