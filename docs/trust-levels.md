# Trust Levels

The trust level system provides graduated automation control from read-only to full automation.

## Overview

Trust levels (0-4) determine what operations the automation system can perform. Higher levels enable more powerful operations but require more careful oversight.

## Level Definitions

### Level 0: Read-Only
**Purpose:** Safe exploration and analysis

**Allowed Operations:**
- Read files
- List directories
- Search content
- Grep patterns

**Use Cases:**
- Code analysis
- Documentation review
- Finding patterns
- Understanding codebase

**Risk:** None - no modifications possible

### Level 1: Safe Creation
**Purpose:** Adding new content without risk of overwriting

**Allowed Operations:**
- All Level 0 operations
- Create new files (fails if exists)
- Create directories

**Use Cases:**
- Generating new code files
- Creating documentation
- Adding test files
- Scaffolding structure

**Risk:** Low - cannot overwrite existing files

### Level 2: Modify with Backup
**Purpose:** Safe modifications with rollback capability

**Allowed Operations:**
- All Level 1 operations
- Modify existing files (automatic backup)
- Append to files

**Use Cases:**
- Refactoring code
- Updating documentation
- Fixing bugs
- Adding features

**Risk:** Medium - files are modified but backups created automatically

**Backup Strategy:**
- Original file copied to `<filename>.backup`
- Timestamp added to backup name
- Backups stored in `.dev/backups/`

### Level 3: Action Scripts
**Purpose:** Complex operations requiring human review

**Allowed Operations:**
- All Level 2 operations
- Generate action scripts
- Write action scripts to `.dev/actions/`

**Use Cases:**
- Multi-step refactoring
- Database migrations
- Deployment scripts
- Complex transformations

**Risk:** Medium - scripts must be reviewed before execution

**Workflow:**
1. AI generates action script
2. Human reviews script
3. Human executes with `./run-action.sh`
4. Full audit trail maintained

### Level 4: Full Automation
**Purpose:** Trusted automation with comprehensive logging

**Allowed Operations:**
- All Level 3 operations
- Execute action scripts automatically
- Delete files
- Move/rename files
- Modify permissions

**Use Cases:**
- CI/CD pipelines
- Automated testing
- Batch processing
- Trusted workflows

**Risk:** High - full system access

**Safety Measures:**
- Comprehensive logging
- Rollback capability
- Operation whitelist
- Path restrictions
- Audit trail

## Configuration

### Set Trust Level

In `.automation-config`:
```bash
TRUST_LEVEL=2
```

### Programmatic Usage

```python
from kiro_automation import TrustLevel, TrustLevelManager

# Initialize with level
manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)

# Check if operation allowed
if manager.is_allowed('modify_file'):
    # Perform operation
    pass

# Require specific level
manager.require_level('delete_file', TrustLevel.FULL_AUTO)
```

## Best Practices

### Start Low, Increase Gradually
Begin with Level 0 or 1, increase as you gain confidence.

### Use Level 3 for Complex Changes
When multiple files need coordinated changes, use action scripts for review.

### Reserve Level 4 for Trusted Workflows
Only use full automation for well-tested, repeatable processes.

### Monitor Logs
Always review `.dev/logs/actions.log` after operations.

### Test in Sandbox First
Use sandbox mode to test automation before applying to real project.

## Combining with Whitelist

Trust levels and whitelists work together:
- Trust level determines operation categories
- Whitelist provides fine-grained control
- Both must allow operation for it to proceed

Example:
```python
# Trust level allows modify_file
manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)

# But whitelist restricts paths
whitelist = OperationWhitelist()
whitelist.add_path('src/')
whitelist.block_path('src/critical.py')

# Can modify src/utils.py ✅
# Cannot modify src/critical.py ❌
# Cannot modify config/settings.py ❌
```

## Rollback

### Level 2 Rollback
```bash
# Restore from automatic backup
cp file.py.backup file.py
```

### Level 3+ Rollback
```bash
# Review action log
cat .dev/logs/actions.log

# Restore from backups
ls .dev/backups/

# Or use git
git restore <file>
```

## Security Considerations

### Never Use Level 4 for Untrusted Input
If automation processes user input or external data, use Level 3 maximum.

### Restrict Paths at Higher Levels
Always use whitelist to restrict file access at Levels 3-4.

### Review Generated Scripts
Even at Level 3, always review action scripts before execution.

### Audit Regularly
Check logs frequently to ensure automation behaves as expected.
