from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidgetItem,
    QDialog
)

from inventory_app.shared.db import session_scope
from inventory_app.ingredients.services.ingredient_service import IngredientService

from inventory_app.app.app_context import AppContext
from inventory_app.ingredients.gui.ingredient_editor import IngredientEditor


class IngredientPage(QWidget):

    def __init__(self, context: AppContext):
        super().__init__()

        self.context = context

        self.setWindowTitle("Ingredients")

        # ---------------
        # Search Box
        # ---------------
        #
        # The user types here to narrow the ingredient list.
        #
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search Ingredients..."
        )

        # ---------------
        # Ingredient List
        # ---------------
        #
        #QListWidget provides:
        #
        #  - one row per ingredient
        #  - mouse selection
        #  - keyboard navigation
        #  - build-in highlighting
        #
        self.ingredient_list = QListWidget()

        # --------------
        # Selected Ingredient Label
        # --------------
        #
        # Temporary: Later could be replaces with ingredient detail panel or 
        # editor
        #
        self.selected_label = QLabel(
            "Selected: None"
        )

        # ---------------
        # Buttons
        # ---------------
        
        self.new_button = QPushButton(
            "New Ingredient"
        )

        self.close_button = QPushButton(
            "Close"
        )

        # ---------------
        # Layout
        # ---------------

        layout = QVBoxLayout()

        layout.addWidget(
            self.search_box
        )

        layout.addWidget(
            self.ingredient_list
        )

        layout.addWidget(
            self.selected_label
        )

        layout.addWidget(
            self.new_button
        )

        layout.addWidget(
            self.close_button
        )

        self.setLayout(layout)

        # ---------------
        # Signals
        # ---------------
        
        self.search_box.textChanged.connect(
            self.search_ingredients
        )
        
        self.ingredient_list.itemSelectionChanged.connect(
            self.ingredient_selected
        )

        self.ingredient_list.itemDoubleClicked.connect(
            self.ingredient_double_clicked
        )
        
        self.close_button.clicked.connect(
            self.close
        )
        
        # ---------------
        # Ingredients
        # ---------------

        self.load_ingredients()
    
    def load_ingredients(self):
        """
        Load ingredients into the list.
        """
        with session_scope() as session:

            ingredient_service = IngredientService(session)
            ingredients = ingredient_service.get_all()

            self.ingredient_list.clear()

            for ingredient in ingredients:
                item = QListWidgetItem(ingredient.item.name)
                item.setData(Qt.ItemDataRole.UserRole, ingredient.id)
                self.ingredient_list.addItem(item)

    def search_ingredients(self, search_text: str):
        """
        Filter the ingredients displayed

        The search is case-insensitive
        """
        
        search_text = search_text.lower()

        for index in range(
            self.ingredient_list.count()
        ):
            item = self.ingredient_list.item(index)

            matches = (
                search_text
                in item.text().lower()
            )

            item.setHidden(
                not matches
            )

    def ingredient_selected(self):
        """
        Respond when the user selects an ingredient.
        """

        selected = (
            self.ingredient_list.selectedItems()
        )

        if not selected:
            self.selected_label.setText(
                "Selected: None"
            )
            return
        
        ingredient = selected[0]

        self.selected_label.setText(
            f"Selected: {ingredient.text()}"
        )

    def ingredient_double_clicked(self, item: QListWidgetItem):
        
        ingredient_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if ingredient_id is None:
            return
        
        editor = IngredientEditor(
            ingredient_id=ingredient_id,
            parent=self
        )

        if editor.exec() == QDialog.DialogCode.Accepted:
            self.load_ingredients()