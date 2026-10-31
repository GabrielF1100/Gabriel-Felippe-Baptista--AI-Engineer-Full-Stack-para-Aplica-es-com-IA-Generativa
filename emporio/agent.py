import json
import re
from typing import Any, Dict, List, Optional
from emporio import config
from emporio import database
from emporio.tools import TOOLS_DEFINITIONS, execute_tool

SYSTEM_PROMPT = """Você é o assistente virtual da Empório da Música, uma tradicional loja de instrumentos musicais fundada em 2008 em Campo Grande/MS.

Sua identidade e tom:
- Seu tom é caloroso, amigável, entusiasmado e profissional — como um colega músico atendendo um amigo.
- Seja objetivo, claro e solícito em português brasileiro.
- Sempre que falar de preços, mencione em Reais (R$ 0.000,00) e cite se há estoque disponível.

Diretrizes obrigatórias da loja:
1. CONSULTA DE DADOS OBRIGATÓRIA: Nunca invente preços, promoções ou estoque. Consulte sempre as ferramentas `search_products`, `get_product_details` ou `check_promotions`. Se um produto estiver sem estoque, avise com transparência e recomende alternativas disponíveis.
2. POLÍTICAS DA LOJA: Para horários, endereço, frete, formas de pagamento e devoluções, use a ferramenta `consult_store_policies`.
   - Endereço: Rua 14 de Maio, 3200 — Centro, Campo Grande - MS.
   - Horário: Seg-Sex 09h às 18h, Sáb 09h às 13h, Domingos e Feriados fechado.
   - Formas de Pagamento: PIX com 5% de desconto à vista (não cumulativo com outras promoções), Cartão de Débito, Boleto e Cartão de Crédito em até 12x sem juros (com valores mínimos de parcela: até 3x sem mínimo exceto <R$50; 4x a 6x mínimo R$80; 7x a 12x mínimo R$100).
   - Frete: Região Metropolitana de Campo Grande tem FRETE GRÁTIS para compras a partir de R$ 500,00 (taxa fixa de R$ 35,00 abaixo desse valor, entrega em 1 a 3 dias úteis). Demais regiões via Correios (PAC/SEDEX) ou Jadlog.
   - Devolução por arrependimento: compras online podem ser devolvidas em até 7 dias corridos após o recebimento, sem custo de frete para o cliente e com reembolso integral na forma de pagamento original.
3. ESCOPO DE PRODUTOS (IMPORTANTE):
   A Empório da Música vende EXCLUSIVAMENTE instrumentos musicais. NÃO vendemos acessórios (palhetas, encordoamentos/cordas, cabos, correias, cases, pedais ou amplificadores). Se o cliente perguntar por algum acessório, informe educadamente que a loja é especializada exclusivamente em instrumentos e sugira procurar lojas parceiras de acessórios.
4. PERGUNTAS FORA DO ESCOPO:
   Se o usuário fizer perguntas completamente desconexas da loja ou da música (ex: receitas de comida, futebol, programação, notícias), responda com simpatia e brevidade, esclarecendo que você é o assistente virtual da Empório da Música focado em instrumentos e atendimento da loja.
"""


