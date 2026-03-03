import pytest
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from kiro_automation import Sandbox

def test_sandbox_creation():
    sandbox = Sandbox()
    path = sandbox.create()
    assert path.exists()
    assert sandbox.is_active
    sandbox.cleanup()

def test_sandbox_file_operations():
    sandbox = Sandbox()
    sandbox.create()
    
    test_file = sandbox.get_path('test.txt')
    test_file.write_text('content')
    assert test_file.exists()
    
    sandbox.cleanup()

def test_sandbox_diff():
    sandbox = Sandbox()
    sandbox.create()
    
    test_file = sandbox.get_path('new_file.txt')
    test_file.write_text('content')
    
    changes = sandbox.diff()
    assert 'new_file.txt' in changes['added']
    
    sandbox.cleanup()

def test_sandbox_cleanup():
    sandbox = Sandbox()
    path = sandbox.create()
    sandbox.cleanup()
    assert not path.exists()
    assert not sandbox.is_active
