import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INSTANCE_DIR = PROJECT_ROOT / "instance"

DATABASE_PATH = INSTANCE_DIR / "inventory.db"

INVOICE_DIR = INSTANCE_DIR / "invoices"

EXPORT_DIR = INSTANCE_DIR / "exports"

BACKUP_DIR = INSTANCE_DIR / "backups"

LOG_DIR = INSTANCE_DIR / "logs"

INSTANCE_DIR.mkdir(exist_ok=True)
INVOICE_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)



DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{INSTANCE_DIR/'inventory.db'}"
)

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO"
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"
