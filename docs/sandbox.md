# Sandbox Mode

Sandbox mode provides an isolated environment for testing automation before applying changes to your real project.

## Overview

A sandbox is a temporary copy of your project where automation can run safely. You can review changes, test functionality, and then decide whether to apply them to the real project.

## Use Cases

- **Testing New Automation:** Try automation workflows without risk
- **Iterative Development:** Let AI iterate multiple times in isolation
- **Change Preview:** See exactly what will change before committing
- **Learning:** Understand what automation does in safe environment
- **Debugging:** Test fixes without affecting real code

## Basic Usage

### Python API

```python
from kiro_automation import Sandbox

# Create sandbox
sandbox = Sandbox()
sandbox_path = sandbox.create()
sandbox.copy_project()

print(f"Sandbox created at: {sandbox_path}")

# Work in sandbox
# ... automation runs here ...

# Review changes
changes = sandbox.diff()
print(f"Added: {changes['added']}")
print(f"Modified: {changes['modified']}")
print(f"Deleted: {changes['deleted']}")

# Apply changes if satisfied
sandbox.apply_changes()

# Or discard
sandbox.cleanup()
```

### Configuration

In `.automation-config`:
```bash
SANDBOX_MODE=true
SANDBOX_AUTO_APPLY=false
```

## Workflow

### 1. Create Sandbox
```python
sandbox = Sandbox()
sandbox_path = sandbox.create()
```

Creates temporary directory with unique name.

### 2. Copy Project
```python
sandbox.copy_project(exclude_patterns=['.git', '__pycache__', '.venv'])
```

Copies project files, excluding specified patterns.

### 3. Run Automation
All automation operations work on sandbox copy:
```python
# Operations happen in sandbox
file_path = sandbox.get_path('src/main.py')
# Modify file_path...
```

### 4. Review Changes
```python
changes = sandbox.diff()

for file in changes['modified']:
    print(f"Modified: {file}")
    # Show diff, review changes
```

### 5. Apply or Discard
```python
# Apply changes to real project
sandbox.apply_changes()

# Or discard everything
sandbox.cleanup()
```

## Advanced Features

### Selective Application

Apply only specific changes:
```python
changes = sandbox.diff()

# Apply only certain files
for file in changes['modified']:
    if file.startswith('src/'):
        src = sandbox.get_path(file)
        dest = Path(file)
        shutil.copy2(src, dest)
```

### Multiple Iterations

Let automation iterate in sandbox:
```python
sandbox = Sandbox()
sandbox.create()
sandbox.copy_project()

for iteration in range(5):
    # Run automation
    # Check results
    # Continue or break
    
    if satisfied:
        break

sandbox.apply_changes()
```

### Diff Preview

Show detailed diff before applying:
```python
import difflib

changes = sandbox.diff()

for file in changes['modified']:
    original = Path(file).read_text().splitlines()
    modified = sandbox.get_path(file).read_text().splitlines()
    
    diff = difflib.unified_diff(original, modified, lineterm='')
    print('\n'.join(diff))
```

## Integration with Trust Levels

Sandbox mode works with all trust levels:

```python
from kiro_automation import TrustLevel, TrustLevelManager, Sandbox

# Create sandbox
sandbox = Sandbox()
sandbox.create()
sandbox.copy_project()

# Set trust level for sandbox operations
manager = TrustLevelManager(TrustLevel.FULL_AUTO)

# Run automation in sandbox with high trust level
# ... operations ...

# Review before applying to real project
changes = sandbox.diff()
if looks_good(changes):
    sandbox.apply_changes()
```

**Key Insight:** You can use higher trust levels in sandbox because changes are isolated.

## Best Practices

### Always Review Changes
Never blindly apply sandbox changes. Review the diff first.

### Use for Complex Operations
Sandbox is especially valuable for multi-file refactoring.

### Test Incrementally
Apply changes incrementally rather than all at once.

### Keep Sandbox Clean
Clean up sandbox after use to avoid disk space issues.

### Exclude Large Files
Exclude large files/directories when copying to sandbox:
```python
sandbox.copy_project(exclude_patterns=[
    '.git', 'node_modules', '.venv', 'dist', 'build'
])
```

## Example: Safe Refactoring

```python
from kiro_automation import Sandbox, TrustLevelManager, TrustLevel

def safe_refactor():
    # Create sandbox
    sandbox = Sandbox()
    sandbox.create()
    sandbox.copy_project()
    
    # High trust level in sandbox
    manager = TrustLevelManager(TrustLevel.FULL_AUTO)
    
    # Run refactoring automation
    # ... multiple operations ...
    
    # Review changes
    changes = sandbox.diff()
    
    print("Changes to be applied:")
    print(f"  Added: {len(changes['added'])} files")
    print(f"  Modified: {len(changes['modified'])} files")
    print(f"  Deleted: {len(changes['deleted'])} files")
    
    # Show details
    for file in changes['modified']:
        print(f"  - {file}")
    
    # Confirm before applying
    response = input("Apply changes? (yes/no): ")
    
    if response.lower() == 'yes':
        sandbox.apply_changes()
        print("✅ Changes applied")
    else:
        print("❌ Changes discarded")
    
    # Cleanup
    sandbox.cleanup()

safe_refactor()
```

## Limitations

### Not a Full VM
Sandbox is file-based only. It doesn't isolate:
- Network access
- System calls
- Environment variables
- Running processes

### Disk Space
Sandbox creates full copy of project. Large projects consume significant space.

### Performance
Copying large projects takes time. Consider excluding unnecessary files.

## Troubleshooting

### Sandbox Creation Fails
```python
# Check permissions
sandbox = Sandbox(base_path=Path('/tmp/my-sandbox'))
```

### Copy Takes Too Long
```python
# Exclude more patterns
sandbox.copy_project(exclude_patterns=[
    '.git', 'node_modules', '.venv', 'dist', 'build',
    '*.log', '*.tmp', '__pycache__'
])
```

### Diff Shows Too Many Changes
```python
# Filter diff results
changes = sandbox.diff()
relevant = [f for f in changes['modified'] if f.endswith('.py')]
```

## Integration with Action System

Combine sandbox with action scripts:

```python
from kiro_automation import Sandbox, ActionRunner

sandbox = Sandbox()
sandbox.create()
sandbox.copy_project()

# Generate action in sandbox context
runner = ActionRunner(actions_dir=sandbox.get_path('.dev/actions'))
script = runner.generate_action(
    description="Refactor module",
    commands=["python refactor.py"],
    files_affected=["src/module.py"],
    reason="Improve code structure"
)

# Execute in sandbox
result = runner.execute_action(script)

# Review and apply
if result['status'] == 'success':
    changes = sandbox.diff()
    # Review and apply...
```
