# 🧠 PACT-HX: Framework Integrations for PACT Memory

**Official integrations for PACT memory across popular AI frameworks.**

Built by [NeurobloomAI](https://neurobloom.ai)

---

## 📦 What's This?

This repository contains official integrations that bring PACT's emotional intelligence and context-aware memory to popular AI frameworks.

### Available Integrations

#### 🦜 LangChain
```bash
pip install pact-langchain
```

Drop-in replacement for LangChain memory with emotional tracking, context consolidation, and intelligent prioritization.

- **Status:** ✅ Ready
- **Documentation:** [packages/langchain/README.md](./packages/langchain/README.md)
- **Examples:** [packages/langchain/examples/](./packages/langchain/examples/)
- **PyPI:** `pact-langchain` (when published)

[View LangChain Integration →](./packages/langchain/)

---

### 🚧 Coming Soon

#### CrewAI Integration
Memory management for CrewAI multi-agent systems.
- **Status:** Planned Q1 2026
- **Target:** CrewAI users building collaborative agent teams

#### AutoGPT Integration  
Context management for AutoGPT autonomous agents.
- **Status:** Planned Q1 2026
- **Target:** AutoGPT developers building autonomous systems

#### OpenAI Assistants API
Enhanced memory for OpenAI's Assistants.
- **Status:** Planned Q2 2026
- **Target:** Developers using OpenAI's Assistants API

---

## 🎯 Why PACT Integrations?

### The Problem
AI frameworks have basic memory, but lack:
- Emotional awareness
- Context prioritization
- Intelligent consolidation
- Long-term relationship tracking

### The Solution
PACT provides:
- ✅ **Emotional Intelligence:** Track emotional states across conversations
- ✅ **Smart Consolidation:** Automatically summarize old context to save tokens
- ✅ **Context Prioritization:** Remember what matters most
- ✅ **Relationship Patterns:** Build long-term understanding
- ✅ **Drop-in Integration:** Minimal code changes required

---

## 🚀 Quick Start

### LangChain

```python
from pact_langchain import PACTMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI

# Just replace your memory
memory = PACTMemory(api_key="your_key")

llm = OpenAI(temperature=0.7)
conversation = ConversationChain(llm=llm, memory=memory)

# Everything else stays the same!
response = conversation.predict(input="I'm excited about this project!")

# But now you have emotional context
state = memory.get_emotional_state()
print(state["current_emotion"])  # "excited"
```

---

## 📊 Comparison

| Feature | Standard Memory | PACT Memory |
|---------|----------------|-------------|
| Drop-in replacement | ✅ | ✅ |
| Emotional tracking | ❌ | ✅ |
| Context consolidation | ❌ | ✅ |
| Priority management | ❌ | ✅ |
| Token optimization | ❌ | ✅ |
| Relationship tracking | ❌ | ✅ |
| Graph visualization | ❌ | ✅ |

---

## 📁 Repository Structure

```
pact-hx/
├── packages/
│   ├── langchain/              # 🦜 LangChain integration
│   │   ├── pact_langchain/    # Main package
│   │   ├── examples/          # Usage examples
│   │   ├── tests/             # Test suite
│   │   └── README.md          # Full documentation
│   │
│   ├── crewai/                # 🚧 Coming soon
│   ├── autogpt/               # 🚧 Coming soon
│   └── openai-assistants/     # 🚧 Coming soon
│
├── PACKAGE_SUMMARY.md         # Package overview
├── QUICKSTART.md              # 5-minute setup guide
└── README.md                  # This file
```

---

## 🎓 Documentation

- **LangChain Integration:** [packages/langchain/README.md](./packages/langchain/README.md)
- **Quick Start Guide:** [QUICKSTART.md](./QUICKSTART.md)
- **Package Summary:** [PACKAGE_SUMMARY.md](./PACKAGE_SUMMARY.md)
- **API Documentation:** https://docs.neurobloom.ai/pact
- **Examples:** See `packages/*/examples/` directories

---

## 💡 Use Cases

### Customer Support
- Track customer frustration levels
- Escalate to humans when needed
- Provide context-rich handoffs

### Coaching & Therapy
- Monitor emotional states
- Adapt tone based on feelings
- Track progress over time

### Sales & Marketing
- Understand prospect concerns
- Personalize outreach
- Build relationship context

### Personal Assistants
- Remember preferences
- Adapt to mood changes
- Provide contextual suggestions

---

## 🛠️ Development

### Setup

```bash
# Clone the repo
git clone https://github.com/neurobloomai/pact-hx.git
cd pact-hx

# Install LangChain integration in dev mode
cd packages/langchain
pip install -e ".[dev]"

# Run tests
pytest
```

### Contributing

We welcome contributions! See [CONTRIBUTING.md](./packages/langchain/CONTRIBUTING.md)

**Ways to contribute:**
- 🐛 Report bugs
- 💡 Suggest features
- 📝 Improve documentation
- 🧪 Add test cases
- 🎨 Build new integrations

---

## 📈 Roadmap

### Q4 2025
- [x] LangChain integration MVP
- [x] Core emotional tracking
- [x] Context consolidation
- [x] Comprehensive documentation

### Q1 2026
- [ ] PyPI publication
- [ ] CrewAI integration
- [ ] AutoGPT integration
- [ ] Community feedback integration

### Q2 2026
- [ ] OpenAI Assistants integration
- [ ] Self-hosted option
- [ ] Multi-session support
- [ ] Advanced analytics dashboard

### Q3 2026
- [ ] LangSmith integration
- [ ] Voice tone analysis
- [ ] Multi-modal memory
- [ ] Enterprise features

---

## 🔗 Links

- **Website:** https://neurobloom.ai
- **Documentation:** https://docs.neurobloom.ai/pact
- **Discord:** https://discord.gg/neurobloom
- **Twitter:** https://twitter.com/neurobloomai
- **GitHub:** https://github.com/neurobloomai/pact-hx
- **Email:** hello@neurobloom.ai

---

## 📄 License

MIT License - see [LICENSE](./packages/langchain/LICENSE)

---

## 🙏 Acknowledgments

Special thanks to:
- **LangChain** team for building an amazing framework
- **CrewAI** community for inspiring multi-agent patterns
- **OpenAI** for pushing the boundaries of AI
- Early beta testers and contributors

---

## 💰 Pricing

### Free Tier
- 10K tokens/month
- All core features
- Community support

### Paid Plans (Starting $20/month)
- Higher token limits
- Priority support
- Advanced analytics
- Team features

[View full pricing →](https://neurobloom.ai/pricing)

---

## ⭐ Star History

If you find PACT useful, give us a star!

[![Star History Chart](https://api.star-history.com/svg?repos=neurobloomai/pact-hx&type=Date)](https://star-history.com/#neurobloomai/pact-hx&Date)

---

<div align="center">

**Made with 🧠 by NeurobloomAI**

*Building AI that understands emotions*

[Website](https://neurobloom.ai) • [Docs](https://docs.neurobloom.ai) • [Discord](https://discord.gg/neurobloom) • [Twitter](https://twitter.com/neurobloomai)

</div>
