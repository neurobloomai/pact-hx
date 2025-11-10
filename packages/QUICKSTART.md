# Quick Start Guide - PACT for LangChain

## 🚀 5-Minute Setup

### Step 1: Get Your API Key

Visit [neurobloom.ai](https://neurobloom.ai) and sign up for a free account. You'll get:
- `PACT_API_KEY` (starts with `sk_test_` or `sk_prod_`)
- 10K tokens/month free

### Step 2: Install the Package

```bash
# From PyPI (when published)
pip install pact-langchain

# Or from source (now)
cd packages/langchain
pip install -e .
```

### Step 3: Set Environment Variables

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your keys
PACT_API_KEY=sk_test_your_key_here
OPENAI_API_KEY=sk-your_openai_key_here
```

### Step 4: Run Your First Example

```python
# test.py
from pact_langchain import PACTMemory
from langchain.chains import ConversationChain
from langchain.llms import OpenAI
import os

memory = PACTMemory(api_key=os.getenv("PACT_API_KEY"))
llm = OpenAI(temperature=0.7)
conversation = ConversationChain(llm=llm, memory=memory)

# Have a conversation
print(conversation.predict(input="Hi! I'm excited about AI"))
print(conversation.predict(input="But I'm also a bit worried"))
print(conversation.predict(input="Can you help me?"))

# Check emotional state
state = memory.get_emotional_state()
print(f"\nDetected emotion: {state['current_emotion']}")
print(f"Emotional trend: {state['trend']}")
```

Run it:
```bash
python test.py
```

## 🎯 Try the Examples

### Basic Chatbot
```bash
python examples/basic_usage.py
```

### Emotional Tracking
```bash
python examples/emotional_tracking_complete.py
```

### Customer Support Bot
```bash
python examples/support_agent.py
```

## 🔧 Common Issues

### Issue: "ModuleNotFoundError: No module named 'pact_langchain'"
**Solution:** Install the package first:
```bash
pip install -e .
```

### Issue: "PACT_API_KEY not set"
**Solution:** Set environment variable:
```bash
export PACT_API_KEY="sk_test_..."  # Linux/Mac
set PACT_API_KEY="sk_test_..."     # Windows
```

### Issue: "Connection refused" or API errors
**Solution:** Check your API key is valid and you have internet connection.
Visit neurobloom.ai to verify your account.

## 📚 Next Steps

1. **Read the Full README:** See `README.md` for comprehensive documentation
2. **Check API Reference:** Visit docs.neurobloom.ai/pact/langchain
3. **Join Community:** discord.gg/neurobloom
4. **Star the Repo:** github.com/neurobloomai/pact-hx

## 💡 Quick Tips

- Use `emotional_tracking=True` for coaching/therapy bots
- Use `context_consolidation=True` for long conversations
- Use `max_token_limit` to control context size
- Call `memory.force_consolidation()` when you want to summarize

## 🎉 You're Ready!

You now have PACT Memory running with LangChain. Your agents can:
- ✅ Track emotional states
- ✅ Consolidate context automatically
- ✅ Remember what matters
- ✅ Save tokens

Happy building! 🧠

---

Questions? hello@neurobloom.ai
