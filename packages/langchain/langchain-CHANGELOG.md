# Changelog - pact-langchain

All notable changes to the **pact-langchain** package.

This is a sub-package of the PACT-HX monorepo.

---

## [0.1.0] - 2025-11-13

### 🎉 Initial Release

First public release of pact-langchain!

**PyPI:** https://pypi.org/project/pact-langchain/0.1.0/

### Added

- Drop-in memory replacement for LangChain
- Compatible with `BaseChatMemory` interface
- Works with `ConversationChain` and other chains
- Basic emotional intelligence tracking
- Session-based memory management
- REST API client for PACT server
- Comprehensive documentation and examples
- End-to-end integration tests

### Infrastructure

- Connects to deployed PACT API server
- SQLite-backed persistent storage
- RESTful API communication

### Known Limitations (MVP)

- Emotional state returns "neutral" (advanced analysis coming in v0.2.0)
- Context consolidation not yet implemented
- Basic error handling

### Coming in v0.2.0

- Advanced emotional analysis
- Intelligent context consolidation
- Memory graph visualization
- Enhanced error handling

---

**Full documentation:** https://github.com/neurobloomai/pact-hx/tree/main/packages/langchain
