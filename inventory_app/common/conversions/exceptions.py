from shared.exceptions import InventoryAppError

class ConversionError(InventoryAppError):
    pass

class MissingIngredientConversion(ConversionError):
    def __init__(self, ingredient, from_unit, to_unit):
        self.ingredient = ingredient
        self.from_unit = from_unit
        self.to_unit = to_unit
        super().__init__(f"Missing conversion for ingredient {self.ingredient} {self.from_unit} -> {self.to_unit}")