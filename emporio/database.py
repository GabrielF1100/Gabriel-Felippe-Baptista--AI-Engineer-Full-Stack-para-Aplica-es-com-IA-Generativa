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

    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]

    if count == 0 or force_reload:
        cur.execute("DELETE FROM order_items")
        cur.execute("DELETE FROM orders")
        cur.execute("DELETE FROM promotions")
        cur.execute("DELETE FROM products")
        cur.execute("DELETE FROM customers")
        cur.execute("DELETE FROM categories")

        # Ingestão de categories
        if config.CATEGORIES_CSV.exists():
            with open(config.CATEGORIES_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cur.execute(
                        "INSERT INTO categories (category_id, name, description) VALUES (?, ?, ?)",
                        (int(r["category_id"]), r["name"], r.get("description", ""))
                    )

        # Ingestão de customers
        if config.CUSTOMERS_CSV.exists():
            with open(config.CUSTOMERS_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cur.execute(
                        "INSERT INTO customers (customer_id, name, phone, email, city) VALUES (?, ?, ?, ?, ?)",
                        (int(r["customer_id"]), r["name"], r["phone"], r["email"], r.get("city", ""))
                    )

        # Ingestão de products
        if config.PRODUCTS_CSV.exists():
            with open(config.PRODUCTS_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cur.execute(
                        "INSERT INTO products (product_id, price_brl, name, category_id, description, stock_quantity, status, specs, created_at) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            int(r["product_id"]),
                            float(r["price_brl"]),
                            r["name"],
                            int(r["category_id"]),
                            r.get("description", ""),
                            int(r["stock_quantity"]),
                            r.get("status", "active"),
                            r.get("specs", ""),
                            r.get("created_at", "")
                        )
                    )

        # Ingestão de promotions
        if config.PROMOTIONS_CSV.exists():
            with open(config.PROMOTIONS_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cur.execute(
                        "INSERT INTO promotions (promotion_id, product_id, discount_percent, description, is_active) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (
                            int(r["promotion_id"]),
                            int(r["product_id"]),
                            float(r["discount_percent"]),
                            r.get("description", ""),
                            int(r.get("is_active", 0))
                        )
                    )

        # Ingestão de orders
        if config.ORDERS_CSV.exists():
            with open(config.ORDERS_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cur.execute(
                        "INSERT INTO orders (order_id, customer_id, order_date, status, total_brl, payment_method, tracking_code, estimated_delivery, notes) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            int(r["order_id"]),
                            int(r["customer_id"]),
                            r["order_date"],
                            r["status"],
                            float(r["total_brl"]),
                            r.get("payment_method", ""),
                            r.get("tracking_code", ""),
                            r.get("estimated_delivery", ""),
                            r.get("notes", "")
                        )
                    )

        # Ingestão de order_items
        if config.ORDER_ITEMS_CSV.exists():
            with open(config.ORDER_ITEMS_CSV, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for r in reader:
                    cur.execute(
                        "INSERT INTO order_items (order_id, quantity, product_id) VALUES (?, ?, ?)",
                        (int(r["order_id"]), int(r["quantity"]), int(r["product_id"]))
                    )

        conn.commit()

    return conn


def search_products(
    query: Optional[str] = None,
    category_name: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    only_in_stock: bool = False,
    limit: int = 10,
    db_path=None
) -> List[Dict[str, Any]]:
    """
    Pesquisa produtos no catálogo com suporte a filtros de texto, categoria, preço e estoque.
    Retorna também se há promoção ativa para o item e o preço promocional.
    """
    conn = get_connection(db_path)
    cur = conn.cursor()

    sql = """
        SELECT 
            p.product_id,
            p.name,
            p.price_brl,
            p.stock_quantity,
            p.status,
            p.description,
            p.specs,
            c.name as category_name,
            pr.discount_percent,
            pr.description as promotion_name,
            pr.is_active as promotion_active
        FROM products p
        JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN promotions pr ON p.product_id = pr.product_id AND pr.is_active = 1
        WHERE p.status = 'active'
    """
    params: List[Any] = []

    if only_in_stock:
        sql += " AND p.stock_quantity > 0"

    if max_price is not None:
        sql += " AND p.price_brl <= ?"
        params.append(max_price)

    if min_price is not None:
        sql += " AND p.price_brl >= ?"
        params.append(min_price)

    if category_name:
        sql += " AND (LOWER(c.name) LIKE ? OR LOWER(p.name) LIKE ?)"
        params.extend([f"%{category_name.lower()}%", f"%{category_name.lower()}%"])

    if query:
        # Busca flexível por palavras-chave
        keywords = query.strip().split()
        for kw in keywords:
            sql += " AND (LOWER(p.name) LIKE ? OR LOWER(p.description) LIKE ? OR LOWER(c.name) LIKE ?)"
            pat = f"%{kw.lower()}%"
            params.extend([pat, pat, pat])

    sql += " ORDER BY p.price_brl ASC LIMIT ?"
    params.append(limit)

    cur.execute(sql, params)
    rows = cur.fetchall()

    results = []
    for r in rows:
        item = dict(r)
        orig_price = item["price_brl"]
        disc = item.get("discount_percent")
        if disc and item.get("promotion_active"):
            item["promotional_price_brl"] = round(orig_price * (1 - disc / 100.0), 2)
            item["has_discount"] = True
        else:
            item["promotional_price_brl"] = None
            item["has_discount"] = False

        # Parse specs se for JSON válido
        if item.get("specs"):
            try:
                item["specs_parsed"] = json.loads(item["specs"])
            except Exception:
                item["specs_parsed"] = {}
        results.append(item)

    conn.close()
    return results


