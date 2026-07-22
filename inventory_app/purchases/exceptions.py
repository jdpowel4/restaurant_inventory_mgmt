from inventory_app.shared.exceptions import InventoryAppError

class PurchaseError(InventoryAppError):
    pass

class ImportError(PurchaseError):
    pass

class UnknownFileTypeError(ImportError):
    pass

class UnknownVendorError(ImportError):
    pass