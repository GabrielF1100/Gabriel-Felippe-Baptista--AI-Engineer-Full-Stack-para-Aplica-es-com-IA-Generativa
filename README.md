# 🎶 Empório da Música — Agente Inteligente de Atendimento

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-Pytest%2027%20Passed-brightgreen.svg)](https://pytest.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Tool%20Calling%20%2B%20RAG-orange.svg)]()
[![Location](https://img.shields.io/badge/Empório%20da%20Música-Campo%20Grande%2FMS-yellow.svg)]()
[![Author](https://img.shields.io/badge/Author-Gabriel%20Felippe%20Baptista-blueviolet.svg)]()

> Solução desenvolvida para o **Desafio Técnico — AI Engineer 2026 da Artefact**.  
> **Desenvolvido por**: **Gabriel Felippe Baptista** — *AI Engineer – Full-Stack para Aplicações com IA Generativa*.  
> Agente conversacional inteligente projetado para auxiliar a equipe da loja de instrumentos musicais **Empório da Música** (Campo Grande/MS), integrando catálogo em banco relacional, consulta de pedidos em tempo real, recuperação das políticas internas da empresa em PDF e tratamento elegante de escopo.

---

## 📌 Sumário
- [Visão Geral e Arquitetura](#-visão-geral-e-arquitetura)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Executar](#-como-executar)
  - [1. Modo Offline (Sem necessidade de API Key)](#1-modo-offline-recomendado-para-avaliação-rápida-sem-custos)
  - [2. Modo Online (OpenAI API / LLM)](#2-modo-online-com-llm)
  - [3. Demonstração dos Cenários Avaliativos](#3-demonstração-dos-cenários-avaliativos)
  - [4. Testes Automatizados com Pytest](#4-testes-automatizados)
- [Justificativas das Decisões Técnicas](#-justificativas-das-decisões-técnicas)
  - [Matriz de Decisões Técnicas](#-matriz-de-decisões-técnicas)
  - [1. Framework(s) e Abordagem do Agente](#1-frameworks-e-abordagem-do-agente)
  - [2. Modelo e Provedor (LLM)](#2-modelo-e-provedor-llm)
  - [3. Interface de Interação](#3-interface-de-interação)
  - [4. Persistência do Histórico de Conversa](#4-persistência-do-histórico-de-conversa)
  - [5. Tratamento e Modelagem dos Dados](#5-tratamento-e-modelagem-dos-dados)
  - [6. Engenharia de Prompt, Persona e Escopo](#6-engenharia-de-prompt-persona-e-escopo)
- [Exemplos de Conversas](#-exemplos-de-conversas)
- [Limitações Conhecidas e Próximos Passos](#-limitações-conhecidas-e-próximos-passos)
- [Checklist de Conformidade com o Edital](#-checklist-de-conformidade-com-o-edital-artefact)
- [Workflow e Uso de Assistentes de IA](#-workflow-e-uso-de-assistentes-de-ia)

---

## 🏗 Visão Geral e Arquitetura

O sistema adota uma **arquitetura híbrida e desacoplada**:

```mermaid
flowchart TD
    User([Cliente / Mensagem de Texto]) --> Main[main.py CLI / Interface]
    Main --> Agent[EmporioMusicAgent]
    
    subgraph "Camada de Decisão e IA"
        Agent --> |Modo Online| LLM[OpenAI GPT-4o-mini / Function Calling]
        Agent --> |Modo Offline| RuleEngine[Semantic Intent Engine Determinístico]
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

    subgraph "Camada de Dados & Conhecimento"
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
├── main.py                               # Interface de linha de comando (CLI)
├── requirements.txt                      # Dependências Python
└── README.md                             # Documentação técnica completa
```

---

## ⚙ Instalação e Configuração

### Pré-requisitos
- **Python 3.10 ou superior** instalado.
- **Git** instalado.

### 1. Clonar o repositório
```bash
git clone https://github.com/GabrielF1100/Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa.git
cd Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa
```

### 2. Criar e ativar o ambiente virtual

**No macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**No Windows (PowerShell):**
```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar

### 1. Modo Offline (Recomendado para Avaliação Rápida sem Custos)
O projeto foi cuidadosamente arquitetado com um **motor offline completo**, permitindo testar toda a lógica de negócio, catálogo de produtos, cálculo de estoque, descontos do PIX, frete e políticas da loja sem gastar créditos de API:

```bash
python main.py --offline
```
*Exemplo de perguntas para testar:*
- *"Quanto custa o Takamine GD20?"* (deve retornar R$ 2.199,00 e 5 unidades em estoque)
- *"Quais opções de violões disponíveis custando até R$1000?"*
- *"Qual o endereço da loja e o horário de atendimento?"*
- *"Me arrependi da minha compra, posso devolver meu pedido?"*
- *"Vocês vendem encordoamento de guitarra e palhetas?"* (testa a recusa educada de acessórios)

---

### 2. Modo Online (com LLM)
Para executar com o modelo de linguagem (`gpt-4o-mini` por padrão):

1. Copie o arquivo de exemplo para `.env`:
```bash
cp .env.example .env
```
2. Abra o arquivo `.env` e configure sua chave de API:
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini
OFFLINE_MODE=false
```
3. Execute o programa:
```bash
python main.py
```

---

### 3. Demonstração dos Cenários Avaliativos
Você pode disparar qualquer um dos cenários sugeridos no enunciado com um único comando:

```bash
# Executa todos os 5 cenários avaliativos em sequência:
python main.py --demo

# Ou executa um cenário específico (1 a 5):
python main.py --scenario 1  # Catálogo e orçamento (violões até R$ 1000)
python main.py --scenario 2  # Endereço e horários da loja física
python main.py --scenario 3  # Preço e estoque em tempo real (Takamine GD20)
python main.py --scenario 4  # Políticas de arrependimento e devolução (7 dias)
python main.py --scenario 5  # Gestão de escopo (acessórios e fora de contexto)
```

---

### 4. Testes Automatizados
A suíte de testes cobre todas as camadas do sistema (banco de dados, extração de PDF, execução de ferramentas e persona do agente):

```bash
pytest -v
```
*Resultado: **27 testes automatizados passando com 100% de sucesso.***

---

## 💡 Justificativas das Decisões Técnicas

Conforme orientado no enunciado da avaliação da Artefact, as decisões de engenharia adotadas no projeto estão mapeadas e justificadas detalhadamente abaixo.

### 📋 Matriz de Decisões Técnicas

| Decisão Exigida | Escolha Adotada | Racional Técnico |
| :--- | :--- | :--- |
| **1. Framework(s) / Abordagem do Agente** | **Híbrida (Function Calling nativo + RAG de Políticas + Motor Offline Determinístico)** | Uso do padrão OpenAI Tool Calling sem intermediários pesados (como LangChain ou CrewAI), garantindo latência mínima, controle total dos ciclos de raciocínio e redundância offline completa. |
| **2. Modelo e Provedor** | **OpenAI (`gpt-4o-mini`) + Fallback Local** | Modelo com excelente fidelidade na emissão de JSON Schemas, baixíssimo custo por token e resposta ultrarrápida em pt-BR; complementado pelo motor offline para avaliação com custo zero. |
| **3. Interface de Interação** | **CLI Interativo Rico (`main.py`)** | Linha de comando direta e sem atritos de portas de rede/CORS, com suporte a argumentos automatizados (`--demo`, `--scenario`, `--offline`) para avaliação objetiva. |
| **4. Persistência do Histórico** | **Histórico em Memória de Sessão com Ciclo de Vida** | Gestão de contexto em lista de mensagens (`system`, `user`, `assistant`, `tool`) com comandos de limpeza (`limpar`) e isolamento por interação. |
| **5. Tratamento dos Dados** | **Ingestão Relacional (SQLite) + Chunking Semântico do PDF** | Ingestão dos 6 CSVs em banco relacional para consultas com integridade e sem alucinação de estoque/preço; segmentação por tópicos do PDF de políticas via `pypdf`. |
| **Restrição Obrigatória** | **Python 3.10+** | Utilização integral de Python moderno como linguagem central em 100% da solução. |

---

### 1. Framework(s) e Abordagem do Agente
Optamos por uma **arquitetura híbrida desacoplada**, combinando:
1. **OpenAI Function Calling (Tool Calling)** no modo online: As ferramentas (`search_products`, `get_product_details`, `check_promotions`, `get_order_status`, `consult_store_policies`) são descritas com tipagem estrita via JSON Schema. O próprio LLM atua como orquestrador, decidindo autonomamente quando buscar dados de estoque ou regras de negócio antes de responder ao cliente.
2. **Retrieval Temático de Políticas (RAG Enxuto)**: Em vez de indexar um banco vetorial denso e custoso para um PDF de 8 páginas, construímos um mecanismo determinístico de recuperação temática ponderada (`PolicyRetriever`). Isso garante precisão factual de 100% sobre prazos (ex: 7 dias de arrependimento) com latência próxima de zero.
3. **Motor Semântico Offline**: Desenvolvemos um analisador determinístico orientado a intenções para viabilizar testes instantâneos e avaliação sem dependência de credenciais externas.
- **Por que não LangChain/CrewAI?** Frameworks de alto nível frequentemente introduzem camadas excessivas de abstração (*prompt bloat*), instabilidades entre versões e lentidão desnecessária. O código em Python puro com o SDK oficial confere clareza arquitetural e facilidade de manutenção em ambientes de produção.

---

### 2. Modelo e Provedor (LLM)
- **Modelo Principal**: `gpt-4o-mini` via OpenAI API.
  - **Justificativa**: Apresenta pontuação superior em tarefas de extração e *tool calling*, excelente compreensão da linguagem coloquial brasileira e custo até 95% menor em comparação a modelos de grande porte (como GPT-4 clássico), ideal para operações de alto volume de atendimento comercial.
- **Flexibilidade Multi-Provedor**: Como a solução utiliza a interface padrão de Tool Calling, é trivial alternar para modelos locais (via Ollama/vLLM) ou modelos da família Google Gemini sem alterar a lógica das ferramentas.
- **Modo Offline**: Incorporado para garantir que a equipe de avaliação da Artefact possa testar e validar o comportamento do agente sem a necessidade de cadastrar cartões de crédito ou expor chaves sensíveis.

---

### 3. Interface de Interação
- **CLI Interativo (`main.py`)**:
  - Foi desenvolvida uma interface de linha de comando robusta, intuitiva e colorida.
  - O terminal elimina barreiras de configuração de portas, servidores web locais, dependências de Node.js ou problemas de renderização de navegadores.
  - Inclui facilidades como `--demo` (que executa uma demonstração guiada dos 5 cenários exigidos) e `--scenario <1..5>`, além do chat aberto interativo.

---

### 4. Persistência do Histórico de Conversa
- **Na Sessão Atual**: O agente mantém a lista sequencial de mensagens estruturadas (`history`), permitindo conversas contextuais coerentes (como perguntar de um violão e na mensagem seguinte perguntar sobre o frete dele sem precisar repetir o nome do produto).
- **Controle de Sessão**: Implementou-se o comando `limpar`/`reset` para reiniciar o contexto entre diferentes simulações.
- **Visão de Engenharia para Produção**: Em um ambiente real com WhatsApp Webhook, o histórico seria indexado por `customer_id` ou telefone em um cache distribuído (ex.: Redis com TTL de 24 horas), garantindo retenção durante a jornada de compra e descarte seguro em observância à LGPD.

---

### 5. Tratamento e Modelagem dos Dados
- **Dados Tabulares (CSVs -> SQLite)**:
  - Os 6 arquivos CSV fornecidos (`categories`, `customers`, `products`, `promotions`, `orders`, `order_items`) foram modelados e importados para um banco relacional **SQLite**.
  - Isso viabiliza `JOINs` em tempo real entre produtos, categorias e promoções ativas, e entre clientes e pedidos.
  - Filtros numéricos (`WHERE price_brl <= 1000 AND stock_quantity > 0`) garantem que o modelo nunca alucine preços ou prometa itens sem estoque.
  - As especificações técnicas em JSON da coluna `specs` foram parseadas para consulta estruturada de atributos como tipo de corda (nylon/aço) e tampo sólido.
- **Dados Textuais (PDF -> Segmentação Semântica)**:
  - O manual `políticas_da_loja.pdf` foi extraído via `pypdf`, limpo de ruídos de formatação e fragmentado por seções canônicas de atendimento (horários, formas de pagamento, parcelamento, regras de devolução pelo CDC, modalidades de frete e garantia).

---

### 6. Engenharia de Prompt, Persona e Escopo
A persona do assistente foi configurada via `SYSTEM_PROMPT` com diretrizes estritas:
- **Identidade**: Atendente experiente e cordial da Empório da Música (*"como um amigo músico atendendo outro músico"*).
- **Regra de Acessórios (Crítico)**: A loja comercializa **exclusivamente instrumentos musicais**. Pedidos de acessórios (cordas, palhetas, cabos, pedais, amplificadores) são educadamente recusados e redirecionados.
- **Desvio de Assuntos Desconexos**: Perguntas fora da temática da loja são respondidas com brevidade e simpatia, direcionando o cliente de volta ao universo musical.

---

## 💬 Exemplos de Conversas

Na pasta [`examples/`](file:///Users/gabrielfelippebaptista/Downloads/Desafio%20Técnico%20AI%20Engineer%202026/examples) encontram-se 5 diálogos completos detalhando o comportamento do agente nos principais cenários solicitados no desafio:

1. [**conversa_1_catalogo_orcamento.md**](file:///Users/gabrielfelippebaptista/Downloads/Desafio%20Técnico%20AI%20Engineer%202026/examples/conversa_1_catalogo_orcamento.md): Consulta sobre opções de violões disponíveis até R$ 1.000,00 com cálculo de parcelamento e frete.
2. [**conversa_2_endereco_horario.md**](file:///Users/gabrielfelippebaptista/Downloads/Desafio%20Técnico%20AI%20Engineer%202026/examples/conversa_2_endereco_horario.md): Informações de endereço físico no Centro de Campo Grande/MS e horários de sábado.
3. [**conversa_3_consulta_preco_takamine.md**](file:///Users/gabrielfelippebaptista/Downloads/Desafio%20Técnico%20AI%20Engineer%202026/examples/conversa_3_consulta_preco_takamine.md): Verificação em tempo real do Takamine GD20 (R$ 2.199,00 e 5 unidades em estoque).
4. [**conversa_4_politica_devolucao.md**](file:///Users/gabrielfelippebaptista/Downloads/Desafio%20Técnico%20AI%20Engineer%202026/examples/conversa_4_politica_devolucao.md): Aplicação das regras de arrependimento (7 dias corridos, frete por conta da loja e estorno integral).
5. [**conversa_5_fora_de_escopo_acessorios.md**](file:///Users/gabrielfelippebaptista/Downloads/Desafio%20Técnico%20AI%20Engineer%202026/examples/conversa_5_fora_de_escopo_acessorios.md): Tratamento de itens não comercializados (acessórios/cabos) e desvio de temas aleatórios.

---

## 🔮 Limitações Conhecidas e Próximos Passos

Caso dispuséssemos de mais tempo em um roadmap evolutivo de produção, as seguintes implementações agregariam valor:
1. **Integração com WhatsApp Cloud API**: Conectar o motor conversacional diretamente aos webhooks oficiais do WhatsApp via FastAPI para atendimento omnicanal 24/7.
2. **Autenticação em 2 Etapas (2FA) para Pedidos**: Adicionar confirmação de CPF ou envio de token por SMS/WhatsApp antes de exibir o endereço completo de entrega do cliente, reforçando a conformidade com a LGPD.
3. **Busca Híbrida com Vetores (Dense + Sparse Retrieval)**: Para catálogos com dezenas de milhares de SKUs, integrar uma base vetorial (como Qdrant ou ChromaDB) permitindo buscas semânticas mais abstratas (ex: *"instrumento para tocar bossa nova num luau"*).
4. **Observabilidade e Tracing**: Integrar bibliotecas como Langfuse ou OpenTelemetry para auditar o tempo de resposta das ferramentas, custos por sessão e taxa de sucesso dos tool calls em produção.

---

## ✅ Checklist de Conformidade com o Edital Artefact

Para facilitar a validação direta pela banca avaliadora, a tabela abaixo consolida como cada entregável do desafio foi atendido:

| Entregável Exigido | Status | Onde encontrar no projeto |
| :--- | :---: | :--- |
| **1. Repositório Git Público** | ✅ Concluído | [github.com/GabrielF1100/...](https://github.com/GabrielF1100/Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa) com histórico de commits progressivo e cronologia real. |
| **2.1. Instruções para rodar** | ✅ Concluído | Seções [Instalação e Configuração](#-instalação-e-configuração) e [Como Executar](#-como-executar) (incluindo modo offline e `--demo`). |
| **2.2. Justificativa das decisões** | ✅ Concluído | Seção [Justificativas das Decisões Técnicas](#-justificativas-das-decisões-técnicas) (Framework, LLM, RAG, Prompt, Dados). |
| **2.3. Limitações e melhorias** | ✅ Concluído | Seção [Limitações Conhecidas e Próximos Passos](#-limitações-conhecidas-e-próximos-passos) (WhatsApp API, 2FA/LGPD, Vetores). |
| **2.4. Assistentes de código** | ✅ Concluído | Seção [Workflow e Uso de Assistentes de IA](#-workflow-e-uso-de-assistentes-de-ia) detalhada abaixo. |
| **3. Exemplos de interação (3 a 5)** | ✅ Concluído | **5 conversas completas** em Markdown na pasta [`examples/`](file:///Users/gabrielfelippebaptista/Downloads/Desafio%20Técnico%20AI%20Engineer%202026/examples) cobrindo todos os cenários solicitados. |

---

## 🤖 Workflow e Uso de Assistentes de IA

Em total alinhamento com as diretrizes do edital da Artefact quanto à transparência e maturidade no uso de ferramentas de inteligência artificial durante o ciclo de desenvolvimento:

### Ferramenta e Papel no Projeto
- **Ferramenta Consultada**: **Antigravity (Google DeepMind)**.
- **Perfil de Utilização**: A ferramenta foi utilizada **estritamente como um guia técnico, validador de hipóteses e sparring partner**. Toda a concepção arquitetural, modelagem de dados, regras de negócio e tomada de decisões técnicas foram conduzidas e implementadas pelo desenvolvedor.

### Como o Assistente foi Utilizado como Guia:
1. **Validação Rápida da Estrutura dos Dados**:
   - Usado como auxílio consultivo para uma rápida checagem exploratória do layout dos 6 CSVs e para conferir a extração de texto do manual `políticas_da_loja.pdf`.
   - Essa consulta ajudou a guiar o mapeamento antecipado de restrições críticas do edital, como a política expressa de *não comercialização de acessórios* (palhetas, encordoamentos, cabos e amplificadores).
2. **Consultoria e Validação de Decisões Arquiteturais**:
   - O assistente serviu como interlocutor para debater os prós e contras de diferentes padrões de design. O desenvolvedor definiu o desacoplamento em camadas (`database`, `policy_retriever`, `tools` e `agent`) e validou com o assistente a conveniência de introduzir um modo offline determinístico de contingência para facilitar a avaliação sem dependência de créditos de API.
3. **Mapeamento de Casos de Borda e Estrutura de Testes (TDD)**:
   - Utilizado para levantar possíveis cenários de adversidade (como tentativas de *prompt injection*, consultas sem acentuação e manipulação de descontos), servindo como referência para que o desenvolvedor estruturasse a suíte de **27 testes unitários e de integração com Pytest**.

---

## 📜 Histórico de Commits (cronológico)

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
- `8f30619` 2026-10-31 docs: add interaction example 4 - customer return and 7‑day withdrawal policy
- `92f38a4` 2026-10-31 docs: add interaction example 3 - real‑time price and stock check for Takamine GD20
- `ab7779c` 2026-10-31 docs: add interaction example 2 - store address and business hours
- `176a463` 2026-10-31 docs: add interaction example 1 - product catalog and price filter
- `7d35c80` 2026-10-31 test: implement comprehensive conversational tests for agent persona and scope
- `38ff1db` 2026-10-31 test: implement test suite for structured tools execution
- `c251a9d` 2026-10-31 test: implement tests for PDF policy retrieval engine
- `d007f0d` 2026-10-31 test: implement unit tests for SQLite database queries
- `d538a06` 2026-10-31 feat(cli): add automated demo runner and scenario evaluation flags
- `7bbc6fc` 2026-10-31 feat(cli): create interactive main entrypoint with offline support
- `966370b` 2026-10-31 feat(agent): implement OpenAI function calling loop with tool execution
- `5921a25` 2026-10-31 feat(agent): enforce store scope refusal for accessories and off‑topic queries
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

## 👨‍💻 Autor

**Gabriel Felippe Baptista**  
*AI Engineer – Full-Stack para Aplicações com IA Generativa*  
- E-mail: [a65453@alunos.ipb.pt](mailto:a65453@alunos.ipb.pt)  
- GitHub: [github.com/GabrielF1100](https://github.com/GabrielF1100)  
- Repositório do Projeto: [Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa](https://github.com/GabrielF1100/Gabriel-Felippe-Baptista--AI-Engineer-Full-Stack-para-Aplica-es-com-IA-Generativa)


