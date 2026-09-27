from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QWidget, QTableWidget, QVBoxLayout, QPushButton, QDialog
from datetime import datetime

from inventory_app.app.app_context import AppContext
from inventory_app.purchases.services.purchase_service import PurchaseService
from inventory_app.purchases.gui.purchase_editor import NewPurchaseDialog, PurchaseEditor

class PurchasePage(QWidget):

    COLUMNS = {
        "date": 0,
        "vendor": 1,
        "invoice_number": 2,
        "total": 3
    }
    HEADERS = [
        "Date",
        "Vendor",
        "Invoice #",
        "Total"
    ]

    def __init__(self, context: AppContext):
        super().__init__()
        self.context = context

        self._build_ui()
        self._load_purchases()
        self._connect_signals()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        self.setWindowTitle("Purchases")
        self.purchases_list = QTableWidget(0, len(self.HEADERS))
        self.purchases_list.setHorizontalHeaderLabels(self.HEADERS)
        self.add_button = QPushButton("Add Purchase")
        layout.addWidget(self.purchases_list)
        layout.addWidget(self.add_button)

    def _connect_signals(self):
        self.add_button.clicked.connect(self._create_purchase)

    def _add_row(self):
        row = self.purchases_list.rowCount()
        self.purchases_list.insertRow(row)
        self.date = QLabel()
        self.vendor = QLabel()
        self.inv_num = QLabel()
        self.total = QLabel()
        self.purchases_list.setCellWidget(row, self.COLUMNS["date"], self.date)
        self.purchases_list.setCellWidget(row, self.COLUMNS["vendor"], self.vendor)
        self.purchases_list.setCellWidget(row, self.COLUMNS["invoice_number"], self.inv_num)
        self.purchases_list.setCellWidget(row, self.COLUMNS["total"], self.total)

    def _load_purchases(self):
        with self.context.session_factory() as session:
            service = PurchaseService(session)
            purchases = service.get_all()
            self.purchases_list.setRowCount(0)
            for purchase in purchases:
                self._add_row()
                self.date.setText(purchase.invoice_date.strftime("%m/%d/%Y"))
                self.vendor.setText(purchase.vendor.name)
                self.inv_num.setText(str(purchase.invoice_number))
                self.total.setText(f"${purchase.total}")

    def _create_purchase(self):
        pass