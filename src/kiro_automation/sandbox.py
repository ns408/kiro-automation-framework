"""Sandbox mode for safe testing."""

from pathlib import Path
from typing import Optional
import shutil
import tempfile


class Sandbox:
    """Isolated environment for testing automation."""

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path.cwd()
        self.sandbox_dir: Optional[Path] = None
        self.is_active = False

    def create(self) -> Path:
        """Create sandbox directory."""
        self.sandbox_dir = Path(tempfile.mkdtemp(prefix="kiro_sandbox_"))
        self.is_active = True
        return self.sandbox_dir

    def copy_project(self, exclude_patterns: Optional[list] = None):
        """Copy project files to sandbox."""
        if not self.sandbox_dir:
            raise RuntimeError("Sandbox not created")

        exclude = exclude_patterns or [".git", "__pycache__", ".venv", "venv", ".dev"]

        for item in self.base_path.iterdir():
            if item.name in exclude:
                continue

            dest = self.sandbox_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest, ignore=shutil.ignore_patterns(*exclude))
            else:
                shutil.copy2(item, dest)

    def cleanup(self):
        """Remove sandbox directory."""
        if self.sandbox_dir and self.sandbox_dir.exists():
            shutil.rmtree(self.sandbox_dir)
            self.is_active = False

    def get_path(self, relative_path: str) -> Path:
        """Get absolute path within sandbox."""
        if not self.sandbox_dir:
            raise RuntimeError("Sandbox not created")
        return self.sandbox_dir / relative_path

    def diff(self) -> dict:
        """Compare sandbox with original project."""
        if not self.sandbox_dir:
            raise RuntimeError("Sandbox not created")

        changes = {"added": [], "modified": [], "deleted": []}

        # Find added and modified files
        for item in self.sandbox_dir.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(self.sandbox_dir)
                original = self.base_path / rel_path

                if not original.exists():
                    changes["added"].append(str(rel_path))
                elif item.read_bytes() != original.read_bytes():
                    changes["modified"].append(str(rel_path))

        # Find deleted files
        for item in self.base_path.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(self.base_path)
                sandbox_file = self.sandbox_dir / rel_path

                if not sandbox_file.exists():
                    changes["deleted"].append(str(rel_path))

        return changes

    def apply_changes(self):
        """Apply sandbox changes to original project."""
        if not self.sandbox_dir:
            raise RuntimeError("Sandbox not created")

        changes = self.diff()

        # Apply added and modified files
        for file_path in changes["added"] + changes["modified"]:
            src = self.sandbox_dir / file_path
            dest = self.base_path / file_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)

        # Handle deleted files
        for file_path in changes["deleted"]:
            (self.base_path / file_path).unlink()

        return changes
