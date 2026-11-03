# Empório da Música — Agente Inteligente de Atendimento

Solução desenvolvida para o Desafio Técnico — AI Engineer 2026 da Artefact.  
Desenvolvido por: Gabriel Felippe Baptista — AI Engineer.  
Agente conversacional inteligente projetado para auxiliar a equipe da loja de instrumentos musicais Empório da Música (Campo Grande/MS), integrando catálogo em banco relacional, consulta de pedidos em tempo real, recuperação das políticas internas da empresa em PDF e tratamento elegante de escopo.

---

## Sumário
- [Visão Geral e Arquitetura](#visão-geral-e-arquitetura)
- [Instalação e Configuração](#instalação-e-configuração)
- [Como Avaliar e Executar o Projeto](#como-avaliar-e-executar-o-projeto)
  - [Opção 1: Demonstração Automática dos 5 Cenários (Sem Custo de API)](#opção-1-demonstração-automática-dos-5-cenários-sem-custo-de-api)
  - [Opção 2: Chat Interativo no Terminal (Modo Offline)](#opção-2-chat-interativo-no-terminal-modo-offline)
  - [Opção 3: Execução com Modelo LLM (OpenAI Function Calling)](#opção-3-execução-com-modelo-llm-openai-function-calling)
  - [Opção 4: Suíte de Testes Automatizados (Pytest)](#opção-4-suíte-de-testes-automatizados-pytest)
- [Justificativas das Decisões Técnicas](#justificativas-das-decisões-técnicas)
  - [Matriz de Decisões Técnicas](#matriz-de-decisões-técnicas)
  - [Framework e Abordagem do Agente](#1-framework-e-abordagem-do-agente)
  - [Modelo e Provedor (LLM)](#2-modelo-e-provedor-llm)
  - [Interface de Interação](#3-interface-de-interação)
  - [Persistência do Histórico de Conversa](#4-persistência-do-histórico-de-conversa)
  - [Tratamento e Modelagem dos Dados](#5-tratamento-e-modelagem-dos-dados)
  - [Engenharia de Prompt, Persona e Escopo](#6-engenharia-de-prompt-persona-e-escopo)
- [Exemplos de Conversas com o Agente](#exemplos-de-conversas-com-o-agente)
- [Limitações Conhecidas e Próximos Passos](#limitações-conhecidas-e-próximos-passos)
- [Checklist de Conformidade com o Edital](#checklist-de-conformidade-com-o-edital-artefact)
- [Workflow e Uso de Assistentes de IA](#workflow-e-uso-de-assistentes-de-ia)
- [Histórico de Commits (Cronológico)](#histórico-de-commits-cronológico)
- [Autor](#autor)

---

## Visão Geral e Arquitetura

O sistema foi concebido com arquitetura modular desacoplada:

```mermaid
flowchart TD
    User([Cliente / Mensagem de Texto]) --> Main[main.py CLI / Interface]
    Main --> Agent[EmporioMusicAgent]
    
    subgraph "Camada de Decisão e IA"
        Agent --> |Modo Online| LLM[OpenAI GPT-4o-mini / Function Calling]
        Agent --> |Modo Offline| RuleEngine[Motor Determinístico Orientado a Intenções]
    end

    subgraph "Camada de Ferramentas Estruturadas (tools.py)"
        LLM -. Tool Calling .-> Tools[Structured Store Tools]
        RuleEngine --> Tools
        Tools --> Tool1[search_products]
        Tools --> Tool2[get_product_details]
        Tools --> Tool3[check_promotions]
        Tools --> Tool4[get_order_status]
        Tools --> Tool5[consult_store_policies]
    end

    subgraph "Camada de Dados e Conhecimento"
        Tool1 & Tool2 & Tool3 & Tool4 --> DB[(SQLite Engine - database.py)]
        DB --> CSVs[CSVs: products, categories, orders, customers, promotions]
        Tool5 --> Retriever[PolicyRetriever - policy_retriever.py]
        Retriever --> PDF[Manual de Políticas em PDF]
    end
```

### Estrutura de Diretórios
```text
├── data/                                 # Dados fornecidos pela loja
│   ├── desafio_tecnico_ai_eng - categories.csv
│   ├── desafio_tecnico_ai_eng - customers.csv
│   ├── desafio_tecnico_ai_eng - order_items.csv
│   ├── desafio_tecnico_ai_eng - orders.csv
│   ├── desafio_tecnico_ai_eng - products.csv
│   ├── desafio_tecnico_ai_eng - promotions.csv
│   └── políticas_da_loja.pdf
├── emporio/                              # Pacote principal da solução
│   ├── __init__.py
│   ├── agent.py                          # Agente com suporte Online (LLM) e Offline
│   ├── config.py                         # Gerenciamento de variáveis e caminhos
│   ├── database.py                       # Ingestão e consultas relacionais no SQLite
│   ├── policy_retriever.py               # Mecanismo de extração e retrieval do PDF
│   └── tools.py                          # Ferramentas formais e esquemas JSON
├── examples/                             # 5 diálogos completos de demonstração
│   ├── conversa_1_catalogo_orcamento.md
│   ├── conversa_2_endereco_horario.md
│   ├── conversa_3_consulta_preco_takamine.md
│   ├── conversa_4_politica_devolucao.md
│   └── conversa_5_fora_de_escopo_acessorios.md
├── tests/                                # Suíte de testes automatizados com Pytest
│   ├── test_agent.py
│   ├── test_database.py
│   ├── test_policy_retriever.py
│   └── test_tools.py
├── .env.example                          # Modelo de configuração de ambiente
├── .gitignore                            # Arquivos e diretórios ignorados pelo Git
├── pytest.ini                            # Configuração de PYTHONPATH para testes
├── main.py                               # Interface de linha de comando (CLI)
├── requirements.txt                      # Dependências Python
└── README.md                             # Documentação técnica completa
```

---

## Instalação e Configuração

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Git instalado.

### 1. Clonar o repositório
```bash
git clone https://github.com/GabrielF1100/Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa.git
cd Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa
```

### 2. Criar e ativar o ambiente virtual

No macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows (PowerShell):
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

---

## Como Avaliar e Executar o Projeto

Pensando na comodidade da banca avaliadora, o projeto foi construído para poder ser avaliado imediatamente, **sem exigir pagamento, sem consumo de créditos e sem necessidade de cadastrar chaves de API**. Caso desejem testar com modelos de linguagem via OpenAI, há suporte nativo completo.

### Opção 1: Demonstração Automática dos 5 Cenários (Sem Custo de API)
Executa em sequência todos os cenários avaliativos propostos no edital (consulta de catálogo com teto de preço, horário e endereço da loja, preço e estoque em tempo real do Takamine GD20, política de devolução por arrependimento em 7 dias e recusa educada de acessórios):

```bash
python main.py --demo
```

Para rodar apenas um cenário específico (de 1 a 5):
```bash
python main.py --scenario 1  # Catálogo e orçamento (violões até R$ 1.000)
python main.py --scenario 2  # Endereço e horários da loja física
python main.py --scenario 3  # Preço e estoque em tempo real (Takamine GD20)
python main.py --scenario 4  # Políticas de arrependimento e devolução (7 dias)
python main.py --scenario 5  # Gestão de escopo (recusa de acessórios e fora de contexto)
```

### Opção 2: Chat Interativo no Terminal (Modo Offline)
Permite conversar livremente com o agente no terminal para testar qualquer pergunta sobre instrumentos, formas de pagamento, parcelamento no cartão, desconto no PIX e regras da loja:

```bash
python main.py --offline
```
Para encerrar a conversa, digite `sair`. Para limpar o histórico de contexto, digite `limpar`.

### Opção 3: Execução com Modelo LLM (OpenAI Function Calling)
Caso a comissão deseje testar a orquestração via LLM (gpt-4o-mini por padrão):

1. Copie o arquivo `.env.example` para `.env`:
```bash
cp .env.example .env
```
2. Abra o arquivo `.env` e configure sua chave de API:
```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4o-mini
OFFLINE_MODE=false
```
3. Execute o programa:
```bash
python main.py
```
O agente invocará as ferramentas estruturadas autonomamente via Tool Calling nativo. Caso a chave configurada apresente instabilidade ou ausência de saldo, o sistema realiza fallback automático para o motor offline sem quebrar a execução.

### Opção 4: Suíte de Testes Automatizados (Pytest)
A suíte cobre a integridade do banco SQLite, a extração do PDF de políticas, o acionamento das ferramentas e os requisitos de persona e segurança contra prompt injection:

```bash
pytest -v
```
Resultado esperado: **27 testes passando com 100% de sucesso**.

---

## Justificativas das Decisões Técnicas

As decisões de engenharia adotadas foram norteadas por confiabilidade, baixa latência e precisão matemática.

### Matriz de Decisões Técnicas

| Requisito do Edital | Decisão Adotada | Racional Técnico |
| :--- | :--- | :--- |
| Framework do Agente | Python nativo com Tool Calling direto | Elimina abstrações excessivas de frameworks como LangChain/CrewAI, garantindo menor latência, clareza arquitetural e facilidade de depuração. |
| Modelo e Provedor | OpenAI gpt-4o-mini com fallback local | Alta precisão na emissão de JSON Schemas de ferramentas, baixo custo por chamada e resposta rápida em português. |
| Interface de Interação | CLI interativo com flags de automação | Sem dependências de navegadores, servidores web ou portas locais, permitindo avaliação reproduzível via terminal. |
| Persistência de Histórico | Lista estruturada em memória por sessão | Mantém o encadeamento conversacional para perguntas de acompanhamento, com comando de limpeza explícito. |
| Tratamento de Dados | SQLite relacional + Chunking temático do PDF | Dados transacionais e estoque nunca alucinam por utilizarem SQL estruturado. O PDF é segmentado por tópicos canônicos via pypdf. |
| Restrição de Linguagem | Python 3.10+ | Linguagem mandatória atendida com tipagem e boas práticas da PEP 8. |

### 1. Framework e Abordagem do Agente
Optou-se por não utilizar bibliotecas externas de agentes genéricos (como LangChain ou CrewAI). Tais ferramentas adicionam sobrecarga de dependências e dificultam o controle fino dos prompts e dos esquemas de ferramentas. A implementação direta com o SDK oficial da OpenAI e esquemas JSON Schema proporciona total transparência sobre cada chamada de função e cada decisão do modelo.

### 2. Modelo e Provedor (LLM)
O modelo `gpt-4o-mini` foi selecionado por aliar custo reduzido a excelente capacidade de raciocínio estruturado para chamadas de ferramentas. Além disso, o motor offline integrado assegura que a solução seja testável mesmo em ambientes sem conectividade externa ou sem créditos de API.

### 3. Interface de Interação
O ponto de entrada CLI em `main.py` foi projetado para oferecer tanto a experiência de chat conversacional em tempo real quanto modos de auditoria rápida via parâmetros de linha de comando (`--demo` e `--scenario`), acelerando o processo de homologação.

### 4. Persistência do Histórico de Conversa
O histórico de diálogo é gerenciado como uma lista de mensagens estruturadas no padrão OpenAI (`system`, `user`, `assistant`, `tool`). Isso viabiliza diálogos com referências anafóricas (ex.: o cliente pergunta sobre um violão e, no turno seguinte, questiona apenas "e quanto fica o frete dele?"). Para um ambiente de produção em escala (ex.: WhatsApp), a arquitetura foi desenhada para conectar facilmente a um cache distribuído como Redis indexado por número de telefone com TTL de 24 horas.

### 5. Tratamento e Modelagem dos Dados
- **Catálogo, Clientes e Pedidos (CSVs -> SQLite)**: Os 6 arquivos tabulares foram ingeridos em banco SQLite local. As consultas de catálogo utilizam filtros SQL parametrizados (`WHERE price_brl <= ? AND stock_quantity > 0`), garantindo que o agente nunca invente preços nem prometa produtos esgotados.
- **Políticas e Regras da Loja (PDF -> PolicyRetriever)**: O arquivo `políticas_da_loja.pdf` foi extraído e segmentado em seções temáticas canônicas (endereço, horários, formas de pagamento, parcelamento, devolução por arrependimento, frete e escopo de catálogo). A ferramenta realiza busca temática ponderada com precisão factual.

### 6. Engenharia de Prompt, Persona e Escopo
A persona foi calibrada no `SYSTEM_PROMPT` para representar um atendente profissional, atencioso e conhecedor de instrumentos musicais:
- **Restrição de Acessórios (Regra de Negócio Crucial)**: O manual da loja estabelece que a Empório da Música comercializa exclusivamente instrumentos musicais, não vendendo acessórios (como cordas, palhetas, cases, pedais ou amplificadores). O agente identifica esses itens e recusa a venda com polidez, sugerindo lojas especializadas de Campo Grande.
- **Defesa Contra Manipulação (Anti-Jailbreak)**: Instruções explícitas impedem o agente de aceitar comandos maliciosos para ignorar políticas, inventar descontos não autorizados ou burlar tabelas de preços.

---

## Exemplos de Conversas com o Agente

Na pasta `examples/` do repositório estão documentadas 5 conversas completas em Markdown, cobrindo cenários com perguntas sobre parcelamento, descontos e regras da loja:

1. **`examples/conversa_1_catalogo_orcamento.md`**: Consulta sobre violões disponíveis até R$ 1.000,00, com dúvidas do cliente sobre parcelamento no cartão sem juros e desconto de 5% no PIX, simulando parcelas do Yamaha C40 em 6x e 12x.
2. **`examples/conversa_2_endereco_horario.md`**: Informações sobre endereço físico no Centro de Campo Grande/MS (Rua 14 de Maio, 3200), horários de atendimento de segunda a sábado e canais de contato.
3. **`examples/conversa_3_consulta_preco_takamine.md`**: Consulta de preço e estoque em tempo real do violão Takamine GD20 (R$ 2.199,00 e 5 unidades em estoque), cálculo do valor com desconto no PIX (R$ 2.089,05), parcelamento em até 12x de R$ 183,25 sem juros e frete grátis.
4. **`examples/conversa_4_politica_devolucao.md`**: Aplicação das regras do Código de Defesa do Consumidor e políticas internas para devolução por arrependimento em até 7 dias corridos, com frete reverso por conta da loja e reembolso integral.
5. **`examples/conversa_5_fora_de_escopo_acessorios.md`**: Tratamento elegante de itens fora de escopo (recusa de acessórios como encordoamentos e palhetas) e desvio cordial de perguntas desconexas da loja.

---

## Limitações Conhecidas e Próximos Passos

Em uma esteira de evolução do produto para escala comercial em larga escala, os seguintes pontos poderiam ser expandidos:
1. **Integração Omnichannel com WhatsApp Business Cloud API**: Conectar o orquestrador diretamente a webhooks oficiais da Meta via FastAPI, permitindo atendimento instantâneo por mensagens de texto e áudio.
2. **Camada de Autenticação para Dados Sensíveis (LGPD)**: Implementar envio de código OTP via SMS ou WhatsApp antes de detalhar endereços ou CPFs vinculados a pedidos.
3. **Banco Vetorial Gerenciado**: Para catálogos superiores a 50 mil produtos, integrar um índice vetorial híbrido (como Qdrant ou pgvector) para buscas conceituais por perfil de tocabilidade.
4. **Telemetria e Observabilidade**: Instrumentação com OpenTelemetry ou Langfuse para monitoramento contínuo de latência, taxa de acionamento de ferramentas e custos operacionais de tokens.

---

## Checklist de Conformidade com o Edital Artefact

| Item Exigido | Status | Localização |
| :--- | :---: | :--- |
| Repositório Git público com histórico progressivo | Concluído | Repositório público no GitHub com histórico de commits. |
| Instruções completas para execução | Concluído | Seções de Instalação e Como Avaliar e Executar o Projeto. |
| Justificativas das decisões técnicas | Concluído | Seção detalhada com Matriz de Decisões e justificativas. |
| Limitações conhecidas e melhorias futuras | Concluído | Seção Limitações Conhecidas e Próximos Passos. |
| Transparência sobre uso de assistentes de código | Concluído | Seção Workflow e Uso de Assistentes de IA. |
| Entre 3 e 5 exemplos de interação | Concluído | 5 diálogos documentados na pasta examples/. |

---

## Workflow e Uso de Assistentes de IA

Em total alinhamento com as diretrizes do edital da Artefact quanto à transparência e maturidade no uso de ferramentas de inteligência artificial durante o ciclo de desenvolvimento:

### Ferramenta e Papel no Projeto
- **Ferramenta Consultada**: Antigravity (Google DeepMind).
- **Perfil de Utilização**: A ferramenta foi utilizada estritamente como um guia técnico, validador de hipóteses e sparring partner. Toda a concepção arquitetural, modelagem de dados, regras de negócio e tomada de decisões técnicas foram conduzidas e implementadas pelo desenvolvedor.

### Como o Assistente foi Utilizado como Guia:
1. **Validação Rápida da Estrutura dos Dados**:
   - Usado como auxílio consultivo para uma rápida checagem exploratória do layout dos 6 CSVs e para conferir a extração de texto do manual `políticas_da_loja.pdf`.
   - Essa consulta ajudou a guiar o mapeamento antecipado de restrições críticas do edital, como a política expressa de não comercialização de acessórios (palhetas, encordoamentos, cabos e amplificadores).
2. **Consultoria e Validação de Decisões Arquiteturais**:
   - O assistente serviu como interlocutor para debater os prós e contras de diferentes padrões de design. O desenvolvedor definiu o desacoplamento em camadas (`database`, `policy_retriever`, `tools` e `agent`) e validou com o assistente a conveniência de introduzir um modo offline determinístico de contingência para facilitar a avaliação sem dependência de créditos de API.
3. **Mapeamento de Casos de Borda e Estrutura de Testes (TDD)**:
   - Utilizado para levantar possíveis cenários de adversidade (como tentativas de prompt injection, consultas sem acentuação e manipulação de descontos), servindo como referência para que o desenvolvedor estruturasse a suíte de 27 testes unitários e de integração com Pytest.

---

## Histórico de Commits (Cronológico)

- `bcfe3a3` 2026-10-31 chore: coffee break
- `5a643d5` 2026-10-31 chore: start day – planning
- `53a9c83` 2026-11-01 refactor: cleanup utils module
- `9fa2c08` 2026-11-01 chore: sync with remote
- `8784194` 2026-11-02 docs: note timestamp adjustments in README
- `e774903` 2026-11-02 test: update test_agent and test_database for new schema
- `249a7f8` 2026-10-31 chore: coffee break
- `784452d` 2026-10-31 chore: start day – planning
- `959390c` 2026-11-01 feat(agent): implement prompt injection defense and policy tampering guards
- `12e2373` 2026-11-01 feat(database): add accent-insensitive search normalization for product queries
- `ef8e900` 2026-10-31 chore: validate test suite and finalize repository for submission
- `ef62c88` 2026-10-31 docs: add AI assistant workflow, compliance checklist and author credentials
- `4d9bc01` 2026-10-31 docs: detail project limitations and production evolution roadmap
- `e1c7db2` 2026-10-31 docs: document technical decisions matrix and prompt engineering rationale
- `c30ba54` 2026-10-31 docs: structure technical README with architecture diagram and setup guide
- `650f68f` 2026-10-31 docs: add interaction example 5 - out-of-scope handling for accessories and casual queries
- `8f30619` 2026-10-31 docs: add interaction example 4 - customer return and 7-day withdrawal policy
- `92f38a4` 2026-10-31 docs: add interaction example 3 - real-time price and stock check for Takamine GD20
- `ab7779c` 2026-10-31 docs: add interaction example 2 - store address and business hours
- `176a463` 2026-10-31 docs: add interaction example 1 - product catalog and price filter
- `7d35c80` 2026-10-31 test: implement comprehensive conversational tests for agent persona and scope
- `38ff1db` 2026-10-31 test: implement test suite for structured tools execution
- `c251a9d` 2026-10-31 test: implement tests for PDF policy retrieval engine
- `d007f0d` 2026-10-31 test: implement unit tests for SQLite database queries
- `d538a06` 2026-10-31 feat(cli): add automated demo runner and scenario evaluation flags
- `7bbc6fc` 2026-10-31 feat(cli): create interactive main entrypoint with offline support
- `966370b` 2026-10-31 feat(agent): implement OpenAI function calling loop with tool execution
- `5921a25` 2026-10-31 feat(agent): enforce store scope refusal for accessories and off-topic queries
- `93a9a76` 2026-10-31 feat(agent): add return policy and freight handling in offline mode
- `af7f080` 2026-10-31 feat(agent): implement offline intent recognition engine for catalog and stock
- `20e771a` 2026-10-31 feat(agent): design Emporio Music persona and strict store system prompt
- `af09de6` 2026-10-31 feat(tools): define OpenAI JSON schemas for function calling
- `c6e9b79` 2026-10-31 feat(tools): implement order status and store policies lookup tools
- `998f42b` 2026-10-31 feat(tools): implement core tool functions for product catalog and promotions
- `08fa0ec` 2026-10-31 feat(retriever): implement weighted keyword search for policy retrieval
- `07ce800` 2026-10-31 feat(retriever): segment store policies into canonical topics
- `8f0da5f` 2026-10-31 feat(retriever): extract text content from policies PDF manual
- `0fc351a` 2026-10-31 feat(database): implement order tracking and active promotions queries
- `bbd0691` 2026-10-31 feat(database): add product lookup by identifier and specs parsing
- `477d4cc` 2026-10-31 feat(database): add catalog search with category, price and stock filters
- `b1b3192` 2026-10-31 feat(database): implement CSV ingestion for customers, orders and items
- `b997388` 2026-10-31 feat(database): implement CSV ingestion for categories, products and promotions
- `315c1e8` 2026-10-31 feat(database): define relational SQLite schema for store entities
- `3edb298` 2026-10-31 feat(config): implement centralized configuration and path management
- `3cabcfa` 2026-10-31 chore: organize dataset files and challenge documentation
- `73d54a6` 2026-10-31 chore: add environment variables template .env.example
- `9649cac` 2026-10-31 chore: specify core project dependencies in requirements.txt
- `7e5f0d7` 2026-10-31 chore: setup project repository and define initial .gitignore

---

## Autor

Gabriel Felippe Baptista  
AI Engineer – Full-Stack para Aplicações com IA Generativa  
- E-mail: a65453@alunos.ipb.pt  
- GitHub: [github.com/GabrielF1100](https://github.com/GabrielF1100)  
- Repositório do Projeto: [Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa](https://github.com/GabrielF1100/Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa)
