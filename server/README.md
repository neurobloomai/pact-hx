# PACT API Server

Simple FastAPI server for PACT memory system.

## Quick Start (Local Testing)

### 1. Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 2. Run Server

```bash
# From server directory
uvicorn src.main:app --reload

# Server runs at: http://localhost:8000
```

### 3. Test It

**Option A: Browser**
- Health: http://localhost:8000/health
- Docs: http://localhost:8000/docs (interactive API docs!)

**Option B: Manual Test Script**
```bash
# In another terminal
python manual_test.py
```

**Option C: Pytest**
```bash
cd tests
pytest test_api.py -v
```

**Option D: curl**
```bash
# Health check
curl http://localhost:8000/health

# Create session
curl -X POST http://localhost:8000/sessions

# Get context (use session_id from above)
curl http://localhost:8000/sessions/{session_id}/context
```

---

## API Endpoints

### `GET /health`
Health check

**Response:**
```json
{"status": "ok"}
```

### `POST /sessions`
Create new session

**Response:**
```json
{"session_id": "uuid-here"}
```

### `GET /sessions/{session_id}/context`
Get conversation context

**Response:**
```json
{
  "messages": [],
  "emotional_state": "neutral"
}
```

### `POST /sessions/{session_id}/interactions`
Save interaction

**Parameters:**
- `user_message`: string
- `ai_message`: string

**Response:**
```json
{"interaction_id": "saved"}
```

---

## Database

Currently using **SQLite** (`pact.db` file).

**Location:** `server/pact.db` (created automatically)

**Schema:**
```sql
sessions (
  id TEXT PRIMARY KEY,
  messages TEXT  -- JSON string
)
```

---

## Testing with pact-langchain Package

Once server is running locally:

```python
from pact_langchain import PACTMemory

# Point to local server
memory = PACTMemory(
    api_key="test",
    api_url="http://localhost:8000"  # Local server!
)

# Test it
memory.save_context(
    {"input": "Hello"},
    {"output": "Hi there!"}
)

context = memory.load_memory_variables({})
print(context)
```

---

## Deployment

**For now:** Testing locally only! ✅

**Later:** 
- Railway.app (when it works)
- AWS EC2
- Render.com
- Or anywhere else

**Current status:** No deployment needed yet. Just test locally!

---

## File Structure

```
server/
├── src/
│   ├── main.py          # FastAPI app
│   ├── database.py      # DB setup
│   └── models.py        # SQLAlchemy models
├── tests/
│   └── test_api.py      # Pytest tests
├── manual_test.py       # Manual test script
├── requirements.txt     # Dependencies
├── pact.db             # SQLite database (auto-created)
└── README.md           # This file
```

---

## Next Steps

1. ✅ Test locally (you are here!)
2. ⏳ Add more endpoints
3. ⏳ Add emotional analysis
4. ⏳ Add context consolidation
5. ⏳ Deploy when ready

---

## Troubleshooting

**Server won't start?**
```bash
# Make sure you're in server directory
cd server

# Install dependencies
pip install -r requirements.txt

# Try running directly
python -m uvicorn src.main:app --reload
```

**Import errors?**
```bash
# Make sure __init__.py exists in src/
touch src/__init__.py
```

**Port already in use?**
```bash
# Use different port
uvicorn src.main:app --reload --port 8001
```

---

**Built with 🧠 by NeurobloomAI**

Testing locally first = avoiding stupidity = muddhu! 😊
