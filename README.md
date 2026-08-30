# Restaurant Inventory Management

Forgive me Father, for I have sinned... this README is 100% AI generated. Don't hate me... I just suck at essays and the likes. That being said i don't think this would be considered vibe-coding, granted chat-gpt has helped get me started, but this is my second revision and I have never copy-pasted, so i think its fairly kosher... or atleast it looks good from my house.

A Python-based inventory management, recipe costing, purchasing, and reporting system built specifically for restaurants.

This project is designed as a long-term replacement for commercial systems such as ChefTec and Restaurant365 while remaining lightweight, fully customizable, and entirely self-hosted.

Although currently command-line driven, the application is being architected so multiple interfaces (CLI, Desktop, and eventually Web) can all operate from the same business logic.

---

# Current Status

The project is currently under active development.

Completed or mostly complete modules include:

- SQLite Database using SQLAlchemy and Alembic for database migrations
    - **Business**
        - Single Row Table with all business specific information
    - **Ingredients**
        - Ingredients
        - Ingredient Categories
        - Ingredient Subcategories
        - Ingredient Unit Conversions
    - **Inventory**
        - Inventory Events
        - Inventory Transactions
        - Inventory Lots
        - Inventory Locations
    - **Items**
        - Contains all ingredients and recipe names, and links to ingredient and recipe tables
    - **Purchases**
        - 

---

# Goals

The long-term objective is to provide a complete restaurant management platform capable of:

- Inventory Management
- Recipe Costing
- Purchase Tracking
- Vendor Management
- Food Cost Reporting
- Inventory Valuation
- Waste Reporting
- Nutrition Analysis
- POS Integration
- Forecasting
- Production Planning

while remaining modular enough that new functionality can be added without major refactoring.

---

# Design Philosophy

The application follows several guiding principles.

- Domain Driven Design (DDD)
- Layered Architecture
- Repository Pattern
- Service Layer Pattern
- SQLAlchemy ORM
- Transaction-based Inventory
- High testability
- CLI first, UI second

Business logic never belongs inside the user interface.

The CLI, future desktop application, and future API all interact with the same services.

---

# Technologies

- Python 3.13
- SQLAlchemy 2.x
- SQLite
- Alembic
- argparse
- pathlib
- logging
- Decimal arithmetic

---

# Project Structure

inventory_app/

|--cli/

|--ingredients/

|--inventory/

|--items/

|--purchases/

|--recipes/

|--units/

|--vendors/

|--shared/

|--common/


Each domain owns its own:

- models
- repositories
- services
- bootstrap
- importers
- exporters
- reports

---

# Current Features

## Ingredients

- Create
- Import CSV
- Categories
- Subcategories
- Base Units
- Purchase Units
- Count Units
- Inventory Locations

## Units

- Unit Categories
- Global Unit Conversions

## Recipes

- Recipe Components
- Nested Recipes (planned)
- Recipe Costing (planned)

## Inventory

- Transaction based inventory
- FIFO support
- Inventory Lots
- Inventory Events

---

# Future Roadmap

## Phase 1

- Complete CLI
- Reporting
- Conversion Engine v2
- Inventory Adjustments

## Phase 2

- Desktop GUI
- Barcode Support
- Label Printing

## Phase 3

- POS Integration
- Web API
- Mobile Companion

---

# License

Personal project.