# Contributing to PACT for LangChain

Thanks for your interest in contributing! 🎉

## Quick Start

```bash
# Clone the repo
git clone https://github.com/neurobloomai/pact-hx.git
cd pact-hx/packages/langchain

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black pact_langchain/
```

## Development Guidelines

### Code Style
- Follow PEP 8
- Use `black` for formatting
- Use type hints where possible
- Write docstrings for public APIs

### Testing
- Write tests for new features
- Maintain test coverage above 80%
- Run `pytest` before submitting PR

### Commits
- Use clear, descriptive commit messages
- Follow conventional commits format:
  - `feat:` new features
  - `fix:` bug fixes
  - `docs:` documentation changes
  - `test:` test additions/changes
  - `refactor:` code refactoring

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes
6. Push to your fork
7. Open a Pull Request

## Reporting Issues

- Use GitHub Issues
- Include:
  - Clear description of the problem
  - Steps to reproduce
  - Expected vs actual behavior
  - Python version and environment details

## Questions?

- Join our [Discord](https://discord.gg/neurobloom)
- Email: hello@neurobloom.ai

---

**Thank you for contributing to PACT!** 🧠
