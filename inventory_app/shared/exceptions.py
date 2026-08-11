class InventoryAppError(Exception):
    """Base exception for the entire app."""
    pass

class ConversionError(InventoryAppError):
    pass

class MissingIngredientConversion(ConversionError):
    def __init__(self, ingredient, from_unit, to_unit):
        self.ingredient = ingredient
        self.from_unit = from_unit
        self.to_unit = to_unit
        super().__init__(f"Missing conversion for ingredient {self.ingredient} {self.from_unit} -> {self.to_unit}")

class UnitError(InventoryAppError):
    pass

class ValidationError(InventoryAppError):
    pass

class NotFoundError(InventoryAppError):
    pass

class DuplicateConversionError(InventoryAppError):
    """Raised when an ingredient conversion already exists."""
    pass

class UnknownUnitError(UnitError):
    pass

class BusinessError(InventoryAppError):
    pass