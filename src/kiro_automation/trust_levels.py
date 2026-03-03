"""Trust level system for safe AI automation."""
from enum import IntEnum
from typing import Set
from .logger import get_logger

class TrustLevel(IntEnum):
    """Trust levels for automation control."""
    READ_ONLY = 0
    SAFE_CREATE = 1
    MODIFY_WITH_BACKUP = 2
    ACTION_SCRIPTS = 3
    FULL_AUTO = 4

class TrustLevelManager:
    """Manages trust level enforcement."""
    
    def __init__(self, level: TrustLevel = TrustLevel.READ_ONLY):
        self.level = level
        self._allowed_operations = self._compute_allowed_operations()
        self.logger = get_logger()
        self.logger.info("TrustLevelManager initialized", level=level.name)
    
    def _compute_allowed_operations(self) -> Set[str]:
        """Compute allowed operations based on trust level."""
        ops = set()
        
        # Level 0: Read-only
        if self.level >= TrustLevel.READ_ONLY:
            ops.update(['read_file', 'list_dir', 'search', 'grep'])
        
        # Level 1: Safe creation
        if self.level >= TrustLevel.SAFE_CREATE:
            ops.update(['create_file', 'mkdir'])
        
        # Level 2: Modifications with backup
        if self.level >= TrustLevel.MODIFY_WITH_BACKUP:
            ops.update(['modify_file', 'append_file'])
        
        # Level 3: Action scripts
        if self.level >= TrustLevel.ACTION_SCRIPTS:
            ops.update(['generate_action', 'write_action'])
        
        # Level 4: Full automation
        if self.level >= TrustLevel.FULL_AUTO:
            ops.update(['execute_action', 'delete_file', 'move_file'])
        
        return ops
    
    def is_allowed(self, operation: str) -> bool:
        """Check if operation is allowed at current trust level."""
        return operation in self._allowed_operations
    
    def require_level(self, operation: str, required_level: TrustLevel):
        """Raise exception if trust level insufficient."""
        if self.level < required_level:
            self.logger.warning("Permission denied", operation=operation, 
                              required=required_level.name, current=self.level.name)
            raise PermissionError(
                f"Operation '{operation}' requires trust level {required_level.name} "
                f"(current: {self.level.name})"
            )
    
    def set_level(self, level: TrustLevel):
        """Change trust level."""
        old_level = self.level.name
        self.level = level
        self._allowed_operations = self._compute_allowed_operations()
        self.logger.info("Trust level changed", old=old_level, new=level.name)
