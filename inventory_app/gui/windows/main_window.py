from PySide6.QtWidgets import QMainWindow, QMdiArea

from inventory_app.app.app_context import AppContext
from inventory_app.gui.windows.window_manager import WindowManager

from inventory_app.ingredients.gui.ingredient_list import IngredientPage
from inventory_app.recipes.gui.recipe_list import RecipePage
from inventory_app.recipes.gui.recipe_editor import RecipeEditor
from inventory_app.purchases.gui.purchases_list import PurchasePage
from inventory_app.purchases.gui.purchase_editor import NewPurchaseDialog


class MainWindow(QMainWindow):
    """
    Main Application Window.

    MainWindow controls apps Top Level visual structure:

        - Menu Bar
        - Main Toolbar
        - MDI workspace
        - Window Manager

    Domain Specific functions and widgets implimented by domain level GUI files rather than MainWindow.

    MainWindow acts as applications GUI Shell and coordinator.
    """
    def __init__(self, context: AppContext):
        super().__init__()

        self.context = context
    
        self._build_menus()
        self._build_toolbar()
        self._build_ui()
        self._connect_signals()

    def _build_menus(self):
        menu_bar = self.menuBar()
        app_menu = menu_bar.addMenu("App")
        # First Submenu
        app_new_menu = app_menu.addMenu("New")
        self.new_inventory = app_new_menu.addAction("Item")
        self.new_purchase = app_new_menu.addAction("Purchase")
        self.new_recipe = app_new_menu.addAction("Recipe")
        app_new_menu.addSeparator()
        self.new_vendor = app_new_menu.addAction("Vendor")
        self.new_unit = app_new_menu.addAction("Unit")
        # Second submenu
        app_open = app_menu.addMenu("Open")
        self.open_inventory = app_open.addAction("Items")
        self.open_purchases = app_open.addAction("Purchases")
        self.open_recipes = app_open.addAction("Recipes")
    
    def _build_toolbar(self):
        """
        Build the applications main toolbar.
        """
        pass

    def _build_ui(self):
        self.setWindowTitle(self.context.business.name)
        self.resize(1400,900)           
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        self.window_manager = WindowManager(mdi_area=self.mdi_area, context=self.context)

    def _connect_signals(self):
        self.new_recipe.triggered.connect(self.window_manager.open_new_recipe)
        self.open_inventory.triggered.connect(self.window_manager.open_ingredients)
        self.new_purchase.triggered.connect(self.window_manager.open_new_purchase)
        self.open_purchases.triggered.connect(self.window_manager.open_purchases)
        self.open_recipes.triggered.connect(self.window_manager.open_recipes)