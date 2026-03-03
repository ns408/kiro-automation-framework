"""
Example: Complete workflow combining all features.

This example demonstrates a complete automation workflow using:
- Trust levels
- Whitelist
- Sandbox
- Action system
"""

from pathlib import Path
from kiro_automation import (
    TrustLevel,
    TrustLevelManager,
    OperationWhitelist,
    Sandbox,
    ActionRunner
)

def complete_workflow():
    """Complete automation workflow with all safety features."""
    
    print("🎯 Complete Automation Workflow\n")
    print("="*60)
    
    # Step 1: Configure trust level
    print("\n1️⃣  Configuring trust level...")
    manager = TrustLevelManager(TrustLevel.ACTION_SCRIPTS)
    print(f"   Trust level: {manager.level.name}")
    
    # Step 2: Set up whitelist
    print("\n2️⃣  Setting up whitelist...")
    whitelist = OperationWhitelist()
    
    # Allow operations
    whitelist.add_operation('read_file', auto_approve=True)
    whitelist.add_operation('create_file', auto_approve=True)
    whitelist.add_operation('modify_file', auto_approve=False)
    whitelist.add_operation('generate_action', auto_approve=False)
    
    # Allow paths
    project_root = Path.cwd()
    whitelist.add_path(str(project_root / 'src'))
    whitelist.add_path(str(project_root / 'examples'))
    
    # Block sensitive paths
    whitelist.block_path(str(project_root / 'src' / 'secrets.py'))
    
    whitelist.save()
    print("   ✅ Whitelist configured")
    
    # Step 3: Create sandbox
    print("\n3️⃣  Creating sandbox environment...")
    sandbox = Sandbox()
    sandbox_path = sandbox.create()
    sandbox.copy_project(exclude_patterns=[
        '.git', '__pycache__', '.venv', '.dev'
    ])
    print(f"   ✅ Sandbox created: {sandbox_path}")
    
    # Step 4: Run automation in sandbox
    print("\n4️⃣  Running automation in sandbox...")
    
    # Simulate creating new files
    new_file = sandbox.get_path('src/new_feature.py')
    new_file.parent.mkdir(parents=True, exist_ok=True)
    new_file.write_text("""
def new_feature():
    '''New feature implementation.'''
    return "Hello from new feature!"
""".strip())
    print("   ✅ Created new_feature.py")
    
    # Simulate modifying existing file
    readme = sandbox.get_path('README.md')
    if readme.exists():
        content = readme.read_text()
        readme.write_text(content + "\n\n## New Feature\n\nAdded new feature module.\n")
        print("   ✅ Modified README.md")
    
    # Step 5: Review changes
    print("\n5️⃣  Reviewing changes...")
    changes = sandbox.diff()
    
    print(f"\n   📊 Summary:")
    print(f"      Added: {len(changes['added'])} files")
    print(f"      Modified: {len(changes['modified'])} files")
    print(f"      Deleted: {len(changes['deleted'])} files")
    
    if changes['added']:
        print(f"\n   📄 Added files:")
        for file in changes['added']:
            print(f"      + {file}")
    
    if changes['modified']:
        print(f"\n   📝 Modified files:")
        for file in changes['modified']:
            print(f"      ~ {file}")
    
    # Step 6: Generate action script
    print("\n6️⃣  Generating action script...")
    
    runner = ActionRunner()
    
    if manager.is_allowed('generate_action'):
        script = runner.generate_action(
            description="Apply sandbox changes to project",
            commands=[
                "# Changes reviewed and approved in sandbox",
                "echo 'Applying changes...'",
                "# Files will be copied from sandbox"
            ],
            files_affected=changes['added'] + changes['modified'],
            reason="Implement new feature after sandbox testing"
        )
        print(f"   ✅ Action script: {script}")
    else:
        print("   ❌ Trust level too low for action generation")
        script = None
    
    # Step 7: Decision point
    print("\n7️⃣  Decision point...")
    print("   " + "="*56)
    
    if script:
        print(f"\n   Next steps:")
        print(f"   1. Review action: cat {script}")
        print(f"   2. Apply changes: sandbox.apply_changes()")
        print(f"   3. Execute action: ./run-action.sh {script}")
        print(f"   4. Or discard: sandbox.cleanup()")
    
    response = input("\n   Apply changes? (yes/no): ")
    
    if response.lower() == 'yes':
        print("\n   ✅ Applying changes...")
        applied = sandbox.apply_changes()
        print(f"      Applied {len(applied['added']) + len(applied['modified'])} changes")
        
        if script:
            print(f"\n   📋 Action script ready for execution:")
            print(f"      ./run-action.sh {script}")
    else:
        print("\n   ❌ Changes discarded")
    
    # Step 8: Cleanup
    print("\n8️⃣  Cleaning up...")
    sandbox.cleanup()
    print("   ✅ Sandbox removed")
    
    # Step 9: Show logs
    if script:
        print("\n9️⃣  Audit trail...")
        print("   📋 Action log: .dev/logs/actions.log")
        print("   📋 Whitelist: .automation-whitelist.json")
    
    print("\n" + "="*60)
    print("✅ Workflow complete!\n")

def safe_refactoring_workflow():
    """Example: Safe refactoring with full safety measures."""
    
    print("🔧 Safe Refactoring Workflow\n")
    
    # High trust level in sandbox
    manager = TrustLevelManager(TrustLevel.FULL_AUTO)
    
    # Create sandbox
    sandbox = Sandbox()
    sandbox.create()
    sandbox.copy_project()
    
    print("Running refactoring in sandbox...")
    
    # Simulate refactoring operations
    # (In real use, this would be actual refactoring code)
    
    # Review changes
    changes = sandbox.diff()
    
    print(f"\nRefactoring complete:")
    print(f"  Modified: {len(changes['modified'])} files")
    
    # Generate action for applying changes
    runner = ActionRunner()
    script = runner.generate_action(
        description="Apply refactoring changes",
        commands=["echo 'Refactoring applied'"],
        files_affected=changes['modified'],
        reason="Code quality improvements"
    )
    
    print(f"\nAction script: {script}")
    print("Review and execute to apply changes")
    
    # Cleanup
    sandbox.cleanup()

if __name__ == '__main__':
    complete_workflow()
    
    # Uncomment to run refactoring example
    # safe_refactoring_workflow()
