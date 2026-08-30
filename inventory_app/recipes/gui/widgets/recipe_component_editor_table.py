from PySide6.QtCore import Qt, QSize, Signal, QEvent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractItemView, QComboBox, QHBoxLayout, QHeaderView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolButton, QLineEdit, QCompleter, QLabel
from decimal import Decimal, InvalidOperation

from inventory_app.app.app_context import AppContext
from inventory_app.recipes.dto import RecipeComponentInput
from inventory_app.recipes.models import RecipeComponent
from inventory_app.items.services.item_service import ItemService

class RecipeComponentTable(QWidget):

    COLUMNS = {
        "quantity": 0,
        "unit": 1,
        "pre_instructions": 2,
        "item": 3,
        "post_instructions": 4,
        "component_id": 5
    }
    HEADERS = [
        "Quantity",
        "Unit",
        "Pre-Instructions",
        "Item",
        "Post-Instructions",
        "component_id"
    ]
    components_changed = Signal()

    def __init__(self, context: AppContext, recipe_id: int | None = None, parent=None):
        super().__init__(parent)

        self.recipe_id = recipe_id
        self.context = context
        
        self._build_table()
        #self._connect_singals()
        self.table.installEventFilter(self)
    
    def _build_table(self):

        layout = QHBoxLayout(self)

        # Component Table
        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        # Allow user to select entire row
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setColumnHidden(self.COLUMNS["component_id"], True)
        

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(self.COLUMNS["quantity"], QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMNS["unit"], QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMNS["pre_instructions"], QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(self.COLUMNS["item"], QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(self.COLUMNS["post_instructions"], QHeaderView.ResizeMode.Stretch)

        layout.addWidget(self.table)

        self._add_empty_row()


    def get_components(self) -> list[RecipeComponentInput]:
        components = []
        for row in range(self.table.rowCount()):
            component = self._get_component_from_row(row)
            if component is not None:
                components.append(component)
        return components
    
    def _get_component_from_row(self, row: int) -> RecipeComponentInput | None:

        component_id = self.table.cellWidget(row, self.COLUMNS["component_id"])
        if not isinstance(component_id, QLabel):
            raise RuntimeError(f"Expected QLabel in component_id column, row {row}")
        
        quantity_item = self.table.cellWidget(row, self.COLUMNS["quantity"])
        if not isinstance(quantity_item, QLineEdit):
            raise RuntimeError(f"Expected QLineEdit in quantity column, row {row}")
        
        unit_combo = self.table.cellWidget(row, self.COLUMNS["unit"])
        if not isinstance(unit_combo, QComboBox):
            raise RuntimeError(f"Expected QComboBox in unit column, row {row}")
        
        pre_item = self.table.cellWidget(row, self.COLUMNS["pre_instructions"])
        if not isinstance(pre_item, QLineEdit):
            raise RuntimeError(f"Expected QLineEdit in pre-instruction column, row {row}")
        
        item_combo = self.table.cellWidget(row, self.COLUMNS["item"])
        if not isinstance(item_combo, QComboBox):
            raise RuntimeError(f"Expected QComboBox in item column, row {row}")
        
        post_item = self.table.cellWidget(row, self.COLUMNS["post_instructions"])
        if not isinstance(post_item, QLineEdit):
            raise RuntimeError(f"Expected QLineEdit in post-instruction column, row {row}")
        
        if quantity_item is None:
            return None
        if unit_combo is None:
            return None
        if item_combo is None:
            return None
        
        quantity_text = quantity_item.text().strip()
        unit_id = unit_combo.currentData(Qt.ItemDataRole.UserRole)
        item_id = item_combo.currentData(Qt.ItemDataRole.UserRole)

        if not quantity_text or unit_id is None or item_id is None:
            return None
        
        if component_id.text() == "None":
            component_id = None
        else: 
            component_id = int(component_id.text())
        

        return RecipeComponentInput(
            id=component_id,
            quantity=Decimal(quantity_text),
            unit_id=unit_id,
            item_id=item_id,
            pre_instructions=(pre_item.text() if pre_item is not None else ""),
            post_instructions=(post_item.text() if post_item is not None else "")
        )
    def _add_empty_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.quantity_edit = QLineEdit()
        self.quantity_edit.setPlaceholderText("Qty")
        self.table.setCellWidget(row, self.COLUMNS["quantity"], self.quantity_edit)
        self.unit_combo = QComboBox()
        self._populate_units(self.unit_combo)
        self._configure_searchable_combo(self.unit_combo)
        self.unit_combo.setCurrentIndex(-1)
        self.table.setCellWidget(row, self.COLUMNS["unit"], self.unit_combo)
        self.pre_item = QLineEdit()
        self.table.setCellWidget(row, self.COLUMNS["pre_instructions"], self.pre_item)
        self.item_combo = QComboBox()
        self._populate_ingredients(self.item_combo)
        self._configure_searchable_combo(self.item_combo)
        self.item_combo.setCurrentIndex(-1)
        self.table.setCellWidget(row, self.COLUMNS["item"], self.item_combo)
        self.post_item = QLineEdit()
        self.post_item.installEventFilter(self)
        self.table.setCellWidget(row, self.COLUMNS["post_instructions"], self.post_item)
        self.table.setCellWidget(row, self.COLUMNS["component_id"], QLabel("None"))
        
        self.quantity_edit.setFocus()

    def load_components(self, components: list[RecipeComponent]):
        self.table.setRowCount(0)
        for component in components:
            row = self.table.rowCount()
            
            self.table.insertRow(row)
            self.quantity_edit = QLineEdit()
            self.unit_combo = QComboBox()
            self._populate_units(self.unit_combo)
            self._configure_searchable_combo(self.unit_combo)
            self.pre_item = QLineEdit()
            self.item_combo = QComboBox()
            self._populate_ingredients(self.item_combo)
            self._configure_searchable_combo(self.item_combo)
            self.post_item = QLineEdit()
            self.post_item.installEventFilter(self)
            self.component_label = QLabel()

            self.table.setCellWidget(row, self.COLUMNS["quantity"], self.quantity_edit)
            self.table.setCellWidget(row, self.COLUMNS["unit"], self.unit_combo)
            self.table.setCellWidget(row, self.COLUMNS["pre_instructions"], self.pre_item)
            self.table.setCellWidget(row, self.COLUMNS["item"], self.item_combo)
            self.table.setCellWidget(row, self.COLUMNS["post_instructions"], self.post_item)
            self.table.setCellWidget(row, self.COLUMNS["component_id"], self.component_label)

            self.quantity_edit.setText(str(round(component.quantity, 2)))
            self.unit_combo.setCurrentIndex(self.unit_combo.findData(component.unit.id))
            #Pre instructions once it gets implimented
            self.item_combo.setCurrentIndex(self.item_combo.findData(component.item.id))
            # Post Instruction once implimented
            self.component_label.setText(str(component.id))

    def _populate_units(self, combo: QComboBox):
        with self.context.session_factory() as session:
            service = self.context.load_unit_service(session)
            units = service.get_all()
            for unit in units:
                combo.addItem(unit.name, unit.id)

    def _populate_ingredients(self, combo: QComboBox):
        with self.context.session_factory() as session:
            service = ItemService(session)
            items = service.list()
            for item in items:
                combo.addItem(item.name, item.id)

    def _configure_searchable_combo(self, combo: QComboBox):
        combo.setEditable(True)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setStyleSheet("""
            QComboBox {
                border: none;
                padding: 0px;
                background: transparent;
            }    
            QComboBox::drop-down {
                border: none;
                width: 18px
            }
        """)
        completer = QCompleter(combo.model(), combo)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        combo.setCompleter(completer)
        
    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
                if self._is_last_editable_cell():
                    self._add_empty_row()
                    return True
        return super().eventFilter(watched, event)

    def _is_last_editable_cell(self) -> bool:
        return(
            self.table.currentRow() == self.table.rowCount() - 1
            and
            self.table.currentColumn() == self.COLUMNS["post_instructions"]
        )