from sqlalchemy.orm import Session
from rich.console import Console

from inventory_app.ingredients.models import Ingredient
from inventory_app.ingredients.services import ingredient_service, category_service, subcategory_service
from inventory_app.vendors.models import VendorItem

    
class IngredientInterface:

    def __init__(self):
        self.console = Console()

    @staticmethod
    def create_from_vend_item(
        session: Session,
        item: VendorItem
    ) -> Ingredient:
        
        self = IngredientInterface()

        self.console.print("-" * 40)
        self.console.print("Create New Ingredient for Vendor Item:")
        self.console.print(f"SKU: {item.vendor_sku}")
        self.console.print(f"Vendor Description: {item.vendor_description}")

        self.console.print()

        name = self.console.input("Enter Ingredient Name: ")

        get_category = category_service.get_all(session)

        for category in get_category:
            self.console.print(category)
        
        category = self.console.input("Enter Ingredient Category")

        get_sub = subcategory_service.get_by_category_name(session, category)

        for subcategory in get_sub:
            self.console.print(subcategory)
        
        subcategory = self.console.input("Please choose from one of the related Subcategories: ")
        base_unit = self.console.input("Please enter the abbreviation of the Base Unit: ")
        count_unit = self.console.input("Please enter the abbreviation of the Count Unit: ")
        purchase_unit = item.pack_unit

        self.console.print("-" * 40)
        self.console.print("Please confirm the details of the new Ingredient")
        self.console.print(f"Name: {name}, Category: {category}, Subcategory: {subcategory}, Base Unit: {base_unit}, Count Unit: {count_unit}, Purchase Unit: {purchase_unit}")
        confirm = self.console.input("Please Confirm (y/n): ")
        
        if confirm == "y":

            return ingredient_service.create(
                session,
                name=name,
                category=category,
                subcategory=subcategory,
                base_unit=base_unit,
                count_unit=count_unit,
                purchase_unit=purchase_unit
            )
        else:
            raise 

    def hint(
            self,
            session: Session
    ) -> Ingredient:
        
        hint = self.console.input("Please enter a closer match: ")

        return ingredient_service.get_by_name(session, hint)
