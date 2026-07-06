from inventory_app.cli.main import main
from inventory_app.shared.logging import setup_logging


setup_logging()

if __name__ == "__main__":
    main()