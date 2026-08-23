# Contributing Guidelines

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies
5. Run tests

## Development Setup

```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Write docstrings for all public functions
- Keep functions focused and small

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Pull Request Process

1. Update README.md with details of changes if applicable
2. Update docs/ if architecture changes
3. Ensure tests pass
4. Request review from maintainers
