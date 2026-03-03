import pytest
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from kiro_automation import (
    TrustLevel, TrustLevelManager,
    OperationWhitelist, Sandbox, ActionRunner
)

def test_full_workflow_with_sandbox():
    """Integration test: Complete workflow with sandbox."""
    # Setup
    manager = TrustLevelManager(TrustLevel.ACTION_SCRIPTS)
    whitelist = OperationWhitelist()
    sandbox = Sandbox()
    
    # Create sandbox
    sandbox_path = sandbox.create()
    assert sandbox_path.exists()
    
    # Create test file in sandbox
    test_file = sandbox.get_path('test.txt')
    test_file.write_text('test content')
    
    # Check changes
    changes = sandbox.diff()
    assert 'test.txt' in changes['added']
    
    # Cleanup
    sandbox.cleanup()
    assert not sandbox_path.exists()

def test_trust_level_with_whitelist():
    """Integration test: Trust levels with whitelist."""
    temp_dir = Path(tempfile.mkdtemp())
    config_path = temp_dir / 'whitelist.json'
    
    manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)
    whitelist = OperationWhitelist(config_path=config_path)
    
    # Configure whitelist
    whitelist.add_operation('modify_file', auto_approve=False)
    whitelist.add_path(str(temp_dir))
    whitelist.save()
    
    # Test combined permissions
    assert manager.is_allowed('modify_file')
    assert whitelist.is_operation_allowed('modify_file')
    assert whitelist.is_path_allowed(str(temp_dir / 'test.txt'))
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)

def test_action_runner_with_sandbox():
    """Integration test: Action runner in sandbox."""
    temp_dir = Path(tempfile.mkdtemp())
    
    sandbox = Sandbox()
    sandbox.create()
    
    runner = ActionRunner(actions_dir=temp_dir / 'actions')
    
    # Generate action
    script = runner.generate_action(
        description="Test action",
        commands=["echo 'test'"],
        files_affected=[],
        reason="Integration test"
    )
    
    assert script.exists()
    
    # Dry run
    result = runner.execute_action(script, dry_run=True)
    assert result['status'] == 'dry_run'
    
    # Cleanup
    sandbox.cleanup()
    import shutil
    shutil.rmtree(temp_dir)

def test_complete_safety_workflow():
    """Integration test: All safety layers together."""
    temp_dir = Path(tempfile.mkdtemp())
    
    # Layer 1: Trust level
    manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)
    
    # Layer 2: Whitelist
    whitelist = OperationWhitelist(config_path=temp_dir / 'whitelist.json')
    whitelist.add_operation('modify_file')
    whitelist.add_path(str(temp_dir))
    
    # Layer 3: Sandbox
    sandbox = Sandbox(base_path=temp_dir)
    sandbox_path = sandbox.create()
    
    # Layer 4: Action runner
    runner = ActionRunner(actions_dir=temp_dir / 'actions')
    
    # Verify all layers work together
    assert manager.is_allowed('modify_file')
    assert whitelist.is_operation_allowed('modify_file')
    assert sandbox.is_active
    assert runner.actions_dir.parent == temp_dir
    
    # Cleanup
    sandbox.cleanup()
    import shutil
    shutil.rmtree(temp_dir)
