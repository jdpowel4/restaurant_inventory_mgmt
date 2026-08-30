from PySide6.QtWidgets import QMainWindow, QMdiArea

from inventory_app.app.app_context import AppContext
from inventory_app.gui.windows.window_manager import WindowManager

from inventory_app.ingredients.gui.ingredient_list import IngredientPage
from inventory_app.recipes.gui.recipe_list import RecipePage
from inventory_app.recipes.gui.recipe_editor import RecipeEditor


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

        self.setWindowTitle(
            self.context.business.name
        )

        self.resize(1400,900)

        # -------------------------
        # MDI Workspace
        # 
        # QMdiArea is the workspace where all application windows will live.
        # 
        # Individual domain windows remain normal QWidget subclasses.
        # MainWindow wraps them in QMdiSubWindow objects when thet are opened.
        # -------------------------     
            
        self.mdi_area = QMdiArea()

        self.setCentralWidget(self.mdi_area)

        # -------------------------
        # Window Manager
        # 
        # The WindowManager is responsible for opening and eventaully tracking MDI Windows
        # -------------------------        

        self.window_manager = WindowManager(
            mdi_area=self.mdi_area,
            context=self.context
        )

        self._build_menus()
        self._build_toolbar()



    def _build_menus(self):
        """
        Building the applications top-level menu bar.
        """

        # Initalizing Menu obj
        menu_bar = self.menuBar()

        # Creating first drop down menu
        # 
        # following submenus and action buttons owned by the 'App' menu        
        app_menu = menu_bar.addMenu("App")

        # First Submenu       
        app_new_menu = app_menu.addMenu("New")
        new_inventory = app_new_menu.addAction("Item")
        new_purchases = app_new_menu.addAction("Purchases")
        new_recipe = app_new_menu.addAction("Recipe")
        new_recipe.triggered.connect(self.new_recipe)
        app_new_menu.addSeparator()
        new_vendor = app_new_menu.addAction("Vendor")
        new_unit = app_new_menu.addAction("Unit")

        # Second submenu
        app_open = app_menu.addMenu("Open")
        open_inventory = app_open.addAction("Items")
        open_inventory.triggered.connect(
            self.open_ingredients
        )
        #open_purchases = app_open.addAction("Purchases")
        #open_purchases.triggered.connect(
        #    self.open_purchases
        #)
        open_recipes = app_open.addAction("Recipes")
        open_recipes.triggered.connect(
            self.open_recipes
        )

        # These actions will eventually call methods that use the WindowManager to open the appropiate domain windows.

    def _build_toolbar(self):
        """
        Build the applications main toolbar.
        """
        pass

    def open_ingredients(self):
        self.window_manager.open(
            IngredientPage(self.context),
            "Ingredients"
        )
    
    def open_recipes(self):
        self.window_manager.open(
            RecipePage(self.context),
            "Recipes"
        )
    
    def new_recipe(self):
        self.window_manager.open(
            RecipeEditor(self.context),
            "New Recipe"
        )