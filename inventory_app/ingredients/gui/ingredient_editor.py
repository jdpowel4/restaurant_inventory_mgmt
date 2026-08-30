from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)

from inventory_app.shared.db import session_scope
from inventory_app.ingredients.models import Ingredient
from inventory_app.ingredients.services.ingredient_service import IngredientService
from inventory_app.ingredients.services.category_service import IngredientCategoryService
from inventory_app.ingredients.services.subcategory_service import IngredientSubcategoryService
from inventory_app.ingredients.dto import IngredientUpdate
from inventory_app.inventory.services.location_service import InventoryLocationService
from inventory_app.units.services.unit_service import UnitService

class IngredientEditor(QDialog):

    def __init__(self, ingredient_id: int, parent):
        super().__init__(parent)

        self.ingredient_title: str
        self.ingredient_id = ingredient_id
        
        self._build_ui()
        self._load_ingredient()
        
        self.setWindowTitle(f"Ingredient Editor: {self.ingredient_title}")

    def _build_ui(self):

        layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.category_combo = QComboBox()
        self.subcategory_combo = QComboBox()
        self.location_combo = QComboBox()
        self.base_unit_combo = QComboBox()
        self.count_unit_combo = QComboBox()
        self.purchase_unit_combo = QComboBox()

        layout.addRow(
            "Name:",
            self.name_edit
        )
        layout.addRow(
            "Category:",
            self.category_combo
        ) 
        layout.addRow(
            "Subcategory:",
            self.subcategory_combo
        )
        layout.addRow(
            "Location:",
            self.location_combo
        )
        layout.addRow(
            "Base Unit:",
            self.base_unit_combo
        )
        layout.addRow(
            "Count Unit:",
            self.count_unit_combo
        )
        layout.addRow(
            "Purchase Unit",
            self.purchase_unit_combo
        )

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.cancel_button
        )
        button_layout.addWidget(
            self.save_button
        )

        layout.addRow(
            button_layout
        )

        self.setLayout(layout)

        self.save_button.clicked.connect(
            self._save
        )
        self.cancel_button.clicked.connect(
            self.reject
        )

    def _load_ingredient(self):

        with session_scope() as session:

            service = IngredientService(session)

            ingredient = service.get(
                self.ingredient_id
            )

            if ingredient is None:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Ingredient could not be found"
                )

                self.reject()
                return
            
            self.ingredient_title = ingredient.item.name
            
            self._populate_fields(
                session,
                ingredient
            )
            

    def _save(self):
        
        data = IngredientUpdate(
            name = self.name_edit.text().strip(),
            category_id=self.category_combo.currentData(),
            subcategory_id=self.subcategory_combo.currentData(),
            location_id=self.location_combo.currentData(),
            base_unit_id=self.base_unit_combo.currentData(),
            count_unit_id=self.count_unit_combo.currentData(),
            purchase_unit_id=self.purchase_unit_combo.currentData()
        )
        print(data)

        try:
            with session_scope() as session:

                service = IngredientService(session)

                service.update(
                    self.ingredient_id,
                    data
                )
        except Exception as e:

            QMessageBox.critical(
                self,
                "Unable to Save Ingredient",
                str(e)
            )
            return
        
        self.accept()

    def _populate_fields(self, session, ingredient: Ingredient):
        
        self.name_edit.setText(
            ingredient.item.name
        )

        self._load_categories(session)
        cat = self.category_combo.findData(
            ingredient.category_id
        )
        if cat >= 0:
            self.category_combo.setCurrentIndex(
                cat
            )
        sub = self.subcategory_combo.findData(
            ingredient.subcategory_id
        )
        if sub >= 0:
            self.subcategory_combo.setCurrentIndex(
                sub
            )

        self._load_location(session)
        loc = self.location_combo.findData(
            ingredient.location_id
        )
        if loc >= 0:
            self.location_combo.setCurrentIndex(
                loc
            )

        self._load_units(session)
        base = self.base_unit_combo.findData(
            ingredient.base_unit_id
        )
        if base >= 0:
            self.base_unit_combo.setCurrentIndex(
                base
            )
        count = self.count_unit_combo.findData(
            ingredient.count_unit_id
        )
        if count >= 0:
            self.count_unit_combo.setCurrentIndex(
                count
            )
        purchase = self.purchase_unit_combo.findData(
            ingredient.purchase_unit_id
        )
        if purchase >= 0:
            self.purchase_unit_combo.setCurrentIndex(
                purchase
            )

    def _load_categories(self, session):

        category_service = IngredientCategoryService(session)
        subcategory_service = IngredientSubcategoryService(session)

        self.category_combo.clear()
        self.subcategory_combo.clear()

        categories = category_service.get_all()
        subcategories = subcategory_service.get_all()

        for category in categories:

            self.category_combo.addItem(
                category.name,
                category.id
            )
        
        for subcategory in subcategories:

            self.subcategory_combo.addItem(
                subcategory.name,
                subcategory.id
            )

    def _load_location(
            self,
            session
    ):
        location_service = InventoryLocationService(session)
        locations = location_service.get_all()

        for location in locations:

            self.location_combo.addItem(
                location.name,
                location.id
            )

    def _load_units(self, session):
        unit_service = UnitService(session)
        units = unit_service.get_all()

        for unit in units:

            self.base_unit_combo.addItem(
                unit.name,
                unit.id
            )
            self.count_unit_combo.addItem(
                unit.name,
                unit.id
            )
            self.purchase_unit_combo.addItem(
                unit.name,
                unit.id
            )