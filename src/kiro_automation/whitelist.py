"""Operation whitelist for fine-grained control."""
from typing import Set, Dict, Optional
from pathlib import Path
import json

class OperationWhitelist:
    """Manages whitelisted operations and paths."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path(".automation-whitelist.json")
        self.allowed_operations: Set[str] = set()
        self.allowed_paths: Set[str] = set()
        self.blocked_paths: Set[str] = set()
        self.auto_approve: Set[str] = set()
        
        if self.config_path.exists():
            self.load()
    
    def load(self):
        """Load whitelist from config file."""
        with open(self.config_path) as f:
            config = json.load(f)
        
        self.allowed_operations = set(config.get('allowed_operations', []))
        self.allowed_paths = set(config.get('allowed_paths', []))
        self.blocked_paths = set(config.get('blocked_paths', []))
        self.auto_approve = set(config.get('auto_approve', []))
    
    def save(self):
        """Save whitelist to config file."""
        config = {
            'allowed_operations': list(self.allowed_operations),
            'allowed_paths': list(self.allowed_paths),
            'blocked_paths': list(self.blocked_paths),
            'auto_approve': list(self.auto_approve)
        }
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def is_operation_allowed(self, operation: str) -> bool:
        """Check if operation is whitelisted."""
        return operation in self.allowed_operations
    
    def is_path_allowed(self, path: str) -> bool:
        """Check if path is allowed and not blocked."""
        path_obj = Path(path).resolve()
        
        # Check blocked paths first
        for blocked in self.blocked_paths:
            if str(path_obj).startswith(blocked):
                return False
        
        # Check allowed paths
        if not self.allowed_paths:
            return True  # No restrictions if empty
        
        for allowed in self.allowed_paths:
            if str(path_obj).startswith(allowed):
                return True
        
        return False
    
    def requires_approval(self, operation: str) -> bool:
        """Check if operation requires manual approval."""
        return operation not in self.auto_approve
    
    def add_operation(self, operation: str, auto_approve: bool = False):
        """Add operation to whitelist."""
        self.allowed_operations.add(operation)
        if auto_approve:
            self.auto_approve.add(operation)
    
    def add_path(self, path: str):
        """Add path to allowed paths."""
        self.allowed_paths.add(str(Path(path).resolve()))
    
    def block_path(self, path: str):
        """Add path to blocked paths."""
        self.blocked_paths.add(str(Path(path).resolve()))
