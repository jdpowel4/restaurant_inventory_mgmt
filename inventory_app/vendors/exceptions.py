from inventory_app.shared.exceptions import InventoryAppError

class VendorError(InventoryAppError):
    pass

class VendorItemError(VendorError):
    pass

class MissingVendorItemError(VendorItemError):
    pass
