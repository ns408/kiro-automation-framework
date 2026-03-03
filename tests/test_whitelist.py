import pytest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kiro_automation import OperationWhitelist


@pytest.fixture
def temp_config():
    temp_dir = Path(tempfile.mkdtemp())
    config_path = temp_dir / "whitelist.json"
    yield config_path
    import shutil

    shutil.rmtree(temp_dir)


def test_whitelist_initialization(temp_config):
    whitelist = OperationWhitelist(config_path=temp_config)
    assert len(whitelist.allowed_operations) == 0


def test_add_operation(temp_config):
    whitelist = OperationWhitelist(config_path=temp_config)
    whitelist.add_operation("read_file", auto_approve=True)
    assert whitelist.is_operation_allowed("read_file")
    assert not whitelist.requires_approval("read_file")


def test_path_allowed(temp_config):
    whitelist = OperationWhitelist(config_path=temp_config)
    whitelist.add_path("/tmp/test")
    assert whitelist.is_path_allowed("/tmp/test/file.txt")


def test_path_blocked(temp_config):
    whitelist = OperationWhitelist(config_path=temp_config)
    whitelist.add_path("/tmp/test")
    whitelist.block_path("/tmp/test/secret.txt")
    assert not whitelist.is_path_allowed("/tmp/test/secret.txt")


def test_save_and_load(temp_config):
    whitelist = OperationWhitelist(config_path=temp_config)
    whitelist.add_operation("read_file")
    whitelist.save()

    whitelist2 = OperationWhitelist(config_path=temp_config)
    assert whitelist2.is_operation_allowed("read_file")
