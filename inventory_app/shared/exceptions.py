class InventoryAppError(Exception):
    """Base exception for the entire app."""
    pass

class IngredientError(InventoryAppError):
    pass

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