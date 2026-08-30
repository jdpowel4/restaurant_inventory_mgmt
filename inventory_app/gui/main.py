import time
import sys

START = time.perf_counter()
from PySide6.QtWidgets import QApplication
print(f"Imports: {time.perf_counter() - START:.3f}s")
from inventory_app.app.app_context import AppContext
print(f"AppContext import: {time.perf_counter() - START:.3f}s")
from inventory_app.gui.windows.main_window import MainWindow
print(f"MainWindow import: {time.perf_counter() - START:.3f}s")


def main():
    print(f"Before QApp: {time.perf_counter() - START:.3f}s")    
    app = QApplication(sys.argv)
    print(f"After QApp: {time.perf_counter() - START:.3f}s")
    context = AppContext()
    print(f"After Context: {time.perf_counter() - START:.3f}s")
    window = MainWindow(context)
    print(f"After MainWindow: {time.perf_counter() - START:.3f}s")
    window.show()
    print(f"After show: {time.perf_counter() - START:.3f}s")
    sys.exit(app.exec())

