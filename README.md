# pact-hx

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)

Human experience primitives for AI agents — persistent memory, attention tracking, tone adaptation, and value alignment per user.

```bash
pip install pact-hx
```

---

## What problem does this solve?

When an AI agent talks to a human, it loses everything between sessions. No memory of past interactions. No awareness of how this person prefers to communicate. No record of their goals or values.

PACT-HX gives agents the primitives to fix that:

1. **Memory** — episodic, semantic, and identity layers that persist across sessions
2. **Attention** — track what entities and topics matter most to this user right now
3. **Tone adaptation** — adjust communication style based on ongoing feedback
4. **Value alignment** — detect and surface value conflicts before they cause friction

---

## Quickstart

```python
from pact_hx.primitives.memory.manager import MemoryManager
from pact_hx.primitives.attention.manager import AttentionManager
from pact_hx.primitives.tone_adapt.manager import ToneAdaptationManager

# Memory — persists across sessions
mem = MemoryManager("user-alice")
mem.store_memory("Alice prefers concise answers", memory_type="semantic")
results = mem.retrieve_memories("communication preferences")

# Attention — what matters right now
attn = AttentionManager("agent-001")
attn.update_attention(
    entities=["project_deadline", "budget_constraints"],
    context="User is planning Q3 roadmap"
)
top = attn.get_top_entities(limit=3)

# Tone — adapts over time based on feedback
tone = ToneAdaptationManager("agent-001")
guidance = tone.generate_style_guidance("Here is your project summary...")
tone.provide_feedback("too_formal", {"preferred": "casual"})
```

---

## Primitives

| Primitive | What it does |
|-----------|-------------|
| **Memory** | Episodic, semantic, and identity memory layers with importance scoring |
| **Attention** | Salience-weighted entity tracking per user session |
| **Tone Adaptation** | Dynamic communication style adjustment with feedback loop |
| **Value Alignment** | Detect and resolve conflicting values across interactions |
| **Context** | Shared context state across agent turns |
| **Goal Tracking** | Monitor and update user goals over time |

---

## Start the memory server

PACT-HX includes a FastAPI memory server backed by SQLite:

```bash
cd server
pip install -r requirements.txt
uvicorn src.main:app --port 8001
```

Endpoints:

```
POST   /sessions                    — create a session
GET    /sessions/{id}/context       — retrieve session context
POST   /sessions/{id}/interactions  — record an interaction
GET    /health
```

---

## Start the integration engine

The Node.js integration engine orchestrates multiple PACT-HX components with real-time Socket.io support:

```bash
cd integration_engine
npm install
node server.js
```

Routes: `/sessions`, `/students`, `/adaptations`, `/analytics`

---

## Architecture

```
pact-hx
├── pact_hx/primitives/     — Python library
│   ├── memory/             — episodic + semantic + identity memory
│   ├── attention/          — salience-weighted entity tracking
│   ├── tone_adapt/         — communication style adaptation
│   ├── value_align/        — value conflict detection
│   ├── context/            — shared context state
│   └── goal/               — goal tracking
├── server/                 — FastAPI memory server (SQLite)
└── integration_engine/     — Node.js orchestration layer (Socket.io)
```

---

## Ecosystem

PACT-HX is the human layer of the neurobloom.ai stack:

| Layer | Repo | What it does |
|-------|------|-------------|
| Protocol | [`pact`](https://github.com/neurobloomai/pact) | How agents speak a shared language |
| Agent collaboration | [`pact-ax`](https://github.com/neurobloomai/pact-ax) | Trust, routing, handoffs between agents |
| **Human experience** | **`pact-hx`** | Memory, attention, tone per human user |

---

## License

MIT © [NeuroBloom.ai](https://neurobloom.ai)
