from inventory_app.shared.exceptions import InventoryAppError

class ConversionError(InventoryAppError):
    pass

class MissingConversionError(ConversionError):
    pass

class AmbiguousConversionError(ConversionError):
    pass

class CircularConversionError(ConversionError):
    pass

class InvalidConversionError(ConversionError):
    pass