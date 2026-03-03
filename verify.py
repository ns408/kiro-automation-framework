#!/usr/bin/env python3
"""
Quick verification test for Kiro Automation Framework.
Run this to verify the framework is working correctly.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from kiro_automation import (
            TrustLevel,
            TrustLevelManager,
            OperationWhitelist,
            Sandbox,
            ActionRunner
        )
        print("  [OK] All imports successful")
        return True
    except ImportError as e:
        print(f"  [FAIL] Import failed: {e}")
        return False

def test_trust_levels():
    """Test trust level system."""
    print("\nTesting trust levels...")
    try:
        from kiro_automation import TrustLevel, TrustLevelManager
        
        # Test each level
        for level in TrustLevel:
            manager = TrustLevelManager(level)
            assert manager.level == level
        
        # Test permissions
        manager = TrustLevelManager(TrustLevel.READ_ONLY)
        assert manager.is_allowed('read_file')
        assert not manager.is_allowed('delete_file')
        
        manager = TrustLevelManager(TrustLevel.FULL_AUTO)
        assert manager.is_allowed('delete_file')
        
        print("  [OK] Trust levels working")
        return True
    except Exception as e:
        print(f"  [FAIL] Trust levels failed: {e}")
        return False

def test_whitelist():
    """Test whitelist system."""
    print("\nTesting whitelist...")
    try:
        from kiro_automation import OperationWhitelist
        import tempfile
        
        # Create temporary config path (file doesn't exist yet)
        temp_dir = Path(tempfile.mkdtemp())
        config_path = temp_dir / 'whitelist.json'
        
        whitelist = OperationWhitelist(config_path=config_path)
        
        # Test operations
        whitelist.add_operation('read_file', auto_approve=True)
        assert whitelist.is_operation_allowed('read_file')
        assert not whitelist.requires_approval('read_file')
        
        # Test paths
        whitelist.add_path('/tmp/test')
        assert whitelist.is_path_allowed('/tmp/test/file.txt')
        
        whitelist.block_path('/tmp/test/secret.txt')
        assert not whitelist.is_path_allowed('/tmp/test/secret.txt')
        
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)
        
        print("  [OK] Whitelist working")
        return True
    except Exception as e:
        print(f"  [FAIL] Whitelist failed: {e}")
        return False

def test_sandbox():
    """Test sandbox system."""
    print("\nTesting sandbox...")
    try:
        from kiro_automation import Sandbox
        
        sandbox = Sandbox()
        sandbox_path = sandbox.create()
        
        assert sandbox_path.exists()
        assert sandbox.is_active
        
        # Test file operations
        test_file = sandbox.get_path('test.txt')
        test_file.write_text('test content')
        assert test_file.exists()
        
        # Test diff
        changes = sandbox.diff()
        assert 'test.txt' in changes['added']
        
        # Cleanup
        sandbox.cleanup()
        assert not sandbox_path.exists()
        
        print("  [OK] Sandbox working")
        return True
    except Exception as e:
        print(f"  [FAIL] Sandbox failed: {e}")
        return False

def test_action_runner():
    """Test action runner system."""
    print("\nTesting action runner...")
    try:
        from kiro_automation import ActionRunner
        import tempfile
        import shutil
        
        # Create temporary actions directory
        temp_dir = Path(tempfile.mkdtemp())
        actions_dir = temp_dir / 'actions'
        actions_dir.mkdir()
        
        runner = ActionRunner(actions_dir=actions_dir)
        
        # Generate action
        script = runner.generate_action(
            description="Test action",
            commands=["echo 'test'"],
            files_affected=["test.txt"],
            reason="Testing"
        )
        
        assert script.exists()
        assert script.is_file()
        assert script.stat().st_mode & 0o111  # Executable
        
        # Test dry run
        result = runner.execute_action(script, dry_run=True)
        assert result['status'] == 'dry_run'
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        print("  [OK] Action runner working")
        return True
    except Exception as e:
        print(f"  [FAIL] Action runner failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("Kiro Automation Framework - Verification Test")
    print("="*60)
    
    results = []
    
    results.append(test_imports())
    results.append(test_trust_levels())
    results.append(test_whitelist())
    results.append(test_sandbox())
    results.append(test_action_runner())
    
    print("\n" + "="*60)
    
    if all(results):
        print("[SUCCESS] All tests passed!")
        print("\nFramework is ready to use.")
        print("\nNext steps:")
        print("  1. Read QUICKSTART.md")
        print("  2. Try examples in examples/")
        print("  3. Read docs in docs/")
        return 0
    else:
        print("[FAILED] Some tests failed")
        print("\nPlease check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
