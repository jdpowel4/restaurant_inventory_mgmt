from __future__ import annotations
from PySide6.QtWidgets import QMessageBox, QWidget
from enum import Enum, auto

class ErrorAction(Enum):
    CANCEL = auto()
    CREATE_VENDOR = auto()
    CREATE_VENDOR_ITEM = auto()
    CREATE_INGREDIENT = auto()
    RETRY = auto()

    @classmethod
    def missing_vendor_item(
            cls,
            parent: QWidget,
            vendor_name: str,
            sku: str
    ) -> ErrorAction:
        box = QMessageBox(parent)
        box.setIcon(QMessageBox.Icon.Critical)
        box.setWindowTitle("Vendor Item Not Found")
        box.setText("The vendor item could not be found.")
        box.setInformativeText(f"No vendor item with SKU {sku} exists for {vendor_name}.")
        box.setDetailedText("A vendor item must be mapped to an ingredient before this purchase can be entered.")
        create_button = box.addButton("Create Vendor Item", QMessageBox.ButtonRole.AcceptRole)
        cancel_button = box.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(create_button)
        box.setEscapeButton(cancel_button)
        box.exec()
        if box.clickedButton() is create_button:
            return ErrorAction.CREATE_VENDOR_ITEM
        return ErrorAction.CANCEL