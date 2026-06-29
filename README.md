# pact-hx

> Human experience primitives for AI agents. Memory, attention, tone, and values — per person, across sessions.

---

The agent answered correctly.

Right format. Right facts. Within the guardrails.

And the human felt like they were talking to a very fast search engine.

No memory of last week's context. No awareness that this person communicates in lists, not paragraphs. No record of the value conflict that surfaced three sessions ago and was never fully resolved. No recognition that this question is the continuation of something that started six weeks ago.

Technically functional. Relationally empty.

pact-hx is the layer that changes that.

---

## The four primitives — and why those four

An agent that knows a human well enough to have a real relationship with them needs to hold four distinct things:

**What happened — `Memory`**
Not a transcript. Episodic events, semantic understanding, and identity-level patterns that persist across sessions. The difference between knowing someone said something and knowing what kind of person says things like that.

**What matters right now — `Attention`**
Context is not flat. Some entities and topics are salient in this session; others are background signal. `AttentionManager` tracks salience weights in real time so the agent knows what to weight, not just what to retrieve.

**How they communicate — `ToneAdaptation`**
Communication style is a relational contract. When someone tells you they prefer directness, that preference should survive the end of the session. `ToneAdaptationManager` accumulates style signals over time and shapes every subsequent response accordingly.

**What they stand for — `ValueAlignment`**
Value conflicts between agent behavior and human values don't announce themselves. They accumulate quietly until something breaks trust. `ValueAlignmentManager` detects conflicts before they surface and routes them to resolution — not as a policy check, but as a relational signal.

These four cover the full relational surface between a human and an agent: history, current salience, communication contract, ethical coherence.

---

## Quickstart

```python
from pact_hx.primitives.memory.manager import MemoryManager
from pact_hx.primitives.attention.manager import AttentionManager
from pact_hx.primitives.tone_adapt.manager import ToneAdaptationManager
from pact_hx.primitives.value_align.manager import ValueAlignmentManager

user_id = "alice"

# What happened
mem = MemoryManager(user_id)
mem.store_memory("Alice prefers concise answers", memory_type="semantic")
mem.store_memory("Working on Q3 roadmap — deadline pressure high", memory_type="episodic")

# What matters right now
attn = AttentionManager(user_id)
attn.update_attention(
    entities=["q3_roadmap", "budget_constraints"],
    context="User is reviewing resource allocation for Q3"
)
top = attn.get_top_entities(limit=3)

# How they communicate
tone = ToneAdaptationManager(user_id)
guidance = tone.generate_style_guidance("Here is your project summary...")
tone.provide_feedback("too_formal", {"preferred": "direct"})

# What they stand for
values = ValueAlignmentManager(user_id)
assessment = values.assess_value_alignment(
    proposed_action="share resource allocation data with external vendor",
    context="Q3 planning"
)
if assessment.requires_attention:
    # surface the conflict — don't suppress it
    print(assessment.conflicts_detected)
```

---

## Architecture

```
pact_hx/primitives/
├── memory/             episodic + semantic + identity memory, importance scoring
├── attention/          salience-weighted entity tracking per session
├── tone_adapt/         communication style adaptation with feedback loop
├── value_align/        value conflict detection and resolution
│   ├── manager.py      ValueAlignmentManager — primary interface
│   ├── conflict.py     ConflictDetector — detection and resolution strategies
│   └── schemas.py      ValueDomain, ConflictSeverity, ConflictResolution
├── context/            shared context state across agent turns
└── goal/               goal tracking across sessions
```

Each primitive is independent. Use one or all four — they share no required coupling.

---

## pact-hx and pact-hh — not the same thing

These two repos solve adjacent but distinct problems.

**pact-hx** answers: *how should the interaction with this human feel?*
Tone, memory, value alignment, attention. The relational texture of every message the agent sends.

**pact-hh** answers: *when should a human enter the protocol, and how does their decision get back in?*
Escalation routing, decision injection, loop closure.

```
pact-hh produces:   EscalationPacket (raw structured data — what needs a decision)
        ↓
pact-hx renders:    "Hey — billing-agent and compliance-agent hit a wall on this
                     refund. Here's what I'd suggest, given what I know about
                     how you've handled these before..."
        ↓
pact-hh delivers:   via the human's preferred channel
        ↓
pact-hh receives:   human's reply
        ↓
pact-hx interprets: tone, certainty signals, implicit intent
        ↓
pact-hh re-injects: structured HumanDecision into CoordinationBus
```

Without pact-hx, escalations land as system alerts. With it, they read like a colleague asking for a second opinion — with context the agent actually has about this specific person.

---

## Where pact-hx sits in the stack

```
pact          Intent translation across platforms
pact-ax       Agent ↔ agent coordination and trust
pact-bridge   Orchestration — connects pact + pact-ax as a live system
pact-hh       Human escalation loop — catches signals, routes, re-injects decisions
pact-hx       Human ↔ agent experience — memory, tone, attention, values   ◀ this repo
pact-sx       Participant ↔ system relationships — persistent, portable standing
```

pact-hx is the layer closest to the human. It does not route, coordinate, or orchestrate. It holds what the agent needs to know about this person in order to treat them as a person.

---

## Related repos

| Repo | Role |
|---|---|
| [pact](https://github.com/neurobloomai/pact) | Intent translation protocol |
| [pact-ax](https://github.com/neurobloomai/pact-ax) | Agent collaboration primitives |
| [pact-bridge](https://github.com/neurobloomai/pact-bridge) | Connects pact + pact-ax |
| [pact-hh](https://github.com/neurobloomai/pact-hh) | Human escalation loop |
| [pact-sx](https://github.com/neurobloomai/pact-sx) | Participant-system relationships |

---

MIT License · [neurobloom.ai](https://neurobloom.ai)
