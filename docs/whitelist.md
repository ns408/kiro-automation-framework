# Operation Whitelist

Fine-grained control over which operations and paths are allowed in automation.

## Overview

While trust levels provide broad categories of allowed operations, the whitelist system enables precise control over:
- Specific operations
- File paths
- Auto-approval settings

## Configuration File

Create `.automation-whitelist.json`:

```json
{
  "allowed_operations": [
    "read_file",
    "create_file",
    "modify_file"
  ],
  "allowed_paths": [
    "/home/user/project/src",
    "/home/user/project/tests"
  ],
  "blocked_paths": [
    "/home/user/project/src/critical.py",
    "/home/user/project/config"
  ],
  "auto_approve": [
    "read_file",
    "list_dir"
  ]
}
```

## Usage

### Basic Setup

```python
from kiro_automation import OperationWhitelist

# Load from config
whitelist = OperationWhitelist()

# Or specify custom path
whitelist = OperationWhitelist(config_path=Path("custom-whitelist.json"))
```

### Check Operations

```python
# Check if operation allowed
if whitelist.is_operation_allowed('modify_file'):
    # Proceed
    pass

# Check if path allowed
if whitelist.is_path_allowed('/home/user/project/src/main.py'):
    # Proceed
    pass

# Check if requires approval
if whitelist.requires_approval('delete_file'):
    # Ask user for confirmation
    pass
```

### Modify Whitelist

```python
# Add operation
whitelist.add_operation('create_file', auto_approve=True)

# Add allowed path
whitelist.add_path('/home/user/project/src')

# Block specific path
whitelist.block_path('/home/user/project/src/critical.py')

# Save changes
whitelist.save()
```

## Operation Types

### Read Operations
- `read_file` - Read file contents
- `list_dir` - List directory contents
- `search` - Search for patterns
- `grep` - Grep patterns

### Write Operations
- `create_file` - Create new file
- `modify_file` - Modify existing file
- `append_file` - Append to file
- `mkdir` - Create directory

### Action Operations
- `generate_action` - Generate action script
- `write_action` - Write action to disk

### Destructive Operations
- `delete_file` - Delete file
- `move_file` - Move/rename file
- `execute_action` - Execute action script

## Path Matching

### Allowed Paths
Files must be under allowed paths to be accessed:

```python
whitelist.add_path('/home/user/project/src')

# Allowed
whitelist.is_path_allowed('/home/user/project/src/main.py')  # True
whitelist.is_path_allowed('/home/user/project/src/utils/helper.py')  # True

# Not allowed
whitelist.is_path_allowed('/home/user/project/config/secret.py')  # False
```

### Blocked Paths
Blocked paths override allowed paths:

```python
whitelist.add_path('/home/user/project/src')
whitelist.block_path('/home/user/project/src/critical.py')

# Allowed
whitelist.is_path_allowed('/home/user/project/src/main.py')  # True

# Blocked (even though src/ is allowed)
whitelist.is_path_allowed('/home/user/project/src/critical.py')  # False
```

### Empty Allowed Paths
If `allowed_paths` is empty, all paths are allowed (except blocked):

```json
{
  "allowed_paths": [],
  "blocked_paths": ["/etc", "/usr/bin"]
}
```

## Auto-Approval

Operations in `auto_approve` don't require manual confirmation:

```python
# Read operations typically auto-approved
whitelist.add_operation('read_file', auto_approve=True)

# Destructive operations require approval
whitelist.add_operation('delete_file', auto_approve=False)

# Check if approval needed
if whitelist.requires_approval('delete_file'):
    confirm = input("Delete file? (yes/no): ")
    if confirm != 'yes':
        return
```

## Integration with Trust Levels

Whitelist and trust levels work together:

```python
from kiro_automation import TrustLevel, TrustLevelManager, OperationWhitelist

manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)
whitelist = OperationWhitelist()

def can_perform(operation, path):
    # Both must allow
    return (
        manager.is_allowed(operation) and
        whitelist.is_operation_allowed(operation) and
        whitelist.is_path_allowed(path)
    )

# Example
can_perform('modify_file', '/home/user/project/src/main.py')
```

