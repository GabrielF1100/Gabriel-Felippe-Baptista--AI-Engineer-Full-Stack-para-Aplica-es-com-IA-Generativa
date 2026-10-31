import json
from typing import Any, Dict, List, Optional
from emporio import database
from emporio.policy_retriever import get_policy_retriever


def tool_search_products(
    query: Optional[str] = None,
    category: Optional[str] = None,
    max_price: Optional[float] = None,
    min_price: Optional[float] = None,
    only_in_stock: bool = False,
    limit: int = 5
) -> str:
    """
    Busca produtos no catálogo da loja por nome/modelo, categoria, faixa de preço e estoque.
    """
    prods = database.search_products(
        query=query,
        category_name=category,
        max_price=max_price,
        min_price=min_price,
        only_in_stock=only_in_stock,
        limit=limit
    )
    if not prods:
        return json.dumps({
            "message": "Nenhum produto encontrado com os filtros informados.",
            "total_found": 0,
            "results": []
        }, ensure_ascii=False, indent=2)

    simplified = []
    for p in prods:
        item = {
            "id": p["product_id"],
            "name": p["name"],
            "category": p["category_name"],
            "price_brl": p["price_brl"],
            "stock": p["stock_quantity"],
            "has_discount": p["has_discount"],
            "promotional_price_brl": p["promotional_price_brl"],
            "discount_description": p.get("promotion_name") if p["has_discount"] else None,
            "description": p["description"]
        }
        simplified.append(item)

    return json.dumps({
        "total_found": len(prods),
        "products": simplified
    }, ensure_ascii=False, indent=2)


def tool_get_product_details(identifier: str) -> str:
    """
    Retorna os detalhes completos de um produto específico (preço, estoque, ficha técnica) buscando por ID ou nome/modelo.
    """
    prod = database.get_product_by_identifier(identifier)
    if not prod:
        return json.dumps({
            "error": f"Produto '{identifier}' não foi encontrado no catálogo.",
            "found": False
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "found": True,
        "product_id": prod["product_id"],
        "name": prod["name"],
        "category": prod["category_name"],
        "price_brl": prod["price_brl"],
        "stock": prod["stock_quantity"],
        "in_stock": prod["stock_quantity"] > 0,
        "description": prod["description"],
        "specs": prod.get("specs_parsed", {}),
        "has_discount": prod["has_discount"],
        "promotional_price_brl": prod["promotional_price_brl"],
        "discount_description": prod.get("promotion_name") if prod["has_discount"] else None
    }, ensure_ascii=False, indent=2)


def tool_check_promotions() -> str:
    """
    Lista todas as promoções e descontos ativos atualmente na loja.
    """
    promos = database.get_active_promotions_list()
    if not promos:
        return json.dumps({
            "message": "Não há campanhas promocionais ativas no momento.",
            "promotions": []
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "total_active": len(promos),
        "promotions": promos
    }, ensure_ascii=False, indent=2)


