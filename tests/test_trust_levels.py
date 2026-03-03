import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from kiro_automation import TrustLevel, TrustLevelManager

def test_trust_levels_exist():
    assert TrustLevel.READ_ONLY == 0
    assert TrustLevel.SAFE_CREATE == 1
    assert TrustLevel.MODIFY_WITH_BACKUP == 2
    assert TrustLevel.ACTION_SCRIPTS == 3
    assert TrustLevel.FULL_AUTO == 4

def test_manager_initialization():
    manager = TrustLevelManager(TrustLevel.READ_ONLY)
    assert manager.level == TrustLevel.READ_ONLY

def test_read_only_permissions():
    manager = TrustLevelManager(TrustLevel.READ_ONLY)
    assert manager.is_allowed('read_file')
    assert manager.is_allowed('list_dir')
    assert not manager.is_allowed('create_file')
    assert not manager.is_allowed('delete_file')

def test_safe_create_permissions():
    manager = TrustLevelManager(TrustLevel.SAFE_CREATE)
    assert manager.is_allowed('read_file')
    assert manager.is_allowed('create_file')
    assert not manager.is_allowed('modify_file')

def test_modify_with_backup_permissions():
    manager = TrustLevelManager(TrustLevel.MODIFY_WITH_BACKUP)
    assert manager.is_allowed('modify_file')
    assert not manager.is_allowed('delete_file')

def test_full_auto_permissions():
    manager = TrustLevelManager(TrustLevel.FULL_AUTO)
    assert manager.is_allowed('delete_file')
    assert manager.is_allowed('execute_action')

def test_require_level():
    manager = TrustLevelManager(TrustLevel.READ_ONLY)
    with pytest.raises(PermissionError):
        manager.require_level('delete', TrustLevel.FULL_AUTO)

def test_set_level():
    manager = TrustLevelManager(TrustLevel.READ_ONLY)
    manager.set_level(TrustLevel.FULL_AUTO)
    assert manager.level == TrustLevel.FULL_AUTO
    assert manager.is_allowed('delete_file')
