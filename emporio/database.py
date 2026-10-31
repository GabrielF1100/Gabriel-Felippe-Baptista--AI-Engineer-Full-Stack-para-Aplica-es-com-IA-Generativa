import csv
import json
import sqlite3
from typing import Any, Dict, List, Optional
from emporio import config


def get_connection(db_path=None) -> sqlite3.Connection:
    target = db_path or config.DB_PATH
    conn = sqlite3.connect(target)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path=None, force_reload=False) -> sqlite3.Connection:
    """
    Inicializa o banco de dados SQLite e carrega os dados dos CSVs da Empório da Música.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    # Criação das tabelas
    cur.execute("CREATE TABLE IF NOT EXISTS categories ("
                "category_id INTEGER PRIMARY KEY, "
                "name TEXT, "
                "description TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS customers ("
                "customer_id INTEGER PRIMARY KEY, "
                "name TEXT, "
                "phone TEXT, "
                "email TEXT, "
                "city TEXT)")

    cur.execute("CREATE TABLE IF NOT EXISTS products ("
                "product_id INTEGER PRIMARY KEY, "
                "price_brl REAL, "
                "name TEXT, "
                "category_id INTEGER, "
                "description TEXT, "
                "stock_quantity INTEGER, "
                "status TEXT, "
                "specs TEXT, "
                "created_at TEXT, "
                "FOREIGN KEY (category_id) REFERENCES categories (category_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS promotions ("
                "promotion_id INTEGER PRIMARY KEY, "
                "product_id INTEGER, "
                "discount_percent REAL, "
                "description TEXT, "
                "is_active INTEGER, "
                "FOREIGN KEY (product_id) REFERENCES products (product_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS orders ("
                "order_id INTEGER PRIMARY KEY, "
                "customer_id INTEGER, "
                "order_date TEXT, "
                "status TEXT, "
                "total_brl REAL, "
                "payment_method TEXT, "
                "tracking_code TEXT, "
                "estimated_delivery TEXT, "
                "notes TEXT, "
                "FOREIGN KEY (customer_id) REFERENCES customers (customer_id))")

    cur.execute("CREATE TABLE IF NOT EXISTS order_items ("
                "order_id INTEGER, "
                "quantity INTEGER, "
                "product_id INTEGER, "
                "FOREIGN KEY (order_id) REFERENCES orders (order_id), "
                "FOREIGN KEY (product_id) REFERENCES products (product_id))")

        conn.commit()
    return conn
