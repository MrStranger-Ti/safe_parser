import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os.path
import configparser

from src.parser.format.formatters import (
    SimpleFieldsFormatter,
    ImagesFormatter,
    CharacteristicsFormatter,
    DefaultFieldsFormatter,
    DescriptionFormatter,
    GuarantyFormatter,
)

# Main

if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent.parent

_config = configparser.ConfigParser()
_config.read(BASE_DIR / "config.ini", encoding="utf-8")


# Logging

LOG_LEVELS = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}

LOG_LEVEL = _config.get("optional", "LOG_LEVEL")
if LOG_LEVEL not in LOG_LEVELS:
    LOG_LEVEL = "INFO"

os.makedirs(BASE_DIR / "logs", exist_ok=True)

logging.basicConfig(
    level=LOG_LEVEL,
    handlers=[
        RotatingFileHandler(
            BASE_DIR / "logs/log",
            mode="a",
            backupCount=5,
            maxBytes=100000,
        )
    ],
    datefmt="%d.%m.%Y-%H:%M:%S",
    format="[%(levelname)s | %(asctime)s | %(module)s:%(lineno)s] %(message)s",
)

log = logging.getLogger(__name__)


# Parsing

URL = _config.get("required", "URL")
if not URL:
    log.error("No URL. Set URL option in config.ini")
    raise ValueError("URL option is required")

DEFAULT_FORMATTERS = [
    DefaultFieldsFormatter,
    SimpleFieldsFormatter,
    DescriptionFormatter,
    ImagesFormatter,
    CharacteristicsFormatter,
    GuarantyFormatter,
]


# Excel

TEMPLATE_PATH = BASE_DIR / "templates/template.xlsx"

if not os.path.exists(TEMPLATE_PATH):
    msg = f"Path {TEMPLATE_PATH} does not exists."
    log.error(msg)
    raise FileNotFoundError(msg)

RESULT_FILE_NAME = _config.get("optional", "RESULT_FILE_NAME") or "result.xlsx"

RESULT_FILE_DIR = _config.get("optional", "RESULT_FILE_DIR")
RESULT_FILE_DIR = (
    Path(RESULT_FILE_DIR) / RESULT_FILE_NAME
    if RESULT_FILE_DIR
    else BASE_DIR / RESULT_FILE_NAME
)

SHEET_NAME = "Ассортимент"

COLS = {
    "id": 2,  # SKU
    "name": 4,  # Название
    "manufacturer": 6,  # Бренд
    "description": 8,  # Описание
    "price22": 11,  # Цена по умолчанию
    "vat": 16,  # НДС
    "category": 17,  # Категория
    "images": 19,  # Изображения товара
    "warranty": 21,  # Гарантия
    "country": 22,  # Страна
    "characteristics": 23,  # Характеристики
    "unit_measurement": 24,  # Единица измерения
    "available": 25,  # Доступность
    "weight": 34,  # Вес
}

START_ROW = 5
START_COL = 2
