import pytest
from emporio import database


@pytest.fixture(scope="module")
def db_conn():
    conn = database.init_db(force_reload=True)
    yield conn
    conn.close()


def test_takamine_gd20_exists(db_conn):
    prod = database.get_product_by_identifier("Takamine GD20")
    assert prod is not None
    assert "Takamine GD20" in prod["name"]
    assert prod["price_brl"] == 2199.0
    assert prod["stock_quantity"] == 5
    assert prod["category_name"] == "Violões"


def test_search_violoes_under_1000(db_conn):
    prods = database.search_products(category_name="Violões", max_price=1000.0, only_in_stock=True)
    assert len(prods) > 0
    for p in prods:
        assert p["price_brl"] <= 1000.0
        assert p["stock_quantity"] > 0
        assert p["category_name"] == "Violões"


def test_active_promotions(db_conn):
    promos = database.get_active_promotions_list()
    assert len(promos) > 0
    for pr in promos:
        assert pr["discount_percent"] > 0
        assert pr["promotional_price_brl"] < pr["original_price_brl"]


def test_order_details(db_conn):
    order = database.get_order_details("1")
    assert order is not None
    assert order["order_id"] == 1
    assert "BRAB1234567BR" in order["tracking_code"]
    assert len(order["items"]) > 0


def test_nonexistent_product(db_conn):
    prod = database.get_product_by_identifier("ProdutoInexistenteX999")
    assert prod is None
