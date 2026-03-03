# Contributing to Kiro Automation Framework

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/kiro-automation-framework.git
cd kiro-automation-framework

# Install development dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run verification
python3 verify.py
```

## Project Structure

```
kiro-automation-framework/
├── src/kiro_automation/      # Core framework
│   ├── trust_levels.py       # Trust level system
│   ├── whitelist.py          # Operation whitelist
│   ├── sandbox.py            # Sandbox mode
│   ├── action_runner.py      # Action scripts
│   └── logger.py             # Logging
├── tests/                    # Test suite
├── docs/                     # Documentation
├── examples/                 # Usage examples
└── scripts/                  # Helper scripts
```

## Adding Features

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Write code** in `src/kiro_automation/`

3. **Add tests** in `tests/`

4. **Update docs** in `docs/`

5. **Run tests**
   ```bash
   pytest
   ```

6. **Submit PR**

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Keep functions small
- No external dependencies (stdlib only)

## Testing

- Write tests for all new features
- Maintain 80%+ coverage
- Use pytest fixtures
- Test edge cases

## Documentation

- Update relevant docs in `docs/`
- Add examples if needed
- Update CHANGELOG.md
- Keep README.md current

## Logging

Use the framework logger:

```python
from kiro_automation.logger import get_logger

logger = get_logger()
logger.info("Event occurred", key="value")
```

## Release Process

1. Update version in `src/kiro_automation/__init__.py`
2. Update CHANGELOG.md
3. Run full test suite
4. Tag release: `git tag v0.2.0`
5. Push: `git push --tags`
