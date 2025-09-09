# PACT-HX: Human Experience Layer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

PACT-HX provides primitives for personalized attention, emotional context retention, adaptive communication, and values alignment in AI systems.

## Quick Start

```python
from pact_hx.primitives.attention import AttentionManager

# Create attention manager
manager = AttentionManager("agent-001")

# Update attention
result = manager.update_attention(
    entities=["user_preferences", "current_task"], 
    context="User is asking about their preferences"
)
```

## Features

- **Attention Management**: Track what matters to each user
- **Memory Persistence**: Episodic, semantic, and identity memory layers  
- **Tone Adaptation**: Dynamic communication style adjustment
- **Value Alignment**: Detect and resolve value conflicts

## Installation

```bash
pip install pact-hx
```

## Documentation

- [Getting Started](docs/getting_started.md)
- [API Reference](docs/api_reference/)
- [Examples](examples/)

## Contributing

See [CONTRIBUTING.md](docs/contributing.md)

## License

MIT License - see [LICENSE](LICENSE) file.
