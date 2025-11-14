# Release Guide - pact-langchain v0.1.0

## 📂 File Locations

### Add CHANGELOG here:
```
pact-hx/packages/langchain/CHANGELOG.md
```

### GitHub Release Tag:
```
pact-langchain-v0.1.0
```
(NOT just `v0.1.0` - that's for entire repo!)

---

## 🚀 Steps

### 1. Add CHANGELOG to Package

```bash
cd /Users/akanuganti/pact-hx/packages/langchain

# Copy CHANGELOG
cp /path/to/langchain-CHANGELOG.md ./CHANGELOG.md

# Commit
git add CHANGELOG.md
git commit -m "docs(langchain): Add CHANGELOG for v0.1.0"
git push
```

---

### 2. Create Git Tag (Package-Specific)

```bash
cd /Users/akanuganti/pact-hx

# Create tag with package prefix
git tag -a pact-langchain-v0.1.0 -m "pact-langchain v0.1.0 - Initial Release"

# Push tag
git push origin pact-langchain-v0.1.0
```

---

### 3. Create GitHub Release

**Go to:** https://github.com/neurobloomai/pact-hx/releases/new

**Fill in:**

**Tag:** `pact-langchain-v0.1.0`

**Release title:** 
```
pact-langchain v0.1.0 - Initial Release
```

**Description:**
```markdown
# 🎉 pact-langchain v0.1.0 - Initial Release

LangChain memory integration with emotional intelligence!

## 📦 Installation

```bash
pip install pact-langchain
```

**PyPI:** https://pypi.org/project/pact-langchain/0.1.0/

## ✨ Features

✅ Drop-in LangChain memory replacement  
✅ Emotional intelligence tracking  
✅ Cloud-native architecture  
✅ Session-based persistence  

## 🚀 Quick Start

```python
from pact_langchain import PACTMemory

memory = PACTMemory(
    api_key="your-key",
    api_url="https://pact-hx.onrender.com"
)

# Use with LangChain!
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

conversation = ConversationChain(llm=ChatOpenAI(), memory=memory)
```

## 📝 Changelog

See [CHANGELOG.md](https://github.com/neurobloomai/pact-hx/blob/main/packages/langchain/CHANGELOG.md)

## 🔗 Links

- **Package Docs:** [packages/langchain/README.md](https://github.com/neurobloomai/pact-hx/tree/main/packages/langchain)
- **API Server:** https://pact-hx.onrender.com
- **Issues:** https://github.com/neurobloomai/pact-hx/issues

---

**Note:** This release is for the `pact-langchain` package only. Other PACT integrations (CrewAI, AutoGPT) coming soon!

**Built with 🧠 by NeurobloomAI**
```

---

## 📋 Why Package-Specific Tags?

### Because your repo will have multiple packages:

```
pact-langchain-v0.1.0      # LangChain integration
pact-langchain-v0.2.0      # LangChain update
pact-crewai-v0.1.0         # CrewAI integration (future)
pact-autogpt-v0.1.0        # AutoGPT integration (future)
pact-hx-v1.0.0             # Overall repo version (future)
```

**Each package gets its own versioning!** ✅

---

## 🎯 Monorepo Best Practices

### Tag Format:
```
{package-name}-v{version}
```

### Examples:
```
✅ pact-langchain-v0.1.0
✅ pact-crewai-v0.1.0
✅ pact-server-v0.1.0

❌ v0.1.0 (ambiguous - which package?)
```

---

## 📂 Final Structure

```
pact-hx/                           # Monorepo root
├── packages/
│   ├── langchain/
│   │   ├── CHANGELOG.md          # pact-langchain changes
│   │   ├── README.md
│   │   └── setup.py              # version="0.1.0"
│   │
│   ├── crewai/                   # Future
│   │   └── CHANGELOG.md          # pact-crewai changes
│   │
│   └── autogpt/                  # Future
│       └── CHANGELOG.md          # pact-autogpt changes
│
├── server/
│   └── CHANGELOG.md              # API server changes
│
└── CHANGELOG.md                  # Overall repo changes
```

---

## ✅ Summary

**For pact-langchain v0.1.0:**

1. ✅ CHANGELOG goes in: `/packages/langchain/CHANGELOG.md`
2. ✅ Git tag: `pact-langchain-v0.1.0`
3. ✅ GitHub release title: "pact-langchain v0.1.0"
4. ✅ Specific to this package only

**NOT:**
- ❌ CHANGELOG in repo root (that's for overall repo)
- ❌ Tag `v0.1.0` (ambiguous)
- ❌ Release for entire repo

---

**This is standard monorepo practice!** ✅
