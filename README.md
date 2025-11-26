# context-engineering-reinvent

Redis context engineering course for AWS re:Invent

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

## Getting Started

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setup Project

```bash
# Sync dependencies
uv sync

# Run the application
uv run python main.py
```

## Development

```bash
# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>

# Update dependencies
uv sync
```
