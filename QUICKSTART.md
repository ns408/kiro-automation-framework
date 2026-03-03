# Quick Start Guide

Get started with Kiro Automation Framework in 5 minutes.

## Installation

### Option 1: Install from source
```bash
git clone https://github.com/yourusername/kiro-automation-framework.git
cd kiro-automation-framework
pip install -e .
```

### Option 2: Copy to your project
```bash
# Copy the framework to your project
cp -r kiro-automation-framework/src/kiro_automation your-project/
cp kiro-automation-framework/run-action.sh your-project/
```

## Basic Setup

### 1. Initialize in your project
```bash
cd your-project
./scripts/init-framework.sh
```

This creates:
- `.dev/actions/` - Action scripts directory
- `.dev/logs/` - Log files
- `run-action.sh` - Action execution wrapper
- `.automation-config` - Configuration file

### 2. Configure trust level

Edit `.automation-config`:
```bash
TRUST_LEVEL=2  # Start with level 2 (modify with backup)
SANDBOX_MODE=false
```

## First Automation

### Example 1: Read-only exploration (Level 0)

```python
from kiro_automation import TrustLevel, TrustLevelManager

manager = TrustLevelManager(TrustLevel.READ_ONLY)

# Safe operations
if manager.is_allowed('read_file'):
    # Read and analyze files
    pass
```

### Example 2: Create new files (Level 1)

```python
from kiro_automation import TrustLevel, TrustLevelManager
from pathlib import Path

manager = TrustLevelManager(TrustLevel.SAFE_CREATE)

if manager.is_allowed('create_file'):
    # Create new file
    new_file = Path('src/new_module.py')
    new_file.write_text('# New module\n')
```

### Example 3: Modify with backup (Level 2)

```python
from kiro_automation import TrustLevel, TrustLevelManager
from pathlib import Path
import shutil

manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)

if manager.is_allowed('modify_file'):
    file = Path('src/main.py')
    
    # Backup first
    shutil.copy(file, f"{file}.backup")
    
    # Modify
    content = file.read_text()
    file.write_text(content + "\n# Modified\n")
```

### Example 4: Action scripts (Level 3)

```python
from kiro_automation import ActionRunner, TrustLevel, TrustLevelManager

manager = TrustLevelManager(TrustLevel.ACTION_SCRIPTS)
runner = ActionRunner()

if manager.is_allowed('generate_action'):
    script = runner.generate_action(
        description="Add logging to module",
        commands=[
            "sed -i '1i import logging' src/main.py",
            "pytest tests/test_main.py"
        ],
        files_affected=["src/main.py"],
        reason="Improve debugging"
    )
    
    print(f"Review and execute: ./run-action.sh {script}")
```

## Using Sandbox

Test automation safely:

```python
from kiro_automation import Sandbox

# Create sandbox
sandbox = Sandbox()
sandbox.create()
sandbox.copy_project()

# Work in sandbox
test_file = sandbox.get_path('test.txt')
test_file.write_text('Testing in sandbox')

# Review changes
changes = sandbox.diff()
print(f"Added: {changes['added']}")

# Apply if satisfied
if input("Apply? (yes/no): ") == 'yes':
    sandbox.apply_changes()

# Cleanup
sandbox.cleanup()
```

## Using Whitelist

Control access precisely:

```python
from kiro_automation import OperationWhitelist
from pathlib import Path

whitelist = OperationWhitelist()

# Allow operations
whitelist.add_operation('read_file', auto_approve=True)
whitelist.add_operation('modify_file', auto_approve=False)

# Allow paths
whitelist.add_path(str(Path.cwd() / 'src'))

# Block sensitive files
whitelist.block_path(str(Path.cwd() / 'src' / 'secrets.py'))

# Save
whitelist.save()

# Check access
if whitelist.is_path_allowed('/path/to/file'):
    # Proceed
    pass
```

## Complete Example

```python
from pathlib import Path
from kiro_automation import (
    TrustLevel, TrustLevelManager,
    OperationWhitelist, Sandbox, ActionRunner
)

# Setup
manager = TrustLevelManager(TrustLevel.ACTION_SCRIPTS)
whitelist = OperationWhitelist()
whitelist.add_path(str(Path.cwd() / 'src'))
whitelist.save()

# Create sandbox
sandbox = Sandbox()
sandbox.create()
sandbox.copy_project()

# Work in sandbox
new_file = sandbox.get_path('src/feature.py')
new_file.write_text('def feature(): pass')

# Review
changes = sandbox.diff()
print(f"Changes: {len(changes['added'])} added")

# Generate action
runner = ActionRunner()
script = runner.generate_action(
    description="Add new feature",
    commands=["echo 'Feature added'"],
    files_affected=changes['added'],
    reason="New feature implementation"
)

# Apply
sandbox.apply_changes()
sandbox.cleanup()

print(f"Execute: ./run-action.sh {script}")
```

## Next Steps

1. **Read the docs**: Check `docs/` for detailed documentation
2. **Run examples**: Try examples in `examples/`
3. **Configure whitelist**: Set up `.automation-whitelist.json`
4. **Start automating**: Begin with Level 0-1, increase gradually

## Common Patterns

### Pattern 1: Safe exploration
```python
# Level 0: Read-only
manager = TrustLevelManager(TrustLevel.READ_ONLY)
# Analyze codebase safely
```

### Pattern 2: Iterative development
```python
# Use sandbox for multiple iterations
sandbox = Sandbox()
sandbox.create()
sandbox.copy_project()

for i in range(5):
    # Make changes
    # Test
    # Iterate
    pass

sandbox.apply_changes()
```

### Pattern 3: Reviewed automation
```python
# Level 3: Generate actions for review
runner = ActionRunner()
script = runner.generate_action(...)
# Human reviews and executes
```

## Troubleshooting

### Permission denied
```python
# Check trust level
print(manager.level.name)

# Check whitelist
print(whitelist.is_operation_allowed('operation'))
print(whitelist.is_path_allowed('/path'))
```

### Action script fails
```bash
# Check script syntax
bash -n .dev/actions/001-script.sh

# Check permissions
chmod +x .dev/actions/001-script.sh

# Check logs
cat .dev/logs/actions.log
```

### Sandbox issues
```python
# Exclude large directories
sandbox.copy_project(exclude_patterns=[
    '.git', 'node_modules', '.venv', 'dist'
])
```

## Resources

- **Documentation**: `docs/`
- **Examples**: `examples/`
- **Action log**: `.dev/logs/actions.log`
- **Whitelist**: `.automation-whitelist.json`

## Support

- GitHub Issues: [Report issues](https://github.com/yourusername/kiro-automation-framework/issues)
- Documentation: [Full docs](docs/)
