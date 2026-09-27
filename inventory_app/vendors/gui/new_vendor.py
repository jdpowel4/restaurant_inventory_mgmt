from PySide6.QtWidgets import QDialog, QFormLayout, QHBoxLayout

from inventory_app.app.app_context import AppContext

class VendorDialog(QDialog):

    def __init__(self, context: AppContext):
        super().__init__()

        self.context = context

        self._build_ui()

    def _build_ui(self):
        
        layout = QFormLayout(self)

        