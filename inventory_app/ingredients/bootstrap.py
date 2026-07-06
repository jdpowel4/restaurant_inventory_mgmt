from sqlalchemy.orm import Session

from inventory_app.shared.logging import get_logger, log_operation, LogLevels

from inventory_app.ingredients.models import *
from inventory_app.ingredients.services import category_service, subcategory_service, ingredient_service, conversion_service
from inventory_app.items.services import item_service
from inventory_app.units.services import unit_service



logger = get_logger(__name__)

@log_operation(level=LogLevels.INFO)
def seed_defaults(
    session: Session
):
    
    DEFAULT_CATEGORIES = [
        ("Food", 1),
        ("Beverage", 2),
        ("Alcohol", 3),
        ("Non Food Item", 4)
    ]

    DEFAULT_SUBCATEGORIES = [
        ("Proteins", "Food"),
        ("Produce", "Food"),
        ("Dairy", "Food"),
        ("Breads", "Food"),
        ("Dry Goods", "Food"),
        ("Frozen", "Food"),
        ("Prepared Foods", "Food"),
        ("Condiments", "Food"),
        ("Spices", "Food"),
        ("Oils", "Food"),
        ("Desserts", "Food"),

        ("Soft Drink", "Beverage"),
        ("Tea", "Beverage"),
        ("Coffee", "Beverage"),
        ("Juice", "Beverage"),
        ("Water", "Beverage"),
        ("Mixes and Syrups", "Beverage"),

        ("Beer", "Alcohol"),
        ("Wine", "Alcohol"),
        ("Liquor", "Alcohol"),
        ("Cocktail Mixers", "Alcohol"),

        ("Disposables", "Non Food Item"),
        ("Cleaning Chemicals", "Non Food Item"),
        ("Kitchen Supplies", "Non Food Item"),
        ("Office Supplies", "Non Food Item"),
        ("Maintenance", "Non Food Item"),
        ("Paper Products", "Non Food Item"),
        ("Smallwares", "Non Food Item"),
        ("Packaging", "Non Food Item")
    ]

    DEFAULT_INGREDIENTS = [
        ("Beef, Ground", "Food", "Proteins", "ounce"),
        ("Chicken, Breast", "Food", "Proteins", "ounce"),
        ("Pork, Shoulder", "Food", "Proteins", "ounce"),
        ("Bacon, Slices", "Food", "Proteins", "slice"),
        ("Eggs", "Food", "Proteins", "each"),

        ("Milk, Whole", "Food", "Dairy", "fluid ounce"),
        ("Cream, Heavy", "Food", "Dairy", "fluid ounce"),
        ("Butter", "Food", "Dairy", "ounce"),
        ("Cheese, Chedder", "Food", "Dairy", "ounce"),
        ("Cheese, Mozzarella", "Food", "Dairy", "ounce"),

        ("Onion, Yellow", "Food", "Produce", "ounce"),
        ("Tomato, 5x6", "Food", "Produce", "ounce"),
        ("Lettuce, Iceberg", "Food", "Produce", "ounce"),
        ("Carrot, Jumbo", "Food", "Produce", "ounce"),
        ("Celery", "Food", "Produce", "ounce"),
        ("Pepper, Green Bell", "Food", "Produce", "ounce"),
        ("Potato, Baking", "Food", "Produce", "ounce"),
        ("Garlic, Minced", "Food", "Produce", "ounce"),
        ("Lemon", "Food", "Produce", "ounce"),

        ("Flour", "Food", "Dry Goods", "ounce"),
        ("Sugar, Granulated", "Food", "Dry Goods", "ounce"),
        ("Sugar, Brown", "Food", "Dry Goods", "ounce"),
        ("Pepper, Black", "Food", "Dry Goods", "ounce"),
        ("Rice, White Long-Grain", "Food", "Dry Goods", "ounce"),
        ("Bean, Pinto", "Food", "Dry Goods", "ounce"),
        ("Pasta, Macaroni", "Food", "Dry Goods", "ounce"),
        ("Baking, Powder", "Food", "Dry Goods", "ounce"),
        ("Baking, Soda", "Food", "Dry Goods", "ounce"),
        ("Cornstarch", "Food", "Dry Goods", "ounce"),

        ("Oil, Fryer", "Food", "Oils", "ounce"),
        ("Oil, Olive", "Food", "Oils", "fluid ounce"),

        ("Ketchup", "Food", "Condiments", "fluid ounce"),
        ("Mustard, Yellow", "Food", "Condiments", "fluid ounce"),
        ("Mayo", "Food", "Condiments", "fluid ounce"),
        ("Sauce, Soy", "Food", "Condiments", "fluid ounce"),
        ("Sauce, Worcestershire", "Food", "Condiments", "fluid ounce"),
        ("Vinegar, Apple Cider", "Food", "Condiments", "fluid ounce"),

        ("Paprika", "Food", "Spices", "ounce"),
        ("Garlic, Granulated", "Food", "Spices", "ounce"),
        ("Spice, Onion Powder", "Food", "Spices", "ounce"),
        ("Spice, Chili", "Food", "Spices", "ounce"),
        ("Spice, Oregano", "Food", "Spices", "ounce"),
        ("Spice, Basil Dry", "Food", "Spices", "ounce"),
        ("Spice, Thyme", "Food", "Spices", "ounce"),
        ("Spice, Cinnamon", "Food", "Spices", "ounce")
    ]

    DEFUALT_CONVERSIONS = [
        ("Milk, Whole", "cup", "ounce", 8.6),
        ("Flour", "cup", "ounce", 4.25),
        ("Sugar, Granulated", "cup", "ounce", 7.1),
        ("Butter", "cup", "ounce", 8),
    ]
    categories = {}

    for name, sort in DEFAULT_CATEGORIES:

        categories[name] = category_service.get_or_create(session, name, sort)
    
    subcategories = {}

    for name, category in DEFAULT_SUBCATEGORIES:

        subcategories[name] = subcategory_service.get_or_create(session, name, categories[category])
    
    print("Successfully Seeded Ingredient Categories and Subcategories")


    units = {u.name: u for u in unit_service.get_all(session)}

    ingredients = {}

    for name, category, subcategory, base_unit in DEFAULT_INGREDIENTS:

        ingredients[name] = ingredient_service.get_or_create(session, name=name, category=categories[category], subcategory=subcategories[subcategory], base_unit=units[base_unit])

    session.flush()
    print("Successfully Seeded Ingredients")

    for ingredient, from_unit, to_unit, multiplier in DEFUALT_CONVERSIONS:

        conversion_service.create(
            session,
            ingredient=ingredients[ingredient],
            from_unit=units[from_unit],
            to_unit=units[to_unit],
            multiplier=multiplier
        )
        
    print("Successfully Seeded Ingredient Specicific Unit Conversions")

