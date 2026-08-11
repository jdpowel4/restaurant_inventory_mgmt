from inventory_app.shared.exceptions import InventoryAppError

class ItemError(InventoryAppError):
    pass

class UnknownItemError(ItemError):
    pass