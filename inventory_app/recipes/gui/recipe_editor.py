from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize, QSignalBlocker
from PySide6.QtWidgets import QDialog, QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QComboBox, QPushButton
from typing import List
from decimal import Decimal

from inventory_app.app.app_context import AppContext
from inventory_app.common.conversions.conversion_engine import ConversionEngine
from inventory_app.recipes.gui.recipe_tabs import RecipeTab
from inventory_app.recipes.gui.costing_tab import CostingTab
from inventory_app.recipes.services.recipe_service import RecipeService
from inventory_app.recipes.models import Recipe
from inventory_app.recipes.dto import RecipeComponentInput, RecipeInput, RecipeCostReport
from inventory_app.recipes.engines.costing_engine import CostingEngine
from inventory_app.units.services.unit_service import UnitService

class RecipeEditor(QDialog):

    def __init__(
            self,
            context: AppContext,
            recipe_id: int | None = None,
            parent = None        
    ):
        super().__init__(parent)

        self.context = context
        self.recipe_id = recipe_id
        self.recipe = None

        self._build_ui()
        self._load_recipe()
        self._connect_signals()

    def _build_ui(self):
        """
        Editor page is broken into 2 horizontal sections.
        
        From top to bottom

            - Recipe Info

            Contains information like name, yield quantities and units, portion quantities and units, number of portion, and portion cost. Also has information about prep, cook, and shelf times for recipe (Not yet implimented), and Toggles for 'Active', 'Sub Recipe', and 'Saleable' (Not yet implimented) and entry fields for a PLU for pos sales. There are also fields for different tags, like Categories, locations, plates, and tools needed. (Also not implimented)

            - Tabs

            2/3 of the window. Has tabs for recipe creation, costing, nutritional info, etc. 
        """

        main_layout = QVBoxLayout(self)

        main_layout.addWidget(self._build_recipe_info_section())
        main_layout.addWidget(self._build_tab_section())
    
    def _load_recipe(self):
        if self.recipe_id is not None: 
            with self.context.session_factory() as session:
                self.recipe_service = RecipeService(session)
                self.recipe = self.recipe_service.get(self.recipe_id)
                self._populate_recipe_info(self.recipe)
                self.recipe_tab.load_recipe(self.recipe)  

    def _connect_signals(self):
        
        self.save.clicked.connect(self._save)
        self.tabs.currentChanged.connect(self._tab_changed)

        self.yield_edit.editingFinished.connect(self._on_yield_change)
        self.yield_unit_combo.currentIndexChanged.connect(self._on_yield_change)
        self.serving_edit.editingFinished.connect(self._on_serving_change)
        self.serving_unit_combo.currentIndexChanged.connect(self._on_serving_change)
        self.portions_edit.editingFinished.connect(self._on_portion_change)

        self.costing_tab.portion_price_changed.connect(self._on_portion_price_change)
        self.costing_tab.portion_percent_changed.connect(self._on_portion_percent_change)

    def _build_recipe_info_section(self):

        section_widget = QWidget()

        section_layout = QHBoxLayout(section_widget)

        # Recipe Info Subsection
        info_layout = QGridLayout()

        self.name_edit = QLineEdit()
        self.yield_edit = QLineEdit()
        self.yield_edit.setFixedWidth(50)
        self.yield_unit_combo = QComboBox()
        self._populate_units(self.yield_unit_combo)
        self.serving_edit = QLineEdit()
        self.serving_edit.setFixedWidth(50)
        self.serving_unit_combo = QComboBox()
        self._populate_units(self.serving_unit_combo)
        self.portions_edit = QLineEdit()
        self.portion_price_label = QLabel("$0.00")

        self.prep_time_edit = QLineEdit()
        self.cook_time_edit = QLineEdit()
        self.finish_time_edit = QLineEdit()
        self.shelf_time_edit = QLineEdit()

        info_layout.addWidget(QLabel("Name"), 0, 0)
        info_layout.addWidget(self.name_edit, 0, 1, 1, 5)

        info_layout.addWidget(QLabel("Yield"), 1, 0)
        info_layout.addWidget(self.yield_edit, 1, 1)
        info_layout.addWidget(self.yield_unit_combo, 1, 2)
        info_layout.addWidget(QLabel("Prep"), 1, 3)
        info_layout.addWidget(self.prep_time_edit, 1, 4, 1, 2)

        info_layout.addWidget(QLabel("Servings"), 2, 0)
        info_layout.addWidget(self.serving_edit, 2, 1)
        info_layout.addWidget(self.serving_unit_combo, 2, 2)
        info_layout.addWidget(QLabel("Cook"), 2, 3)
        info_layout.addWidget(self.cook_time_edit, 2, 4, 1, 2)
        
        info_layout.addWidget(QLabel("Num Portions"), 3, 0)
        info_layout.addWidget(self.portions_edit, 3, 1, 1, 2)
        info_layout.addWidget(QLabel("Finish"), 3, 3)
        info_layout.addWidget(self.finish_time_edit, 3, 4, 1, 2)

        info_layout.addWidget(QLabel("Portion Price"), 4, 0)
        info_layout.addWidget(self.portion_price_label, 4, 1)
        info_layout.addWidget(QLabel("Shelf"), 4, 3)
        info_layout.addWidget(self.shelf_time_edit, 4, 4, 1, 2)

        # Meta Data Subsection
        # Complete Later

        section_layout.addLayout(info_layout)
        self.save = QPushButton("Save")
        section_layout.addWidget(self.save)

        return section_widget
    
    def _build_tab_section(self):

        self.tabs = QTabWidget()

        self.recipe_tab = RecipeTab(self.context, self.recipe_id)
        self.costing_tab = CostingTab(self.context, self.recipe_id)

        self.tabs.addTab(self.recipe_tab, "Recipe")
        self.tabs.addTab(self.costing_tab, "Costing")

        return self.tabs
                
    def _populate_recipe_info(self, recipe: Recipe):
        
            self.name_edit.setText(recipe.item.name)
            self.yield_edit.setText(str(round(recipe.yield_qty, 2)))
            self.yield_unit_combo.setCurrentIndex(self.yield_unit_combo.findData(recipe.yield_unit_id))
            self.serving_edit.setText(str(round(recipe.serving_qty, 2)))
            self.serving_unit_combo.setCurrentIndex(self.serving_unit_combo.findData(recipe.yield_unit_id))
            with self.context.session_factory() as session:
                engine = CostingEngine(session)
                report = engine.cost_recipe(recipe)
                self.portion_price_label.setText(str(round(report.cost_per_serving, 2)))
                self.portions_edit.setText(str(round(report.num_of_servings, 2)))

    def _populate_units(self, combo: QComboBox):
        with self.context.session_factory() as session:
            service = UnitService(session)
            units = service.get_all()
            for unit in units:
                combo.addItem(unit.name, unit.id)
    
    def _save(self):
        if self.recipe_id is None:
            raise
        component_data = self.recipe_tab.get_components()
        recipe_data = self._get_recipe_data(component_data)
        if component_data is None:
            return
        if recipe_data is None:
            return

        with self.context.session_factory() as session:
            recipe_service = RecipeService(session)
            recipe_service.update(
                recipe_id = self.recipe_id,
                data = recipe_data
            )
            session.commit()
    
    def _tab_changed(self, index: int):
        if self.tabs.widget(index) is self.costing_tab:
            self._refresh_costing()

    def _get_recipe_data(self, component_data: List[RecipeComponentInput]) -> RecipeInput | None:
        name = self.name_edit.text()
        yield_qty = self.yield_edit.text().strip()
        yield_unit = self.yield_unit_combo.currentData(Qt.ItemDataRole.UserRole)
        serving_qty = self.serving_edit.text().strip()
        serving_unit = self.serving_unit_combo.currentData(Qt.ItemDataRole.UserRole)
        if yield_qty is None:
            return None
        if yield_unit is None:
            return None
        if serving_qty is None:
            return None
        if serving_unit is None:
            return None
        yield_qty = Decimal(yield_qty)
        serving_qty = Decimal(serving_qty)

        return RecipeInput(
            recipe_id=self.recipe_id,
            recipe_name=name,
            yield_qty=yield_qty,
            yield_unit_id=yield_unit,
            serving_qty=serving_qty,
            serving_unit_id=serving_unit,
            components=component_data
        )

    def _refresh_costing(self):
        component_data = self.recipe_tab.get_components()
        recipe_data = self._get_recipe_data(component_data)
        if recipe_data is None:
            return
        with self.context.session_factory() as session:
            engine = CostingEngine(session)
            report = engine.cost_recipe(recipe_data)
            self.costing_tab.load_report(report)
            self._load_report(report)

    def _load_report(self, report: RecipeCostReport):
        self.serving_edit.setText(str(round(report.serving_qty, 2)))
        self.portion_price_label.setText(str(round(report.cost_per_serving, 2)))
        self.portions_edit.setText(str(round(report.num_of_servings, 2)))
            
    def _on_yield_change(self):
        self._refresh_costing()
      
    def _on_serving_change(self):
        self._refresh_costing()

    def _on_portion_change(self):
        portions = Decimal(self.portions_edit.text())

        yield_qty, yield_unit = self.get_yield()
        serving_qty, serving_unit = self.get_serving()
        with self.context.session_factory() as session:
            engine = ConversionEngine(session)
            yield_as_serving_unit = engine.convert(yield_qty, yield_unit, serving_unit, None, None)
        
        new_serving_qty = (yield_as_serving_unit / portions)
        with QSignalBlocker(self.serving_edit):
            self.serving_edit.setText(str(round(new_serving_qty)))
        self._refresh_costing()


    def _on_portion_price_change(self):
        price = self.costing_tab.get_portion_price()
        cost = self.costing_tab.get_portion_cost()

        percent = ((cost / price) * 100)
        portion_margin = (price - cost)
        recipe_price = (price * Decimal(self.portions_edit.text()))
        recipe_margin = (recipe_price - self.costing_tab.get_recipe_cost())

        self.costing_tab.set_recipe_price(recipe_price)
        self.costing_tab.set_portion_percent(percent)
        self.costing_tab.set_recipe_percent(percent)
        self.costing_tab.set_portion_margin(portion_margin)
        self.costing_tab.set_recipe_margin(recipe_margin)


    def _on_portion_percent_change(self):
        percent = self.costing_tab.get_portion_percent()
        cost = Decimal(self.portion_price_label.text().lstrip("$"))
        price = ((percent / 100) * cost)
        self.costing_tab.set_portion_price(price)
        margin = (price - cost)
        self.costing_tab.set_portion_margin(margin)

    def get_yield(self) -> tuple[Decimal, int]:
        qty = Decimal(self.yield_edit.text())
        unit = int(self.yield_unit_combo.currentData(Qt.ItemDataRole.UserRole))
        return qty, unit
    
    def get_serving(self) -> tuple[Decimal, int]:
        qty = Decimal(self.serving_edit.text())
        unit = int(self.yield_unit_combo.currentData(Qt.ItemDataRole.UserRole))
        return qty, unit