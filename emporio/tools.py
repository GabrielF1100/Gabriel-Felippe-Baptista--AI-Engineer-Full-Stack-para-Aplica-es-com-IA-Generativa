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


def tool_get_order_status(order_id_or_tracking: str) -> str:
    """
    Consulta o andamento, status de entrega e itens de um pedido pelo ID ou código de rastreamento.
    """
    order = database.get_order_details(order_id_or_tracking)
    if not order:
        return json.dumps({
            "error": f"Pedido ou rastreamento '{order_id_or_tracking}' não localizado no sistema.",
            "found": False
        }, ensure_ascii=False, indent=2)

    return json.dumps({
        "found": True,
        "order_id": order["order_id"],
        "status": order["status"],
        "order_date": order["order_date"],
        "estimated_delivery": order["estimated_delivery"],
        "tracking_code": order["tracking_code"],
        "payment_method": order["payment_method"],
        "total_brl": order["total_brl"],
        "customer_name": order["customer_name"],
        "items": order["items"]
    }, ensure_ascii=False, indent=2)


def tool_consult_store_policies(question: str) -> str:
    """
    Consulta o manual interno de políticas e procedimentos da Empório da Música (horários, formas de pagamento, parcelamento, frete, prazos, trocas, devoluções, garantia e LGPD).
    """
    retriever = get_policy_retriever()
    results = retriever.search_policies(question, top_k=2)

    data = []
    for r in results:
        data.append({
            "section": r["title"],
            "guideline": r["content"]
        })

    return json.dumps({
        "question": question,
        "relevant_policies": data
    }, ensure_ascii=False, indent=2)


# Definição das ferramentas no padrão OpenAI Function Calling
