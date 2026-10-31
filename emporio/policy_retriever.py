import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pypdf
from emporio import config


class PolicyRetriever:
    """
    Mecanismo de indexação e recuperação das políticas internas da Empório da Música.
    Extrai e estrutura as regras do PDF 'políticas_da_loja.pdf' para consulta pelo agente.
    """

    def __init__(self, pdf_path: Optional[Path] = None):
        self.pdf_path = pdf_path or config.POLICIES_PDF
        self.raw_text: str = ""
        self.sections: List[Dict[str, str]] = []
        self._load_and_index()

    def _load_and_index(self):
        """
        Lê o PDF e fragmenta o documento em seções temáticas para retrieval de alta precisão.
        """
        if self.pdf_path and Path(self.pdf_path).exists():
            try:
                reader = pypdf.PdfReader(str(self.pdf_path))
                pages_text = []
                for p in reader.pages:
                    txt = p.extract_text() or ""
                    # Limpeza de espaçamentos estranhos do PDF
                    txt = re.sub(r"[ \t]+", " ", txt)
                    pages_text.append(txt)
                self.raw_text = "\n".join(pages_text)
            except Exception as e:
                self.raw_text = f"Erro ao carregar PDF: {e}"

        # Segmentação por tópicos do manual oficial
        self.sections = [
            {
                "id": "sobre_loja",
                "title": "1. Sobre a Empório da Música e Escopo de Produtos",
                "keywords": ["sobre", "historia", "fundacao", "endereco", "localizacao", "onde", "fica", "cnpj", "telefone", "whatsapp", "acessorios", "escopo", "missao", "campo grande"],
                "content": (
                    "A Empório da Música foi fundada em 2008 em Campo Grande/MS (Rua 14 de Maio, 3200 — Centro, CEP 79202-333). "
                    "Telefone/WhatsApp: (67) 3341-4444 / (67) 3321-4500. E-mail: contato@emporiodamusica.com.br. CNPJ: 12.345.678/0001-90.\n"
                    "REGRA FUNDAMENTAL DE ESCOPO: Trabalhamos EXCLUSIVAMENTE com instrumentos musicais (guitarras, baixos, violões, "
                    "baterias, teclados, sopro, cordas orquestrais e ukuleles). NÃO comercializamos acessórios como cordas, palhetas, "
                    "cabos, cases, pedais ou amplificadores. Dúvidas sobre acessórios devem ser educadamente redirecionadas para lojas parceiras."
                )
            },
            {
                "id": "horario_funcionamento",
                "title": "2. Horário de Funcionamento",
                "keywords": ["horario", "funcionamento", "aberto", "abre", "fecha", "sabado", "domingo", "feriado", "expediente", "atendimento"],
                "content": (
                    "Horário de Funcionamento:\n"
                    "- Segunda a Sexta-feira: 09:00 às 18:00\n"
                    "- Sábado: 09:00 às 13:00\n"
                    "- Domingos e Feriados: Fechado.\n"
                    "O atendimento presencial e via WhatsApp seguem este mesmo horário. Fora do expediente, o assistente virtual informa o retorno."
                )
            },
            {
                "id": "formas_pagamento",
                "title": "3. Formas de Pagamento e Parcelamento",
                "keywords": ["pagamento", "pagar", "forma", "pix", "cartao", "credito", "debito", "boleto", "parcelamento", "parcelas", "juros", "desconto"],
                "content": (
                    "Formas de Pagamento e Condições:\n"
                    "- PIX: Pagamento à vista com 5% de desconto sobre o preço de tabela (não cumulativo com promoções ativas).\n"
                    "- Cartão de Débito: Pagamento à vista, todas as bandeiras.\n"
                    "- Boleto Bancário: Pagamento à vista, compensação em até 3 dias úteis.\n"
                    "- Cartão de Crédito: Até 12x sem juros.\n"
                    "Regras de Parcelamento no Cartão:\n"
                    "  * Em até 3x sem juros: sem valor mínimo de parcela (exceto abaixo de R$ 50,00).\n"
                    "  * De 4x a 6x sem juros: parcela mínima de R$ 80,00.\n"
                    "  * De 7x a 12x sem juros: parcela mínima de R$ 100,00.\n"
                    "- Combinação de formas de pagamento (ex.: PIX + cartão) é permitida para compras acima de R$ 2.000,00."
                )
            },
            {
                "id": "trocas_devolucoes",
                "title": "4. Política de Trocas e Devoluções (Arrependimento e Garantia)",
                "keywords": ["troca", "trocar", "devolucao", "devolver", "arrependi", "arrependimento", "cancelar", "defeito", "quebrado", "preferencia", "prazo", "reembolso"],
                "content": (
                    "Diretrizes de Trocas e Devoluções (Código de Defesa do Consumidor):\n"
                    "- Direito de Arrependimento (Compras Online): O cliente pode solicitar a devolução em até 7 (sete) dias corridos "
                    "após o recebimento do produto, sem necessidade de justificativa. O produto deve estar em sua embalagem original, sem sinais "
                    "de uso, com manuais e acessórios. O reembolso é feito na mesma forma de pagamento em até 10 dias úteis. O frete de devolução é por conta da loja!\n"
                    "- Troca por Defeito: Defeitos de fabricação podem ser trocados diretamente com a loja em até 30 dias corridos da compra. "
                    "Após 30 dias, deve-se acionar a garantia do fabricante.\n"
                    "- Troca por Preferência (cor, modelo): permitida em até 7 dias se em perfeito estado e com disponibilidade em estoque.\n"
                    "- Itens NÃO elegíveis para troca: Instrumentos com regulagem/setup personalizado sob encomenda, produtos em liquidação 'venda final', "
                    "e boquilhas de instrumentos de sopro por motivos de higiene."
                )
            },
            {
                "id": "frete_entregas",
                "title": "5. Frete e Prazos de Entrega",
                "keywords": ["frete", "entrega", "prazo", "envio", "entregar", "campo grande", "correios", "sedex", "pac", "jadlog", "rastreamento", "rastrear", "codigo"],
                "content": (
                    "Políticas de Frete e Entrega:\n"
                    "- Região Metropolitana de Campo Grande/MS: FRETE GRÁTIS para pedidos acima de R$ 500,00! Para pedidos abaixo de R$ 500,00, taxa fixa de R$ 35,00. "
                    "Prazo de 1 a 3 dias úteis por motoboy próprio (o cliente é contatado por telefone antes).\n"
                    "- Outras Cidades e Estados: Envio via Correios (PAC: 5 a 12 dias úteis; SEDEX: 2 a 5 dias úteis) ou Jadlog (3 a 8 dias úteis). "
                    "Cálculo automático por CEP, peso e dimensões. Instrumentos de grande porte podem exigir cotação especial.\n"
                    "- Seguro: Todos os envios têm seguro contra extravios e avarias.\n"
                    "- Código de Rastreamento: Enviado por e-mail e WhatsApp no formato 'BR' + 9 dígitos + 'BR' (ex: BRAB1234567BR) e consultável nos Correios ou Jadlog."
                )
            },
            {
                "id": "promocoes_regras",
                "title": "6. Regras de Promoções e Descontos",
                "keywords": ["promocao", "promocoes", "desconto", "black friday", "aniversario", "cupom", "liquidacao", "cumulativo"],
                "content": (
                    "Regras de Promoções:\n"
                    "- Campanhas: Aniversário da Loja (Agosto: 10% a 25%), Black Friday (Novembro: 15% a 30%), Volta às Aulas (Fevereiro), Semana do Músico (Novembro).\n"
                    "- Não-cumulatividade: Promoções NÃO são cumulativas. O desconto de 5% do PIX NÃO se aplica sobre itens já em promoção.\n"
                    "- Estoque: Promoções válidas enquanto durarem os estoques, sem reserva de preço após o término.\n"
                    "- Transparência: Preços promocionais devem sempre exibir o preço original e o percentual de desconto."
                )
            },
            {
                "id": "atendimento_persona",
                "title": "7. Tom de Atendimento e Conduta",
                "keywords": ["tom", "atendimento", "persona", "amigo", "reclamacao", "fora de estoque", "musica", "cordialidade"],
                "content": (
                    "Diretrizes da Persona e Atendimento:\n"
                    "- Tom de voz: Informal porém profissional, amigável, acolhedor e atencioso — 'como se estivesse conversando com um amigo que entende de música'.\n"
                    "- Precisão: Nunca passar informações de preço ou estoque sem consultar a base de dados real.\n"
                    "- Produtos fora de estoque: Avisar com transparência e sugerir alternativas semelhantes disponíveis no catálogo.\n"
                    "- Reclamações: Ouvir com empatia e registrar com prazo de retorno de até 24 horas úteis."
                )
            },
            {
                "id": "garantia",
                "title": "8. Garantia e Cobertura",
                "keywords": ["garantia", "defeito", "legal", "fabricante", "mau uso", "assistencia", "cobertura", "cdc"],
                "content": (
                    "Políticas de Garantia:\n"
                    "- Garantia Legal: 90 (noventa) dias contra defeitos de fabricação conforme o CDC.\n"
                    "- Garantia do Fabricante: De 6 meses a 2 anos, conforme o certificado do instrumento.\n"
                    "- O que NÃO é coberto: Desgaste natural (cordas, trastes, feltros), mau uso, quedas, umidade excessiva ou modificações por terceiros."
                )
            },
            {
                "id": "privacidade_lgpd",
                "title": "9. Privacidade e Proteção de Dados (LGPD)",
                "keywords": ["lgpd", "privacidade", "dados", "dados pessoais", "seguranca", "exclusao"],
                "content": (
                    "A Empório da Música cumpre rigorosamente a LGPD (Lei nº 13.709/2018). Os dados dos clientes são utilizados unicamente para "
                    "processamento de pedidos, entrega e comunicação autorizada. Não há compartilhamento com terceiros para marketing."
                )
            }
        ]

        def search_policies(self, query: str, top_k: int = 2):
        return self.sections[:top_k]
