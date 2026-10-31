from emporio.agent import EmporioMusicAgent


def test_agent_takamine_scenario():
    agent = EmporioMusicAgent(offline_mode=True)
    resp = agent.chat("Quanto custa o Takamine GD20?")
    assert "2.199,00" in resp or "2199" in resp
    assert "5 unidades em estoque" in resp or "5" in resp


def test_agent_violoes_budget_scenario():
    agent = EmporioMusicAgent(offline_mode=True)
    resp = agent.chat("Quais opções de violões disponíveis custando até R$1000?")
    assert "violões" in resp.lower()
    assert "R$" in resp


def test_agent_store_address():
    agent = EmporioMusicAgent(offline_mode=True)
    resp = agent.chat("Qual o endereço da loja?")
    assert "Rua 14 de Maio" in resp
    assert "Campo Grande" in resp


def test_agent_return_policy():
    agent = EmporioMusicAgent(offline_mode=True)
    resp = agent.chat("Me arrependi da minha compra, posso devolver meu pedido?")
    assert "7" in resp
    assert "arrependimento" in resp.lower()


def test_agent_accessories_refusal():
    agent = EmporioMusicAgent(offline_mode=True)
    resp = agent.chat("Vocês vendem encordoamento de nylon e palhetas?")
    assert "não comercializamos acessórios" in resp.lower() or "não vendemos acessórios" in resp.lower()


def test_agent_out_of_scope():
    agent = EmporioMusicAgent(offline_mode=True)
    resp = agent.chat("Qual a melhor receita para fazer pão de queijo?")
    assert "Empório da Música" in resp
    assert "instrumento" in resp.lower()


def test_agent_history_reset():
    agent = EmporioMusicAgent(offline_mode=True)
    agent.chat("Olá!")
    assert len(agent.history) > 1
    agent.reset_history()
    assert len(agent.history) == 1
