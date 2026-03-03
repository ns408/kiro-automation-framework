"""
Example: Using the action system.

This example shows how to generate and execute action scripts
with full audit trail.
"""

from pathlib import Path
from kiro_automation import ActionRunner, TrustLevel, TrustLevelManager

def main():
    print("⚡ Action System Example\n")
    
    # Initialize action runner
    runner = ActionRunner()
    
    # Check trust level
    manager = TrustLevelManager(TrustLevel.ACTION_SCRIPTS)
    print(f"Trust level: {manager.level.name}")
    
    if not manager.is_allowed('generate_action'):
        print("❌ Trust level too low for action generation")
        return
    
    # Generate a simple action
    print("\n📝 Generating action script...")
    
    script = runner.generate_action(
        description="Create example module structure",
        commands=[
            "mkdir -p src/example",
            "touch src/example/__init__.py",
            "touch src/example/main.py",
            "echo '# Example module' > src/example/README.md"
        ],
        files_affected=[
            "src/example/__init__.py",
            "src/example/main.py",
            "src/example/README.md"
        ],
        reason="Set up new example module for demonstration"
    )
    
    print(f"✅ Action script created: {script}")
    print(f"\nTo execute, run:")
    print(f"  ./run-action.sh {script}")
    
    # List all actions
    print("\n📋 Available actions:")
    actions = runner.list_actions()
    if actions:
        for action in actions:
            print(f"  - {action.name}")
    else:
        print("  (none yet)")
    
    # Show how to execute (but don't actually execute)
    print("\n" + "="*50)
    print("To execute the action:")
    print(f"  1. Review: cat {script}")
    print(f"  2. Execute: ./run-action.sh {script}")
    print(f"  3. Check log: cat .dev/logs/actions.log")

def auto_execute_example():
    """Example with automatic execution (Trust Level 4)."""
    print("\n🚀 Auto-Execute Example\n")
    
    # Requires Trust Level 4
    manager = TrustLevelManager(TrustLevel.FULL_AUTO)
    
    if not manager.is_allowed('execute_action'):
        print("❌ Trust level too low for auto-execution")
        return
    
    runner = ActionRunner()
    
    # Generate action
    script = runner.generate_action(
        description="Create test file",
        commands=[
            "echo 'Test content' > test_auto.txt"
        ],
        files_affected=["test_auto.txt"],
        reason="Test automatic execution"
    )
    
    print(f"Generated: {script}")
    
    # Execute automatically
    print("\n⚡ Executing automatically...")
    result = runner.execute_action(script)
    
    if result['status'] == 'success':
        print("✅ Action completed successfully")
        print(f"\nOutput:\n{result['output']}")
    else:
        print("❌ Action failed")
        print(f"\nError:\n{result['error']}")
    
    # Show log
    print("\n📋 Recent log entries:")
    log = runner.get_log(lines=10)
    print(log)

def dry_run_example():
    """Example with dry run."""
    print("\n🔍 Dry Run Example\n")
    
    runner = ActionRunner()
    
    # Generate action
    script = runner.generate_action(
        description="Risky operation",
        commands=[
            "rm -rf /tmp/test_dir",
            "mkdir /tmp/test_dir"
        ],
        files_affected=[],
        reason="Clean up test directory"
    )
    
    print(f"Generated: {script}")
    
    # Dry run first
    print("\n🔍 Running dry run...")
    result = runner.execute_action(script, dry_run=True)
    
    print(f"Status: {result['status']}")
    print("Action was NOT executed (dry run)")
    
    # Review script before real execution
    print(f"\nReview script: cat {script}")
    print(f"Then execute: ./run-action.sh {script}")

if __name__ == '__main__':
    main()
    
    # Uncomment to run other examples
    # auto_execute_example()
    # dry_run_example()
