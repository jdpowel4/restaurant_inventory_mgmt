from inventory_app.shared.exceptions import InventoryAppError

class IngredientError(InventoryAppError):
    pass

class IngredientCostingError(IngredientError):
    pass

class NoCostDataError(IngredientCostingError):
    pass

class DuplicateIngredientError(IngredientError):
    pass

class UnknownCategoryError(IngredientError):
    pass

class UnknownSubcategoryError(IngredientError):
    pass

class UnknownIngredientError(IngredientError):
    pass
