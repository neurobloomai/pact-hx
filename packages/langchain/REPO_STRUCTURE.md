# PACT-HX Repository Structure

## Monorepo Layout

```
pact-hx/
├── packages/
│   ├── langchain/
│   │   ├── CHANGELOG.md
│   │   ├── README.md
│   │   ├── setup.py
│   │   └── pact_langchain/
│   │
│   ├── crewai/
│   │   └── CHANGELOG.md
│   │
│   └── autogpt/
│       └── CHANGELOG.md
│
├── server/
│   ├── CHANGELOG.md
│   └── src/
│
├── docs/
│
├── CHANGELOG.md
├── README.md
└── LICENSE
```

## Changelog Locations

| Package | Changelog Location | Current Version |
|---------|-------------------|-----------------|
| pact-langchain | `/packages/langchain/CHANGELOG.md` | v0.1.0 ✅ |
| pact-crewai | `/packages/crewai/CHANGELOG.md` | Coming soon |
| pact-autogpt | `/packages/autogpt/CHANGELOG.md` | Coming soon |
| pact-server | `/server/CHANGELOG.md` | In development |
| Overall repo | `/CHANGELOG.md` | Future |

## Git Tags

Each package gets its own versioned tags:

```bash
# LangChain integration
pact-langchain-v0.1.0
pact-langchain-v0.2.0
pact-langchain-v1.0.0

# CrewAI integration (future)
pact-crewai-v0.1.0

# AutoGPT integration (future)
pact-autogpt-v0.1.0

# Server releases
pact-server-v0.1.0

# Overall repo milestones
pact-hx-v1.0.0
```

## Release Workflow

### For pact-langchain v0.1.0:

```bash
# 1. Update package changelog
cd packages/langchain
vim CHANGELOG.md  # Add v0.1.0 entry

# 2. Commit
git add CHANGELOG.md
git commit -m "docs(langchain): Add CHANGELOG for v0.1.0"

# 3. Create tag
git tag -a pact-langchain-v0.1.0 -m "pact-langchain v0.1.0"

# 4. Push
git push origin main
git push origin pact-langchain-v0.1.0

# 5. Create GitHub release
# Go to: github.com/neurobloomai/pact-hx/releases/new
# Tag: pact-langchain-v0.1.0
# Title: pact-langchain v0.1.0 - Initial Release
```

## Why Package-Specific Tags?

**Problem with generic tags:**
```
v0.1.0  ← Which package is this?
```

**Solution with prefixed tags:**
```
pact-langchain-v0.1.0   ← Clear!
pact-crewai-v0.1.0      ← Clear!
```

## Example: Multiple Releases

```
Timeline:
Nov 13: pact-langchain-v0.1.0   (Released ✅)
Dec 01: pact-langchain-v0.2.0   (Planned)
Dec 15: pact-crewai-v0.1.0      (Planned)
Jan 10: pact-langchain-v0.3.0   (Planned)
```

Each package evolves independently!

---

**Standard monorepo practice** ✅
