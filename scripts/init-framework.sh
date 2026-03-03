#!/bin/bash
# Initialize Kiro Automation Framework in a project

set -e

echo "🚀 Initializing Kiro Automation Framework"
echo ""

# Create directory structure
echo "Creating directories..."
mkdir -p .dev/{actions,logs}
mkdir -p src

# Copy run-action.sh if not exists
if [ ! -f "run-action.sh" ]; then
    echo "Creating run-action.sh..."
    cat > run-action.sh << 'EOF'
#!/bin/bash
set -e

SCRIPT="$1"
LOG=".dev/logs/actions.log"
TIMESTAMP=$(date -Iseconds)

if [ -z "$SCRIPT" ]; then
    echo "Usage: ./run-action.sh <action-script>"
    exit 1
fi

mkdir -p .dev/logs

echo "$TIMESTAMP | ACTION: $(basename $SCRIPT .sh)" >> "$LOG"
echo "$TIMESTAMP | EXECUTING: $SCRIPT" >> "$LOG"

if bash "$SCRIPT" 2>&1 | tee -a "$LOG"; then
    echo "$TIMESTAMP | STATUS: ✅ Complete" >> "$LOG"
else
    echo "$TIMESTAMP | STATUS: ❌ Failed" >> "$LOG"
    exit 1
fi

echo "---" >> "$LOG"
EOF
    chmod +x run-action.sh
fi

# Create default config
if [ ! -f ".automation-config" ]; then
    echo "Creating .automation-config..."
    cat > .automation-config << 'EOF'
TRUST_LEVEL=2
SANDBOX_MODE=false
EOF
fi

# Update .gitignore
if [ -f ".gitignore" ]; then
    if ! grep -q ".dev/" .gitignore; then
        echo "Updating .gitignore..."
        echo ".dev/" >> .gitignore
    fi
else
    echo "Creating .gitignore..."
    cat > .gitignore << 'EOF'
.dev/
.kiro/
__pycache__/
*.pyc
*.backup
EOF
fi

echo ""
echo "✅ Framework initialized!"
echo ""
echo "Next steps:"
echo "  1. Configure trust level in .automation-config"
echo "  2. Use the framework in your automation scripts"
echo "  3. Generate actions with ActionRunner"
echo "  4. Execute with: ./run-action.sh .dev/actions/<script>.sh"
