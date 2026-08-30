from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidgetItem,
    QDialog
)

from inventory_app.app.app_context import AppContext
from inventory_app.recipes.gui.recipe_editor import RecipeEditor
from inventory_app.recipes.services.recipe_service import RecipeService

class RecipePage(QWidget):

    def __init__(self, context: AppContext):
        super().__init__()

        self.context = context

        self.setWindowTitle("Recipes")

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search Recipes..."
        )

        self.recipe_list = QListWidget()

        self.selected_label = QLabel(
            "Selected: None"
        )

        self.add_button = QPushButton(
            "Add Recipe"
        )

        layout = QVBoxLayout()

        layout.addWidget(
            self.search_box
        )
        layout.addWidget(
            self.recipe_list
        )
        layout.addWidget(
            self.selected_label
        )
        layout.addWidget(
            self.add_button
        )

        self.setLayout(layout)

        self.search_box.textChanged.connect(
            self._search_recipes
        )
        
        self.recipe_list.itemSelectionChanged.connect(
            self._recipe_selected
        )
        
        self.recipe_list.itemDoubleClicked.connect(
            self._recipe_double_clicked
        )
        
        self._load_recipes()

    def _load_recipes(self):

        with self.context.session_factory() as session:

            recipe_service = RecipeService(session)
            recipes = recipe_service.get_all()

            self.recipe_list.clear()

            for recipe in recipes:
                item = QListWidgetItem(recipe.item.name)
                item.setData(Qt.ItemDataRole.UserRole, recipe.id)
                self.recipe_list.addItem(item)
    
    def _search_recipes(self, search_text: str):

        search_text = search_text.lower()

        for index in range(
            self.recipe_list.count()
        ):
            item = self.recipe_list.item(index)

            matches = (
                search_text
                in item.text().lower()
            )

            item.setHidden(
                not matches
            )

    def _recipe_selected(self):

        selected = (
            self.recipe_list.selectedItems()
        )

        if not selected:
            self.selected_label.setText(
                "Selected: None"
            )
            return
        
        recipe = selected[0]

        self.selected_label.setText(
            f"Selected: {recipe.text()}"
        )

    def _recipe_double_clicked(self, item: QListWidgetItem):

        recipe_id = item.data(Qt.ItemDataRole.UserRole)

        if recipe_id is None:
            return
        
        editor = RecipeEditor(
            context=self.context,
            recipe_id=recipe_id
        )

        if editor.exec() == QDialog.DialogCode.Accepted:
            self._load_recipes()