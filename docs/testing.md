# Testing Guide

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_trust_levels.py
```

### Run with coverage
```bash
pytest --cov=kiro_automation --cov-report=html
```

### Run verbose
```bash
pytest -v
```

## Test Structure

```
tests/
├── test_trust_levels.py    # Trust level system tests
├── test_whitelist.py        # Whitelist tests
├── test_sandbox.py          # Sandbox tests
└── test_action_runner.py    # Action runner tests
```

## What's Tested

### Trust Levels
- Level initialization
- Permission checking at each level
- Level transitions
- Permission errors

### Whitelist
- Operation whitelisting
- Path restrictions
- Blocked paths
- Save/load configuration

### Sandbox
- Creation and cleanup
- File operations
- Change tracking (diff)
- Isolation

### Action Runner
- Script generation
- Execution (dry run)
- Logging
- Action listing

## Adding Tests

Create new test file in `tests/`:

```python
import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from kiro_automation import YourModule

def test_your_feature():
    # Test code
    assert True
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install pytest
      - run: pytest
```
