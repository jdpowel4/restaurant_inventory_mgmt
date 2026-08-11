from inventory_app.shared.exceptions import InventoryAppError

class RecipeError(InventoryAppError):
    pass

class UnknownRecipeError(RecipeError):
    pass

class DuplicateRecipeComponentError(RecipeError):
    pass

class DuplicateRecipeError(RecipeError):
    pass