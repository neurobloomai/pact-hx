# Scripts

Two standalone market tools. No database, no server — just Python and a browser.

---

## Installation

```bash
pip install yfinance
```

Python 3.8+ supported.

---

## Market Selective Briefing — `dashboard.py`

Tracks 12 theme-based ETFs across multiple moving average timeframes and produces a signal for each: **ALIGNED**, **PULLBACK**, or **AVOID**.

**Themes covered:** Software · Cloud · Semis · Cyber · Grid · Nuclear · SMR · Mining · Small Cap · Mid Cap

**What each column means:**

| Column | Meaning |
|---|---|
| Day% | Price change vs previous close |
| Vol/Avg | Today's volume vs 20-day average (T=today, P=prev session) |
| 5D | 5-day price trend direction |
| vs20D | % distance from 20-day moving average |
| 50D / 20W / 10M / 20M | Above (▲) or below (▼) each moving average |
| Mom | Momentum score — how many of the 4 MAs are bullish (0–4) |
| Signal | ALIGNED = all timeframes bullish · PULLBACK = long-term up, short-term dip · AVOID = below long-term MAs |

**Run:**

```bash
python dashboard.py              # uses 15-min cache
python dashboard.py --refresh    # forces fresh data
```

Opens a formatted HTML report in your browser and prints to terminal.

---

## Quality Growth Screener — `screener.py`

Screens a curated universe of quality growth names against five fundamental filters and grades each company A+, A, or B. A separate watchlist tracks high-quality names not yet qualifying, showing exactly which filter is blocking them.

**Filters applied:**

| Filter | Threshold |
|---|---|
| Debt / Enterprise Value | ≤ 0.15 |
| Operating Margin | ≥ 10% |
| Net Margin | ≥ 5% |
| ROE (or ROA fallback) | ≥ 10% ROE or ≥ 15% ROA |
| FCF Yield | > 0% |
| Trailing P/E | ≤ 100x |

**Grading is sector-aware:**
- Financials/insurers: gross margin replaced with FCF yield and adjusted operating margin thresholds
- Consulting/services: gross margin threshold lowered to 30%

**Watchlist:** High-quality names not yet qualifying are tracked separately — each showing exactly which filter is blocking them and by how much.

**Run:**

```bash
python screener.py
```

Opens an interactive HTML report in your browser showing qualified companies and the watchlist.

---

## Data & Disclaimer

Data sourced from **Yahoo Finance** via [yfinance](https://github.com/ranaroussi/yfinance). Prices and fundamentals may be delayed or incomplete.

**For informational purposes only. Not financial advice. Always do your own research before making investment decisions.**
