from PySide6.QtCore import Qt, QSize, Signal, QEvent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QAbstractItemView, QComboBox, QHBoxLayout, QHeaderView, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QToolButton, QLineEdit, QCompleter, QLabel, QMessageBox
from decimal import Decimal

from inventory_app.app.app_context import AppContext
from inventory_app.gui.errors import ErrorAction
from inventory_app.purchases.services.purchase_service import PurchaseService
from inventory_app.purchases.models import PurchaseItem
from inventory_app.vendors.repositories.vendor_item_repo import VendorItemRepo
from inventory_app.vendors.exceptions import MissingVendorItemError


class PurchaseTable(QWidget):

    COLUMNS = {
        "item_name": 0,
        "vendor_sku": 1,
        "quantity": 2,
        "units": 3,
        "change": 4,
        "unit_cost": 5
    }
    HEADERS = [
        "Item Name",
        "Vendor SKU",
        "Quantity",
        "Unit",
        "Change",
        "Unit Cost"
    ]

    def __init__(self, context: AppContext, purchase_id: int):
        super().__init__()

        self.purchase_id = purchase_id
        self.context = context

        self._build_table()
        self._connect_signals()
        self.table.installEventFilter(self)

    def _build_table(self):
        layout = QHBoxLayout(self)

        # PurchaseItem Table
        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels(self.HEADERS)
        # Allow user to select entire row
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(self.COLUMNS["item_name"], QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMNS["vendor_sku"], QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMNS["quantity"], QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMNS["unit"], QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMNS["change"], QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(self.COLUMNS["unit_cost"], QHeaderView.ResizeMode.ResizeToContents)


        layout.addWidget(self.table)
        self._add_empty_row()

    def load_purchase_items(self, items: list[PurchaseItem]):
        self.table.setRowCount(0)
        if not items:
            self._add_empty_row()
        for item in items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.item_name.setText(item.vendor_item.ingredient.item.name)
            self.vendor_sku_edit.setText(item.vendor_item.vendor_sku)
            self.quantity_edit.setText(str(item.quantity))
            self.unit_combo.setCurrentIndex(self.unit_combo.findData(item.))




    def _connect_signals(self):
        self.vendor_sku_edit.editingFinished.connect(self._load_ingredient)

    def _add_empty_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.item_name = QLabel()
        self.vendor_sku_edit = QLineEdit()
        self.quantity_edit = QLineEdit()
        self.unit_combo = QComboBox()
        self._configure_unit_combo(self.unit_combo)
        self.change = QLabel()
        self.unit_cost = QLabel()
        self.table.setCellWidget(row, self.COLUMNS["item_name"], self.item_name)
        self.table.setCellWidget(row, self.COLUMNS["vendor_sku"], self.vendor_sku_edit)
        self.table.setCellWidget(row, self.COLUMNS["quantity"], self.quantity_edit)
        self.table.setCellWidget(row, self.COLUMNS["units"], self.unit_combo)
        self.table.setCellWidget(row, self.COLUMNS["change"], self.change)
        self.table.setCellWidget(row, self.COLUMNS["unit_cost"], self.unit_cost)
        self.vendor_sku_edit.setFocus()

    def _load_ingredient(self, sku):
        with self.context.session_factory() as session:
            service = PurchaseService(session)
            purchase = service.get(self.purchase_id)
            repo = VendorItemRepo(session)
            try:
                vendor_item = repo.get_by_sku(purchase.vendor, sku)
            except MissingVendorItemError as e:
                action = ErrorAction.missing_vendor_item(self, purchase.vendor.name, sku)


    def _configure_unit_combo(self, combo: QComboBox):
        with self.context.session_factory() as session:
            service = self.context.load_unit_service(session)
            units = service.get_all()
            for unit in units:
                combo.addItem(unit.name, unit.id)
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
        combo.setCurrentIndex(-1)

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Tab:
