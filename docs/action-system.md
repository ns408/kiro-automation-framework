# Action System

The action system enables AI to generate executable scripts that humans review and execute, maintaining full control and audit trail.

## Overview

Instead of AI executing commands directly, it generates documented bash scripts that:
- Clearly describe what will happen
- Include safety measures (backups, validation)
- Provide full audit trail
- Allow human review before execution

## Components

### 1. Action Scripts
Executable bash scripts in `.dev/actions/` with:
- Clear description
- Reason for change
- List of affected files
- Step-by-step commands
- Automatic backups

### 2. Action Runner
Python class that:
- Generates action scripts
- Executes scripts with logging
- Maintains audit trail
- Provides rollback capability

### 3. Wrapper Script
`run-action.sh` that:
- Logs execution
- Captures output
- Records success/failure
- Maintains history

## Basic Usage

### Generate Action

```python
from kiro_automation import ActionRunner

runner = ActionRunner()

script_path = runner.generate_action(
    description="Refactor authentication module",
    commands=[
        "mv src/auth.py src/auth_old.py",
        "python scripts/refactor_auth.py",
        "pytest tests/test_auth.py"
    ],
    files_affected=["src/auth.py", "src/auth_old.py"],
    reason="Improve code structure and add type hints"
)

print(f"Action script created: {script_path}")
```

### Execute Action

```bash
# Review the script first
cat .dev/actions/001-refactor-authentication-module.sh

# Execute with wrapper
./run-action.sh .dev/actions/001-refactor-authentication-module.sh

# Check log
cat .dev/logs/actions.log
```

## Action Script Structure

Generated scripts follow this template:

```bash
#!/bin/bash
# ACTION: Brief description
# REASON: Why this is needed
# FILES: file1.py, file2.py
# CREATED: 2026-03-02

set -e

echo "📝 ACTION: Description"
echo ""
echo "This will:"
echo "  1. First step"
echo "  2. Second step"
echo ""

# Backup files before modifying
[ -f "file1.py" ] && cp "file1.py" "file1.py.backup"

# Execute commands
command1
command2

echo "✅ Action complete!"
```

## Python API

### ActionRunner Class

```python
from kiro_automation import ActionRunner
from pathlib import Path

# Initialize
runner = ActionRunner(actions_dir=Path(".dev/actions"))

# Generate action
script = runner.generate_action(
    description="Update dependencies",
    commands=["pip install -U package1 package2"],
    files_affected=["requirements.txt"],
    reason="Security updates"
)

# Execute action
result = runner.execute_action(script)

if result['status'] == 'success':
    print("Action completed successfully")
    print(result['output'])
else:
    print("Action failed")
    print(result['error'])

# List all actions
actions = runner.list_actions()
for action in actions:
    print(action.name)

# Get execution log
log = runner.get_log(lines=50)
print(log)
```

### Dry Run

Test action without executing:

```python
result = runner.execute_action(script, dry_run=True)
print(result['status'])  # 'dry_run'
```

## Integration with Trust Levels

Actions work with trust level system:

```python
from kiro_automation import TrustLevel, TrustLevelManager, ActionRunner

manager = TrustLevelManager(TrustLevel.ACTION_SCRIPTS)
runner = ActionRunner()

# Check if action generation allowed
if manager.is_allowed('generate_action'):
    script = runner.generate_action(...)
    print(f"Review and execute: ./run-action.sh {script}")

# Level 4 can auto-execute
manager.set_level(TrustLevel.FULL_AUTO)
if manager.is_allowed('execute_action'):
    result = runner.execute_action(script)
```

## Workflow Examples

### Simple File Modification

```python
runner = ActionRunner()

script = runner.generate_action(
    description="Add logging to main module",
    commands=[
        "sed -i '1i import logging' src/main.py",
        "python scripts/add_logging.py src/main.py"
    ],
    files_affected=["src/main.py"],
    reason="Improve debugging capability"
)

# Human reviews and executes
# ./run-action.sh .dev/actions/001-add-logging-to-main-module.sh
```

### Multi-Step Refactoring

```python
script = runner.generate_action(
    description="Refactor database layer",
    commands=[
        "mkdir -p src/db",
        "mv src/database.py src/db/connection.py",
        "python scripts/split_db_module.py",
        "pytest tests/test_db.py",
        "black src/db/"
    ],
    files_affected=[
        "src/database.py",
        "src/db/connection.py",
        "src/db/models.py",
        "src/db/queries.py"
    ],
    reason="Separate concerns and improve maintainability"
)
```

### Deployment Script

```python
script = runner.generate_action(
    description="Deploy to staging",
    commands=[
        "pytest",
        "black --check .",
        "mypy src/",
        "docker build -t app:staging .",
        "docker push app:staging",
        "kubectl apply -f k8s/staging/"
    ],
    files_affected=["k8s/staging/deployment.yaml"],
    reason="Deploy version 1.2.3 to staging"
)
```

## Audit Trail

### Log Format

