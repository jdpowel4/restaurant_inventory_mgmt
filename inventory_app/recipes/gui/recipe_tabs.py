from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from inventory_app.app.app_context import AppContext
from inventory_app.recipes.gui.widgets.recipe_component_editor_table import RecipeComponentTable
from inventory_app.recipes.dto import RecipeComponentInput
from inventory_app.recipes.models import Recipe


class RecipeTab(QWidget):

    def __init__(
            self,
            context: AppContext,
            recipe_id: int | None = None,
            parent: QWidget | None = None
        ):
        super().__init__(parent)

        self.context = context
        self.recipe_id = recipe_id 

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        self.component_table = RecipeComponentTable(
            self.context,
            self.recipe_id
        )

        layout.addWidget(self.component_table)

    def load_recipe(self, recipe: Recipe):
        self.component_table.load_components(recipe.components)

    def get_components(self):
        return self.component_table.get_components()
