import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env se existir
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Caminhos dos arquivos de dados
CATEGORIES_CSV = DATA_DIR / "desafio_tecnico_ai_eng - categories.csv"
CUSTOMERS_CSV = DATA_DIR / "desafio_tecnico_ai_eng - customers.csv"
ORDER_ITEMS_CSV = DATA_DIR / "desafio_tecnico_ai_eng - order_items.csv"
ORDERS_CSV = DATA_DIR / "desafio_tecnico_ai_eng - orders.csv"
PRODUCTS_CSV = DATA_DIR / "desafio_tecnico_ai_eng - products.csv"
PROMOTIONS_CSV = DATA_DIR / "desafio_tecnico_ai_eng - promotions.csv"

# Suporte ao nome do PDF com ou sem acento/encoding
_pdf_default = DATA_DIR / "políticas_da_loja.pdf"
if not _pdf_default.exists():
    for f in DATA_DIR.glob("*pol*ticas*.pdf"):
        _pdf_default = f
        break
POLICIES_PDF = _pdf_default

DB_PATH = BASE_DIR / "emporio.db"

# LLM / Execução
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OFFLINE_MODE = os.getenv("OFFLINE_MODE", "false").lower() in ("true", "1", "yes")
