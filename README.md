# Restaurant Inventory Management

A Python-based inventory management, recipe costing, purchasing, and reporting system built specifically for restaurants.

This project is designed as a long-term replacement for commercial systems such as ChefTec and Restaurant365 while remaining lightweight, fully customizable, and entirely self-hosted.

Although currently command-line driven, the application is being architected so multiple interfaces (CLI, Desktop, and eventually Web) can all operate from the same business logic.

---

# Current Status

The project is currently under active development.

Completed or mostly complete modules include:

- Units & Unit Categories
- Ingredients
- Ingredient Categories/Subcategories
- Ingredient Unit Conversions
- Vendors
- Vendor Items
- Purchases
- Inventory Lots
- Inventory Transactions
- Inventory Events
- Recipe foundation
- CSV Import framework
- Domain architecture
- SQLAlchemy 2.x models
- Alembic migrations
- Logging system
- Bootstrap/seed system

Upcoming work includes:

- Recipe production
- Inventory adjustments
- Inventory counts
- Reporting
- Food cost analysis
- Waste tracking
- Desktop UI
- POS Integration

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