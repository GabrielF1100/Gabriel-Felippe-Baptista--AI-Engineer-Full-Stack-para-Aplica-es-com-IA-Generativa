# Exemplo de Interação 1 — Consulta sobre o Catálogo de Produtos

> **Cenário Avaliativo**: "Quais opções de violões disponíveis custando até R$1000?"  
> **Objetivo**: Demonstrar capacidade de consulta estruturada ao banco de dados, filtragem por categoria e faixa de preço, verificação de estoque ativo e apresentação amigável e musical.

---

### Diálogo

**Cliente**:
> Olá! Gostaria de começar a tocar e queria saber quais opções de violões disponíveis vocês têm custando até R$1000? Vocês oferecem desconto no PIX ou parcelamento no cartão sem juros?

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
> **Condições de Pagamento e Descontos**:
> • **À vista no PIX**: você ganha **5% de desconto** imediato em qualquer um deles! (Por exemplo, o Yamaha C40 sai de R$ 599,90 por **R$ 569,90**).
> • **Cartão de Crédito**: parcelamos em **até 12x sem juros** (o Tagima Memphis, por exemplo, fica em 12x de apenas **R$ 35,82**).
> • **Frete**: nas compras a partir de R$ 500,00, a entrega é **grátis** na região de Campo Grande via motoboy próprio!
>
> Você tem preferência por cordas de **nylon** (mais macias para dedos) ou cordas de **aço** (som mais encorpado e brilhante)?

**Cliente**:
> Gostei muito do Yamaha C40! Como ficaria o parcelamento dele em 6x e em 12x no cartão de crédito?

**Agente (Empório da Música)**:
> Excelente escolha! O Yamaha C40 é uma referência mundial para estudantes e músicos amadores exigentes.
>
> As condições de parcelamento para o **Yamaha C40 (R$ 599,90)** no cartão de crédito são:
> • **Em 6x sem juros**: parcelas de **R$ 99,98**
> • **Em 12x sem juros**: parcelas de **R$ 49,99**
>
> Lembrando que se optar pelo **PIX à vista**, com os nossos 5% de desconto ele fica por **R$ 569,90** (economia de R$ 30,00). E como o valor supera R$ 500,00, o frete via motoboy aqui em Campo Grande é **100% gratuito**!
>
> Posso preparar a reserva de uma unidade para você?

---

### Mecanismo Interno
- **Ferramenta Invocada**: `search_products(category="Violões", max_price=1000.0, only_in_stock=True)`
- **Origem dos Dados**: Tabela `products` e `categories` ingeridas a partir dos arquivos CSV originais da loja.
- **Políticas Aplicadas**: Desconto no PIX (5%), parcelamento sem juros no cartão e frete grátis para Campo Grande acima de R$ 500,00.
