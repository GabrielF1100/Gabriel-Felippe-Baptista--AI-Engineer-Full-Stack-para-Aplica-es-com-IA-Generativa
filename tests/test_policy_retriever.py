from emporio.policy_retriever import get_policy_retriever


def test_retriever_initialization():
    retriever = get_policy_retriever()
    assert len(retriever.sections) > 0
    assert len(retriever.raw_text) > 0


def test_retrieve_address_and_hours():
    retriever = get_policy_retriever()
    results = retriever.search_policies("Qual o endereço da loja e horário de funcionamento?")
    assert len(results) > 0
    combined = " ".join([r["content"] for r in results]).lower()
    assert "rua 14 de maio" in combined
    assert "campo grande" in combined


def test_retrieve_return_policy():
    retriever = get_policy_retriever()
    results = retriever.search_policies("Me arrependi da minha compra, posso devolver meu pedido?")
    assert len(results) > 0
    top = results[0]["content"].lower()
    assert "7 (sete) dias corridos" in top
    assert "frete" in top


def test_retrieve_shipping_rules():
    retriever = get_policy_retriever()
    results = retriever.search_policies("Como funciona o frete para Campo Grande?")
    assert len(results) > 0
    combined = " ".join([r["content"] for r in results]).lower()
    assert "frete grátis" in combined or "500,00" in combined
