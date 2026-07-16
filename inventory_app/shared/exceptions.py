class InventoryAppError(Exception):
    """Base exception for the entire app."""
    pass

class IngredientError(InventoryAppError):
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

class RecipeError(InventoryAppError):
    pass

class ValidationError(InventoryAppError):
    pass

class NotFoundError(InventoryAppError):
    pass

class DuplicateConversionError(InventoryAppError):
    """Raised when an ingredient conversion already exists."""
    pass

class DuplicateIngredientError(IngredientError):
    pass

class UnknownCategoryError(IngredientError):
    pass

class UnknownSubcategoryError(IngredientError):
    pass

class UnknownUnitError(UnitError):
    pass

class UnknownIngredientError(IngredientError):
    pass

class UnknownRecipeError(RecipeError):
    pass

class DuplicateRecipeComponentError(RecipeError):
    pass