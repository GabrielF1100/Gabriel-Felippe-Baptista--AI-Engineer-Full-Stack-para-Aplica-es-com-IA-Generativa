# Exemplo de Interação 3 — Consulta de Preço e Estoque em Tempo Real

> **Cenário Avaliativo**: "Quanto custa o Takamine GD20?"  
> **Objetivo**: Demonstrar verificação exata de preço, quantidade de estoque e especificações técnicas sem alucinação, integrando informações de pagamento.

---

### Diálogo

**Cliente**:
> Olá, tudo bem? Quanto custa o Takamine GD20? Vocês têm em estoque para envio imediato?

**Agente (Empório da Música)**:
> Tudo ótimo por aqui, e com você? 🎶
>
> O **Takamine GD20 Dreadnought Natural** está custando **R$ 2.199,00**!
>
> Sim, temos **5 unidades em estoque** a pronta entrega aqui na loja.
>
> Este é um instrumento fantástico: conta com tampo sólido em cedro, laterais e fundo em sapele e escala de 650mm, o que proporciona um timbre extremamente aveludado, encorpado e com alta definição, sendo muito elogiado para fingerstyle e dedilhados.
>
> **Condições de pagamento para ele**:
> • **PIX à vista**: R$ 2.089,05 (já com 5% de desconto!);
> • **Cartão de crédito**: Em até 12x de R$ 183,25 sem juros;
> • **Frete**: Como o valor é superior a R$ 500,00, o frete é **GRÁTIS** para toda a Região Metropolitana de Campo Grande via motoboy próprio (1 a 3 dias úteis), ou podemos cotar via SEDEX/Jadlog para outra cidade.
>
> Deseja que eu reserve uma unidade com tampo regulado para você?

---

### Mecanismo Interno
- **Ferramenta Invocada**: `get_product_details(identifier="Takamine GD20")`
- **Origem dos Dados**: Registro `product_id: 95` do arquivo `products.csv`.
- **Fidedignidade**: Preço exato de R$ 2.199,00 e contagem em estoque (5 unidades), combinados com o cálculo das condições de pagamento do manual de políticas.
