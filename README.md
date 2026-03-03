# Kiro Automation Framework

A reusable framework for safe AI-assisted development with trust levels and sandbox capabilities.

## Overview

This framework implements a trust level system (0-4) that allows controlled automation while maintaining safety and auditability. It combines the action system pattern with whitelist-based operation control.

## Trust Levels

- **Level 0**: Read-only operations (file reading, directory listing, search)
- **Level 1**: Safe file creation (new files only, no overwrites)
- **Level 2**: File modifications with automatic backups
- **Level 3**: Action scripts requiring human review and execution
- **Level 4**: Full automation with comprehensive logging and rollback

## Quick Start

```bash
# Initialize framework in your project
./scripts/init-framework.sh

# Configure trust level
echo "TRUST_LEVEL=2" > .automation-config

# Run with framework
python -m kiro_automation.cli
```

## Directory Structure

```
kiro-automation-framework/
├── src/                    # Framework source code
│   └── kiro_automation/
│       ├── trust_levels.py
│       ├── whitelist.py
│       ├── sandbox.py
│       └── action_runner.py
├── scripts/                # Helper scripts
├── examples/               # Usage examples
├── .dev/                   # Development artifacts (local only)
│   ├── actions/
│   └── logs/
└── docs/                   # Documentation
```

## Features

- Trust level enforcement
- Operation whitelisting
- Automatic backups before modifications
- Full audit trail
- Rollback capabilities
- Sandbox mode for testing
- Action script generation and execution

## Documentation

See `docs/` for detailed documentation:
- `trust-levels.md` - Trust level system details
- `whitelist.md` - Operation whitelist configuration
- `sandbox.md` - Sandbox mode usage
- `action-system.md` - Action script workflow

## License

MIT