class EmporioMusicAgent:
    """
    Agente conversacional da Empório da Música.
    Suporta execução com LLM (OpenAI API / compatível) e modo offline inteligente orientado a intenções.
    """

    def __init__(self, offline_mode: Optional[bool] = None, model: Optional[str] = None):
        database.init_db()
        self.offline_mode = offline_mode if offline_mode is not None else config.OFFLINE_MODE
        self.model = model or config.OPENAI_MODEL
        self.history: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        self.client = None

        if not self.offline_mode:
            if config.OPENAI_API_KEY:
                try:
                    from openai import OpenAI
                    self.client = OpenAI(api_key=config.OPENAI_API_KEY)
                except Exception as e:
                    print(f"[Aviso] Falha ao inicializar cliente OpenAI ({e}). Alternando para modo offline.")
                    self.offline_mode = True
            else:
                self.offline_mode = True

    def reset_history(self):
        """Limpa o histórico e reinicia a sessão de conversa."""
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def chat(self, user_message: str) -> str:
        """
        Processa a mensagem do cliente e retorna a resposta do agente.
        """
        self.history.append({"role": "user", "content": user_message})

        if self.offline_mode:
            response_text = self._respond_offline(user_message)
        else:
            response_text = self._respond_online()

        self.history.append({"role": "assistant", "content": response_text})
        return response_text

    def _respond_online_disabled(self):
        """
        Execução online utilizando OpenAI Function Calling / Tool Calling.
        """
        try:
            # 1ª Chamada: modelo decide se usa ferramentas
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.history,
                tools=TOOLS_DEFINITIONS,
                tool_choice="auto"
            )
            choice = response.choices[0]
            msg = choice.message

            # Se o modelo decidir chamar uma ou mais ferramentas
            if msg.tool_calls:
                # Anexa a decisão do assistente no histórico temporário
                self.history.append(msg)

                for tc in msg.tool_calls:
                    fn_name = tc.function.name
                    try:
                        args = json.loads(tc.function.arguments)
                    except Exception:
                        args = {}
                    tool_output = execute_tool(fn_name, args)

                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "name": fn_name,
                        "content": tool_output
                    })

                # 2ª Chamada: modelo elabora resposta final com os dados das tools
                final_res = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.history
                )
                return final_res.choices[0].message.content or ""
            else:
                return msg.content or ""

        except Exception as e:
            # Fallback transparente para o motor de regras se houver falha de API/rede
            print(f"[Aviso] Erro na API OpenAI ({e}). Usando motor offline de contingência.")
            last_user_msg = ""
            for m in reversed(self.history):
                if isinstance(m, dict) and m.get("role") == "user":
                    last_user_msg = m.get("content", "")
                    break
            return self._respond_offline(last_user_msg)

    def _respond_offline(self, user_text: str) -> str:
        """
        Motor conversacional offline e determinístico da Empório da Música.
        Garante funcionamento imediato e avaliação sem necessidade de chave de API.
        """
        text = user_text.lower().strip()

        # 1. Detecção de produtos fora do escopo da loja (Acessórios)
        acessorios = ["corda", "cordas", "encordoamento", "palheta", "palhetas", "cabo", "cabos", "case", "cases", "capa", "pedal", "pedais", "amplificador", "amplificadores", "caixa de som", "fone", "fones"]
        for ac in acessorios:
            if re.search(rf"\b{ac}\b", text):
                return (
                    "Olá! Aqui na Empório da Música nosso foco é 100% especializado em **instrumentos musicais** "
                    "(como violões, guitarras, baixos, teclados, baterias e sopro). Por isso, **não comercializamos acessórios** "
                    f"como {ac}, cabos, capas ou amplificadores. Recomendamos verificar com lojas especializadas em acessórios em Campo Grande! "
                    "Posso te ajudar a escolher algum instrumento do nosso catálogo?"
                )

        # 2. Perguntas completamente fora do contexto da loja
        fora_de_escopo = ["receita", "bolo", "futebol", "campeonato", "política", "politica", "python", "javascript", "programação", "clima", "previsão do tempo", "filme"]
        if any(re.search(rf"\b{kw}\b", text) for kw in fora_de_escopo):
            return (
                "Poxa, esse assunto foge um pouquinho do meu repertório musical! 🎸 Sou o assistente virtual da **Empório da Música**, "
                "e sou especialista em tirar dúvidas sobre nossos instrumentos musicais, formas de pagamento, pedidos e entregas. "
                "Tem algum instrumento ou detalhe da nossa loja que você gostaria de conhecer?"
            )

        # 3. Consulta de produto específico (ex: Takamine GD20)
        match_prod = re.search(r"(takamine\s+gd20|yamaha\s+c40|yamaha\s+c70|tagima\s+dallas|fender|gibson)", text)
        if "takamine" in text and "gd20" in text:
            raw = execute_tool("get_product_details", {"identifier": "Takamine GD20"})
            data = json.loads(raw)
            if data.get("found"):
                p_brl = f"R$ {data['price_brl']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                stock = data["stock"]
                return (
                    f"O violão **{data['name']}** custa **{p_brl}**!\n\n"
                    f"Temos atualmente **{stock} unidades em estoque** a pronta entrega na loja.\n"
                    f"Ele é um dreadnought excelente com tampo sólido em cedro, timbre encorpado e ótimo para fingerstyle. "
                    f"Além disso, pagando no PIX você garante 5% de desconto à vista, ou pode parcelar em até 12x sem juros no cartão de crédito! Deseja que eu reserve uma unidade para você?"
                )

        # 4. Busca por opções de violões com teto de preço (ex: "violões até R$1000")
        if "viol" in text or "violão" in text or "violao" in text:
            # Tentar extrair preço máximo
            match_price = re.search(r"(?:até|ate|custando até|no máximo|menos de)?\s*(?:r\$)?\s*(\d+)", text)
            max_price = 1000.0
            if match_price and int(match_price.group(1)) > 50:
                max_price = float(match_price.group(1))

            raw = execute_tool("search_products", {
                "category": "Violões",
                "max_price": max_price,
                "only_in_stock": True,
                "limit": 5
            })
            data = json.loads(raw)
            products = data.get("products", [])

            if products:
                lines = [f"Temos ótimas opções de violões disponíveis em estoque custando até R$ {max_price:,.2f}:\n".replace(",", "X").replace(".", ",").replace("X", ".")]
                for p in products:
                    val_str = f"R$ {p['price_brl']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    lines.append(f"• **{p['name']}** — **{val_str}** ({p['stock']} em estoque)")
                lines.append("\nTodos com garantia e opção de parcelamento em até 12x sem juros (ou 5% off no PIX). Qual estilo ou sonoridade você prefere (nylon ou aço)?")
                return "\n".join(lines)

        # 5. Endereço e localização
        if any(w in text for w in ["endereço", "endereco", "localização", "localizacao", "onde fica", "onde estão", "onde voces estao"]):
            raw = execute_tool("consult_store_policies", {"question": "endereco da loja"})
            return (
                "A **Empório da Música** fica na **Rua 14 de Maio, 3200 — Centro, Campo Grande - MS** (CEP 79202-333). "
                "Nosso atendimento é de segunda a sexta-feira das 09:00 às 18:00 e aos sábados das 09:00 às 13:00. "
                "Será um prazer enorme receber sua visita para experimentar nossos instrumentos!"
            )

        # 6. Horário de funcionamento
        if any(w in text for w in ["horario", "horário", "abre", "aberto", "fecha", "fechado"]):
            return (
                "Nosso horário de funcionamento é:\n"
                "• **Segunda a Sexta-feira**: 09:00 às 18:00\n"
                "• **Sábado**: 09:00 às 13:00\n"
                "• **Domingos e Feriados**: Fechado\n"
                "Tanto nossa loja física em Campo Grande quanto nosso canal no WhatsApp atendem dentro desse expediente!"
            )

                return "Posso te ajudar com instrumentos na Empório da Música!"
