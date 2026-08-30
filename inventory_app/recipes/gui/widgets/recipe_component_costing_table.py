from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidget, QWidget, QLabel, QHBoxLayout
from decimal import Decimal


from inventory_app.app.app_context import AppContext
from inventory_app.recipes.dto import ComponentCostLine

class RecipeCostTable(QWidget):

    COLUMNS = {
        "quantity": 0,
        "unit": 1,
        "item": 2,
        "cost": 3,
        "percent_cost": 4,
        "problems": 5
    }

    HEADERS = [
        "Quantity",
        "Unit",
        "Item",
        "Cost",
        "% of Total",
        "Problems"
    ]

    def __init__(self, context: AppContext, parent=None):
        super().__init__(parent)
        self.context = context

        self._build_table()

    def _build_table(self):
        layout = QHBoxLayout(self)

        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        header = self.table.horizontalHeader()

        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_components(self, components: list[ComponentCostLine], total: Decimal):
        self.table.setRowCount(0)
        for component in components:
            row = self.table.rowCount()
            self.table.insertRow(row)
            quantity = QLabel()
            unit = QLabel()
            item = QLabel()
            cost = QLabel()
            percent_cost = QLabel()
            problems = QLabel()

            self.table.setCellWidget(row, self.COLUMNS["quantity"], quantity)
            self.table.setCellWidget(row, self.COLUMNS["unit"], unit)
            self.table.setCellWidget(row, self.COLUMNS["item"], item)
            self.table.setCellWidget(row, self.COLUMNS["cost"], cost)
            self.table.setCellWidget(row, self.COLUMNS["percent_cost"], percent_cost)
            self.table.setCellWidget(row, self.COLUMNS["problems"], problems)

            quantity.setText(str(round(component.recipe_quantity, 2)))
            unit.setText(component.recipe_unit)
            item.setText(component.component_name)
            component_cost = str(round(component.total_cost, 2))
            cost.setText(f"${component_cost}")
            percent = round(((component.total_cost / total) * 100), 2)
            percent_cost.setText(f"{percent}%")
