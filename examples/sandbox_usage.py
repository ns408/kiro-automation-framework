"""
Example: Using sandbox mode for safe testing.

This example demonstrates how to use sandbox mode to test
automation before applying changes to the real project.
"""

from pathlib import Path
from kiro_automation import Sandbox, TrustLevel, TrustLevelManager


def main():
    print("🏖️  Sandbox Mode Example\n")

    # Create sandbox
    sandbox = Sandbox()
    sandbox_path = sandbox.create()
    print(f"✅ Sandbox created: {sandbox_path}")

    # Copy project (excluding large directories)
    print("\n📦 Copying project to sandbox...")
    sandbox.copy_project(
        exclude_patterns=[
            ".git",
            "__pycache__",
            ".venv",
            "venv",
            "node_modules",
            "dist",
            "build",
            ".dev",
        ]
    )
    print("✅ Project copied")

    # Simulate automation in sandbox
    print("\n🤖 Running automation in sandbox...")

    # Create a test file in sandbox
    test_file = sandbox.get_path("test_automation.txt")
    test_file.write_text("This file was created by automation in sandbox")
    print(f"  Created: {test_file.name}")

    # Modify an existing file (if it exists)
    readme = sandbox.get_path("README.md")
    if readme.exists():
        content = readme.read_text()
        readme.write_text(
            content + "\n\n## Automation Test\nThis was added in sandbox.\n"
        )
        print(f"  Modified: {readme.name}")

    # Review changes
    print("\n📊 Reviewing changes...")
    changes = sandbox.diff()

    print(f"\n  Added files: {len(changes['added'])}")
    for file in changes["added"]:
        print(f"    + {file}")

    print(f"\n  Modified files: {len(changes['modified'])}")
    for file in changes["modified"]:
        print(f"    ~ {file}")

    print(f"\n  Deleted files: {len(changes['deleted'])}")
    for file in changes["deleted"]:
        print(f"    - {file}")

    # Ask user to apply changes
    print("\n" + "=" * 50)
    response = input("Apply changes to real project? (yes/no): ")

    if response.lower() == "yes":
        print("\n✅ Applying changes...")
        applied = sandbox.apply_changes()
        print(f"  Added: {len(applied['added'])} files")
        print(f"  Modified: {len(applied['modified'])} files")
        print(f"  Deleted: {len(applied['deleted'])} files")
    else:
        print("\n❌ Changes discarded")

    # Cleanup sandbox
    print("\n🧹 Cleaning up sandbox...")
    sandbox.cleanup()
    print("✅ Sandbox removed")


def advanced_example():
    """Example with higher trust level in sandbox."""
    print("\n🔬 Advanced Sandbox Example\n")

    sandbox = Sandbox()
    sandbox.create()
    sandbox.copy_project()

    # Use high trust level in sandbox (safe because isolated)
    manager = TrustLevelManager(TrustLevel.FULL_AUTO)
    print(f"Trust level in sandbox: {manager.level.name}")

    # Run multiple iterations
    print("\n🔄 Running iterative automation...")
    for i in range(3):
        print(f"\n  Iteration {i+1}:")

        # Simulate automation operations
        test_file = sandbox.get_path(f"iteration_{i+1}.txt")
        test_file.write_text(f"Iteration {i+1} output")
        print(f"    Created: {test_file.name}")

    # Review all changes
    changes = sandbox.diff()
    print(f"\n📊 Total changes: {len(changes['added'])} files added")

    # Apply if satisfied
    if len(changes["added"]) == 3:
        print("\n✅ All iterations successful, applying changes...")
        sandbox.apply_changes()
    else:
        print("\n❌ Unexpected results, discarding...")

    sandbox.cleanup()


if __name__ == "__main__":
    main()

    # Uncomment to run advanced example
    # advanced_example()