## Common Patterns

### Development Environment

```json
{
  "allowed_operations": [
    "read_file", "list_dir", "search",
    "create_file", "modify_file", "append_file"
  ],
  "allowed_paths": [
    "/home/user/project/src",
    "/home/user/project/tests",
    "/home/user/project/docs"
  ],
  "blocked_paths": [
    "/home/user/project/src/config/secrets.py"
  ],
  "auto_approve": [
    "read_file", "list_dir", "search"
  ]
}
```

### Production Environment

```json
{
  "allowed_operations": [
    "read_file", "list_dir"
  ],
  "allowed_paths": [
    "/var/log/app"
  ],
  "blocked_paths": [],
  "auto_approve": [
    "read_file", "list_dir"
  ]
}
```

### CI/CD Pipeline

```json
{
  "allowed_operations": [
    "read_file", "list_dir", "search",
    "create_file", "modify_file",
    "generate_action", "write_action", "execute_action"
  ],
  "allowed_paths": [
    "/workspace"
  ],
  "blocked_paths": [
    "/workspace/.git",
    "/workspace/secrets"
  ],
  "auto_approve": [
    "read_file", "list_dir", "search",
    "create_file", "modify_file"
  ]
}
```

## Best Practices

### Start Restrictive
Begin with minimal permissions, expand as needed:

```python
whitelist = OperationWhitelist()
whitelist.add_operation('read_file', auto_approve=True)
whitelist.add_operation('list_dir', auto_approve=True)
whitelist.save()
```

### Use Path Restrictions
Always restrict paths in production:

```python
whitelist.add_path('/home/user/project/src')
whitelist.block_path('/home/user/project/src/config')
```

### Block Sensitive Files
Explicitly block sensitive files:

```python
sensitive = [
    'secrets.py',
    'credentials.json',
    '.env',
    'private_key.pem'
]

for file in sensitive:
    whitelist.block_path(f'/home/user/project/{file}')
```

### Review Auto-Approvals
Only auto-approve truly safe operations:

```python
# Safe to auto-approve
safe_ops = ['read_file', 'list_dir', 'search', 'grep']

# Require approval
risky_ops = ['delete_file', 'move_file', 'execute_action']
```

### Version Control Whitelist
Commit `.automation-whitelist.json` to version control:

```bash
git add .automation-whitelist.json
git commit -m "Add automation whitelist"
```

## Dynamic Whitelists

Create whitelists programmatically:

```python
def create_dev_whitelist():
    whitelist = OperationWhitelist()
    
    # Read operations
    for op in ['read_file', 'list_dir', 'search', 'grep']:
        whitelist.add_operation(op, auto_approve=True)
    
    # Write operations
    for op in ['create_file', 'modify_file', 'append_file']:
        whitelist.add_operation(op, auto_approve=False)
    
    # Paths
    whitelist.add_path(str(Path.cwd() / 'src'))
    whitelist.add_path(str(Path.cwd() / 'tests'))
    
    # Blocked
    whitelist.block_path(str(Path.cwd() / 'src' / 'secrets.py'))
    
    whitelist.save()
    return whitelist
```

## Troubleshooting

### Operation Denied

```python
try:
    if not whitelist.is_operation_allowed('modify_file'):
        raise PermissionError("Operation not whitelisted")
except PermissionError as e:
    print(f"Error: {e}")
    print("Add to whitelist:")
    print('  whitelist.add_operation("modify_file")')
```

### Path Denied

```python
path = '/home/user/project/config/settings.py'

if not whitelist.is_path_allowed(path):
    print(f"Path not allowed: {path}")
    print("Allowed paths:", whitelist.allowed_paths)
    print("Blocked paths:", whitelist.blocked_paths)
```

### Whitelist Not Loading

```python
from pathlib import Path

config_path = Path('.automation-whitelist.json')

if not config_path.exists():
    print("Whitelist config not found")
    print("Creating default whitelist...")
    whitelist = OperationWhitelist()
    whitelist.add_operation('read_file', auto_approve=True)
    whitelist.save()
```
