import pytest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kiro_automation import ActionRunner


@pytest.fixture
def temp_runner():
    temp_dir = Path(tempfile.mkdtemp())
    runner = ActionRunner(actions_dir=temp_dir / "actions")
    yield runner
    import shutil

    shutil.rmtree(temp_dir)


def test_generate_action(temp_runner):
    script = temp_runner.generate_action(
        description="Test action",
        commands=["echo 'test'"],
        files_affected=["test.txt"],
        reason="Testing",
    )
    assert script.exists()
    assert script.suffix == ".sh"


def test_action_executable(temp_runner):
    script = temp_runner.generate_action(
        description="Test", commands=["echo 'test'"], files_affected=[], reason="Test"
    )
    assert script.stat().st_mode & 0o111


def test_dry_run(temp_runner):
    script = temp_runner.generate_action(
        description="Test", commands=["echo 'test'"], files_affected=[], reason="Test"
    )
    result = temp_runner.execute_action(script, dry_run=True)
    assert result["status"] == "dry_run"


def test_list_actions(temp_runner):
    temp_runner.generate_action("Test 1", ["echo 1"], [], "Test")
    temp_runner.generate_action("Test 2", ["echo 2"], [], "Test")
    actions = temp_runner.list_actions()
    assert len(actions) == 2
