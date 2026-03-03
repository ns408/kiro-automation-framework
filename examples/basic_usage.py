"""
Example: Basic usage of trust levels and whitelist.

This example shows how to set up trust levels and whitelist
for safe automation.
"""

from pathlib import Path
from kiro_automation import TrustLevel, TrustLevelManager, OperationWhitelist


def main():
    # Initialize trust level manager
    manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)
    print(f"Trust level: {manager.level.name}")

    # Check allowed operations
    operations = ["read_file", "create_file", "modify_file", "delete_file"]
    print("\nAllowed operations:")
    for op in operations:
        allowed = manager.is_allowed(op)
        status = "✅" if allowed else "❌"
        print(f"  {status} {op}")

    # Set up whitelist
    whitelist = OperationWhitelist()

    # Add allowed operations
    whitelist.add_operation("read_file", auto_approve=True)
    whitelist.add_operation("create_file", auto_approve=True)
    whitelist.add_operation("modify_file", auto_approve=False)

    # Add allowed paths
    project_root = Path.cwd()
    whitelist.add_path(str(project_root / "src"))
    whitelist.add_path(str(project_root / "tests"))

    # Block sensitive paths
    whitelist.block_path(str(project_root / "src" / "secrets.py"))

    # Save whitelist
    whitelist.save()
    print("\n✅ Whitelist saved to .automation-whitelist.json")

    # Test path access
    test_paths = ["src/main.py", "src/secrets.py", "config/settings.py"]

    print("\nPath access:")
    for path in test_paths:
        full_path = project_root / path
        allowed = whitelist.is_path_allowed(str(full_path))
        status = "✅" if allowed else "❌"
        print(f"  {status} {path}")

    # Combined check
    def can_perform(operation: str, path: str) -> bool:
        """Check if operation is allowed by both trust level and whitelist."""
        return (
            manager.is_allowed(operation)
            and whitelist.is_operation_allowed(operation)
            and whitelist.is_path_allowed(path)
        )

    print("\nCombined checks:")
    checks = [
        ("modify_file", str(project_root / "src" / "main.py")),
        ("modify_file", str(project_root / "src" / "secrets.py")),
        ("delete_file", str(project_root / "src" / "main.py")),
    ]

    for op, path in checks:
        allowed = can_perform(op, path)
        status = "✅" if allowed else "❌"
        print(f"  {status} {op} on {Path(path).relative_to(project_root)}")


if __name__ == "__main__":
    main()
