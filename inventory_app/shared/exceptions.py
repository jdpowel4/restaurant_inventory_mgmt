class InventoryAppError(Exception):
    """Base exception for the entire app."""
    pass

class ValidationError(InventoryAppError):
    pass

class NotFoundError(InventoryAppError):
    pass

class DuplicateConversionError(InventoryAppError):
    """Raised when an ingredient conversion already exists."""
    pass