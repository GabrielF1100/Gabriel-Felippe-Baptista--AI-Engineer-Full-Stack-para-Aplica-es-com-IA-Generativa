import json
from emporio import tools


def test_tool_search_products():
    res_raw = tools.execute_tool("search_products", {"category": "Violões", "max_price": 1000.0})
    data = json.loads(res_raw)
    assert data["total_found"] > 0
    assert len(data["products"]) > 0


def test_tool_get_product_details_takamine():
    res_raw = tools.execute_tool("get_product_details", {"identifier": "Takamine GD20"})
    data = json.loads(res_raw)
    assert data["found"] is True
    assert data["price_brl"] == 2199.0
    assert data["stock"] == 5


def test_tool_check_promotions():
    res_raw = tools.execute_tool("check_promotions", {})
    data = json.loads(res_raw)
    assert data["total_active"] > 0


def test_tool_get_order_status():
    res_raw = tools.execute_tool("get_order_status", {"order_id_or_tracking": "1"})
    data = json.loads(res_raw)
    assert data["found"] is True
    assert data["order_id"] == 1


def test_tool_consult_store_policies():
    res_raw = tools.execute_tool("consult_store_policies", {"question": "devolução e prazo de arrependimento"})
    data = json.loads(res_raw)
    assert "relevant_policies" in data
    assert len(data["relevant_policies"]) > 0