`.dev/logs/actions.log`:
```
2026-03-02T10:30:00+00:00 | ACTION: 001-refactor-authentication-module
2026-03-02T10:30:00+00:00 | EXECUTING: .dev/actions/001-refactor-authentication-module.sh
📝 ACTION: Refactor authentication module
This will:
  1. Move old auth module
  2. Run refactoring script
  3. Run tests
✅ Action complete!
2026-03-02T10:30:15+00:00 | STATUS: ✅ Complete
---
```

### Query Log

```python
# Get recent actions
log = runner.get_log(lines=100)

# Parse log for specific action
with open('.dev/logs/actions.log') as f:
    for line in f:
        if 'refactor' in line.lower():
            print(line)
```

### Log Analysis

```bash
# Count successful actions
grep "STATUS: ✅" .dev/logs/actions.log | wc -l

# Find failed actions
grep "STATUS: ❌" .dev/logs/actions.log

# Actions in last hour
grep "$(date -d '1 hour ago' +%Y-%m-%d)" .dev/logs/actions.log
```

## Best Practices

### Clear Descriptions
Use descriptive action names:
```python
# Good
"Refactor authentication to use JWT tokens"

# Bad
"Update auth"
```

### Document Reasoning
Always explain why:
```python
reason="Current auth system has security vulnerabilities (CVE-2024-1234)"
```

### List All Affected Files
Be comprehensive:
```python
files_affected=[
    "src/auth.py",
    "src/middleware/auth.py",
    "tests/test_auth.py",
    "docs/authentication.md"
]
```

### Test Before Modifying
Include tests in action:
```python
commands=[
    "pytest tests/test_feature.py",  # Test first
    "python scripts/modify_feature.py",  # Then modify
    "pytest tests/test_feature.py"  # Test again
]
```

### Use Idempotent Commands
Make actions safe to re-run:
```python
commands=[
    "mkdir -p src/new_module",  # -p makes it idempotent
    "[ -f src/old.py ] && mv src/old.py src/new_module/",  # Check before move
]
```

### Review Before Execution
Always review generated scripts:
```bash
# Review
cat .dev/actions/001-action.sh

# Check affected files
grep "FILES:" .dev/actions/001-action.sh

# Execute only after review
./run-action.sh .dev/actions/001-action.sh
```

## Rollback

### Automatic Backups
Action scripts create backups automatically:
```bash
# Restore from backup
cp src/main.py.backup src/main.py
```

### Manual Rollback
```bash
# List backups
ls -lt *.backup

# Restore specific file
cp src/auth.py.backup src/auth.py

# Restore all backups in directory
for f in *.backup; do
    cp "$f" "${f%.backup}"
done
```

### Git Rollback
```bash
# View changes
git diff

# Restore specific file
git restore src/main.py

# Restore all changes
git restore .
```

## Advanced Usage

### Conditional Actions

```python
script = runner.generate_action(
    description="Update config if needed",
    commands=[
        "if [ ! -f config/production.yaml ]; then",
        "  cp config/default.yaml config/production.yaml",
        "fi"
    ],
    files_affected=["config/production.yaml"],
    reason="Ensure production config exists"
)
```

### Parameterized Actions

```python
def create_migration_action(version: str):
    return runner.generate_action(
        description=f"Run database migration {version}",
        commands=[
            f"alembic upgrade {version}",
            "python scripts/verify_migration.py"
        ],
        files_affected=["alembic/versions/*.py"],
        reason=f"Apply migration {version}"
    )

script = create_migration_action("abc123")
```

### Chained Actions

```python
# Generate multiple related actions
actions = []

actions.append(runner.generate_action(
    description="Step 1: Backup database",
    commands=["pg_dump mydb > backup.sql"],
    files_affected=["backup.sql"],
    reason="Safety before migration"
))

actions.append(runner.generate_action(
    description="Step 2: Run migration",
    commands=["alembic upgrade head"],
    files_affected=["alembic/versions/*.py"],
    reason="Apply schema changes"
))

actions.append(runner.generate_action(
    description="Step 3: Verify migration",
    commands=["python scripts/verify_schema.py"],
    files_affected=[],
    reason="Ensure migration succeeded"
))

# Execute in sequence
for action in actions:
    print(f"Execute: {action}")
    input("Press Enter to continue...")
    result = runner.execute_action(action)
    if result['status'] != 'success':
        print("Failed! Stopping.")
        break
```

## Troubleshooting

### Action Fails to Execute

```bash
# Check script permissions
ls -l .dev/actions/001-action.sh

# Make executable
chmod +x .dev/actions/001-action.sh

# Check for syntax errors
bash -n .dev/actions/001-action.sh
```

### Log Not Created

```bash
# Ensure log directory exists
mkdir -p .dev/logs

# Check permissions
ls -ld .dev/logs
```

### Backup Not Created

Check action script includes backup logic:
```bash
grep "backup" .dev/actions/001-action.sh
```

Add manually if needed:
```bash
cp file.py file.py.backup
```
