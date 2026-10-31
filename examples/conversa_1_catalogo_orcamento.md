# Exemplo de Interação 1 — Consulta sobre o Catálogo de Produtos

> **Cenário Avaliativo**: "Quais opções de violões disponíveis custando até R$1000?"  
> **Objetivo**: Demonstrar capacidade de consulta estruturada ao banco de dados, filtragem por categoria e faixa de preço, verificação de estoque ativo e apresentação amigável e musical.

---

### Diálogo

**Cliente**:
> Olá! Gostaria de começar a tocar e queria saber quais opções de violões disponíveis vocês têm custando até R$1000?

**Agente (Empório da Música)**:
> Olá! Seja muito bem-vindo à Empório da Música! 🎶 É uma satisfação imensa te ajudar a dar os primeiros passos na música!
>
> Temos excelentes opções de violões em estoque que atendem perfeitamente a esse orçamento de até R$ 1.000,00:
>
> • **Tagima Memphis AC-39 Nylon Natural** — **R$ 429,90** (15 unidades em estoque)  
> *Violão clássico leve e macio com cordas de nylon, muito confortável para quem está iniciando os estudos.*
>
> • **Rozini RC-104 Nylon Estudante** — **R$ 459,90** (10 unidades em estoque)  
> *Tradicional violão de estudo brasileiro, com excelente ressonância e tampo em marfim.*
>
> • **Shelby SN-100 Folk Aço Preto** — **R$ 549,00** (5 unidades em estoque)  
> *Para quem prefere o brilho e pegada das cordas de aço e um visual moderno folk.*
>
> • **Giannini GF-1R Aço Folk Sunburst** — **R$ 579,90** (7 unidades em estoque)  
> *Excelente custo-benefício em cordas de aço com acabamento sunburst clássico.*
>
> • **Yamaha C40 Nylon Natural** — **R$ 599,90** (12 unidades em estoque)  
> *Um dos violões clássicos mais recomendados por professores no mundo todo pelo equilíbrio e durabilidade.*
>
> Além disso, você tem **5% de desconto à vista pagando no PIX** ou pode parcelar em **até 12x sem juros no cartão de crédito**. E se você estiver na região metropolitana de Campo Grande e fechar um pedido acima de R$ 500,00, o frete é grátis via motoboy próprio!
>
> Você tem preferência por cordas de **nylon** (mais macias para dedos) ou cordas de **aço** (som mais encorpado e brilhante)?

---

### Mecanismo Interno
- **Ferramenta Invocada**: `search_products(category="Violões", max_price=1000.0, only_in_stock=True)`
- **Origem dos Dados**: Tabela `products` e `categories` ingeridas a partir dos arquivos CSV originais da loja.
- **Políticas Aplicadas**: Desconto no PIX (5%), parcelamento sem juros no cartão e frete grátis para Campo Grande acima de R$ 500,00.
