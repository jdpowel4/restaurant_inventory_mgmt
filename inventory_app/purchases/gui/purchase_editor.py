from PySide6.QtCore import Signal, QDate
from PySide6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QComboBox, QPushButton, QLineEdit, QDateEdit, QLabel, QMessageBox
from decimal import Decimal
from datetime import date

from inventory_app.app.app_context import AppContext
from inventory_app.vendors.services.vendor_service import VendorService
from inventory_app.purchases.services.purchase_service import PurchaseService
from inventory_app.purchases.gui.widgets.purchase_table import PurchaseTable


class NewPurchaseDialog(QDialog):

    new_vendor = Signal()
    purchase_created = Signal(int)

    def __init__(
            self,
            context: AppContext,
            parent = None
    ):
        super().__init__(parent)

        self.context = context

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        self.vendor_combo = QComboBox()
        self._load_vendors()
        self.new_vendor_button = QPushButton("New Vendor")
        main_layout.addWidget(self.vendor_combo)
        main_layout.addWidget(self.new_vendor_button)
        form_layout = QFormLayout()
        self.inv_number = QLineEdit()
        self.inv_date = QDateEdit()
        self.inv_date.setCalendarPopup(True)
        self.inv_date.setDate(QDate.currentDate())
        count_widget = QWidget()
        count_lable = QVBoxLayout(count_widget)
        count_lable.addWidget(QLabel("Number of Items"))
        count_lable.addWidget(QLabel("[optional]"))
        self.item_count = QLineEdit()
        total_widget = QWidget()
        total_label = QVBoxLayout(total_widget)
        total_label.addWidget(QLabel("Total Amount"))
        total_label.addWidget(QLabel("[optional]"))
        self.total = QLineEdit()
        form_layout.addRow("Invoice Number", self.inv_number)
        form_layout.addRow("Invoice Date", self.inv_date)
        form_layout.addRow(count_widget, self.item_count)
        form_layout.addRow(total_widget, self.total)
        main_layout.addLayout(form_layout)
        button_box = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        button_box.addWidget(self.ok_button)
        button_box.addWidget(self.cancel_button)
        main_layout.addLayout(button_box)
    
    def _connect_signals(self):
        self.new_vendor_button.clicked.connect(self.new_vendor.emit)
        self.ok_button.clicked.connect(self._save_purchase)
        self.cancel_button.clicked.connect(self.reject)
        
    def _save_purchase(self):
        vendor_id = self.vendor_combo.currentData()
        invoice_number = self.inv_number.text().strip()
        qdate = self.inv_date.date()
        invoice_date = date(
            qdate.year(),
            qdate.month(),
            qdate.day(),
        )    
        item_count = self.item_count.text().strip()
        total = Decimal(self.total.text().strip())

        with self.context.session_factory() as session:
            vendor_service = VendorService(session)
            vendor = vendor_service.get(vendor_id)
            if vendor is None:
                QMessageBox.critical(None, "Error Occurred", "No Vendor Found, Please Create New Vendor.")
                return
            service = PurchaseService(session)
            purchase = service.create(vendor, invoice_number, invoice_date, total)
            purchase_id = purchase.id
        self.purchase_created.emit(purchase_id)
        self.accept()

    def _load_vendors(self):
        with self.context.session_factory() as session:
            service = VendorService(session)
            vendors = service.get_all()
            for vendor in vendors:
                self.vendor_combo.addItem(vendor.name, vendor.id)


class PurchaseEditor(QWidget):

    def __init__(
            self,
            context: AppContext,
            purchase_id: int,
            parent = None
    ):
        super().__init__(parent)

        self.context = context
        self.purchase_id = purchase_id

        self._build_ui()
        self._load_purchase()

    def _build_ui(self):
        self.table = PurchaseTable(
            self.context,
            self.purchase_id
        )
        layout = QVBoxLayout(self)
        #layout.addWidget(self._build_purchase_info_section())
        layout.addWidget(self.table)
        #layout.addWidget(self._build_lower_section())

    def _load_purchase(self):
        with self.context.session_factory() as session:
            service = PurchaseService(session)
            purchase = service.get(self.purchase_id)
            self.table.load_purchase_items(purchase.items)

    def _build_purchase_info_section(self):
        section_widget = QWidget()
        section_layout = QHBoxLayout(section_widget)

    