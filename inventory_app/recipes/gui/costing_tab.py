from PySide6.QtCore import Signal, QSignalBlocker
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit
from decimal import Decimal

from inventory_app.app.app_context import AppContext
from inventory_app.recipes.dto import RecipeCostReport
from inventory_app.recipes.gui.widgets.recipe_component_costing_table import RecipeCostTable


class CostingTab(QWidget):

    portion_price_changed = Signal()
    portion_percent_changed = Signal()

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
        self._connect_signals()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.table = RecipeCostTable(self.context)
        layout.addLayout(self._build_cost_grid())
        layout.addWidget(self.table)

    def _connect_signals(self):
        self.portion_price.editingFinished.connect(self.portion_price_changed.emit)
        self.portion_percent.editingFinished.connect(self.portion_percent_changed.emit)
    
    def _build_cost_grid(self):
        layout = QGridLayout()
        self.portion_cost = QLabel("$0.00")
        self.portion_price = QLineEdit()
        self.portion_percent = QLineEdit()
        self.portion_margin = QLineEdit()
        self.recipe_cost = QLabel("$0.00")
        self.recipe_price = QLabel("$0.00")
        self.recipe_percent = QLabel("$0.00")
        self.recipe_margin = QLabel("$0.00")

        layout.addWidget(QLabel("Single Portion"), 0, 1)
        layout.addWidget(QLabel("Entire Recipe"), 0, 2)
        layout.addWidget(QLabel("Cost"), 1, 0)
        layout.addWidget(self.portion_cost, 1, 1)
        layout.addWidget(self.recipe_cost, 1, 2)
        layout.addWidget(QLabel("Price"), 2, 0)
        layout.addWidget(self.portion_price, 2, 1)
        layout.addWidget(self.recipe_price, 2, 2)
        layout.addWidget(QLabel("% Cost"), 3, 0)
        layout.addWidget(self.portion_percent, 3, 1)
        layout.addWidget(self.recipe_percent, 3, 2)
        layout.addWidget(QLabel("Margin"), 4, 0)
        layout.addWidget(self.portion_margin, 4, 1)
        layout.addWidget(self.recipe_margin, 4, 2)

        return layout

    def load_report(self, report: RecipeCostReport):
        self.portion_cost.setText(str(round(report.cost_per_serving, 2)))
        self.recipe_cost.setText(str(round(report.total_cost, 2)))

        self.table.load_components(report.component_lines, report.total_cost)
    
    def get_portion_cost(self) -> Decimal:
        return Decimal(self.portion_cost.text().lstrip("$"))
    
    def get_portion_price(self) -> Decimal:
        return Decimal(self.portion_price.text().lstrip("$"))

    def get_portion_percent(self) -> Decimal:
        return Decimal(self.portion_percent.text().strip("%"))
    
    def get_recipe_cost(self) -> Decimal:
        return Decimal(self.recipe_cost.text().lstrip("$"))
    
    def set_portion_price(self, value: Decimal):
        with QSignalBlocker(self.portion_price):
            self.portion_price.setText(f"{value:.2f}")

    def set_portion_percent(self, value: Decimal):
        with QSignalBlocker(self.portion_percent):
            self.portion_percent.setText(f"{value:.2f}%")
    
    def set_portion_margin(self, value: Decimal):
        self.portion_margin.setText(f"${value:.2f}")

    def set_recipe_price(self, value: Decimal):
        self.recipe_price.setText(f"${value:.2f}")
    
    def set_recipe_percent(self, value: Decimal):
        self.recipe_percent.setText(f"{value:.2f}%")

    def set_recipe_margin(self, value: Decimal):
        self.recipe_margin.setText(f"${value:.2f}")
