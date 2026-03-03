"""Action script generation and execution."""

from pathlib import Path
from datetime import datetime
from typing import Optional
import subprocess


class ActionRunner:
    """Manages action script lifecycle."""

    def __init__(self, actions_dir: Path = Path(".dev/actions")):
        self.actions_dir = actions_dir
        self.actions_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = Path(".dev/logs/actions.log")
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

    def generate_action(
        self, description: str, commands: list, files_affected: list, reason: str
    ) -> Path:
        """Generate action script."""
        # Find next action number
        existing = list(self.actions_dir.glob("*.sh"))
        next_num = len(existing) + 1

        # Create filename
        safe_desc = description.lower().replace(" ", "-")[:40]
        filename = f"{next_num:03d}-{safe_desc}.sh"
        script_path = self.actions_dir / filename

        # Generate script content
        script = f"""#!/bin/bash
# ACTION: {description}
# REASON: {reason}
# FILES: {', '.join(files_affected)}
# CREATED: {datetime.now().strftime('%Y-%m-%d')}

set -e

echo "ACTION: {description}"
echo ""
echo "This will:"
"""

        for i, cmd in enumerate(commands, 1):
            script += f'echo "  {i}. {cmd}"\n'

        script += 'echo ""\n\n'

        # Add backup logic if modifying files
        if files_affected:
            script += "# Backup files before modifying\n"
            for file in files_affected:
                script += f'[ -f "{file}" ] && cp "{file}" "{file}.backup"\n'
            script += "\n"

        # Add commands
        for cmd in commands:
            script += f"{cmd}\n"

        script += '\necho "Action complete!"\n'

        # Write script
        script_path.write_text(script)
        script_path.chmod(0o755)

        return script_path

    def execute_action(self, script_path: Path, dry_run: bool = False) -> dict:
        """Execute action script with logging."""
        timestamp = datetime.now().isoformat()

        # Log execution start
        with open(self.log_file, "a") as f:
            f.write(f"{timestamp} | ACTION: {script_path.name}\n")
            f.write(f"{timestamp} | EXECUTING: {script_path}\n")

        if dry_run:
            with open(self.log_file, "a") as f:
                f.write(f"{timestamp} | STATUS: [DRY RUN] (not executed)\n")
                f.write("---\n")
            return {"status": "dry_run", "output": "Dry run - not executed"}

        try:
            result = subprocess.run(
                ["bash", str(script_path)], capture_output=True, text=True, check=True
            )

            with open(self.log_file, "a") as f:
                f.write(result.stdout)
                f.write(f"{timestamp} | STATUS: [SUCCESS]\n")
                f.write("---\n")

            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr,
            }

        except subprocess.CalledProcessError as e:
            with open(self.log_file, "a") as f:
                f.write(f"{timestamp} | STATUS: [FAILED]\n")
                f.write(f"{timestamp} | ERROR: {e.stderr}\n")
                f.write("---\n")

            return {"status": "failed", "output": e.stdout, "error": e.stderr}

    def list_actions(self) -> list:
        """List all action scripts."""
        return sorted(self.actions_dir.glob("*.sh"))

    def get_log(self, lines: Optional[int] = None) -> str:
        """Get action execution log."""
        if not self.log_file.exists():
            return "No actions executed yet"

        content = self.log_file.read_text()
        if lines:
            return "\n".join(content.split("\n")[-lines:])
        return content
