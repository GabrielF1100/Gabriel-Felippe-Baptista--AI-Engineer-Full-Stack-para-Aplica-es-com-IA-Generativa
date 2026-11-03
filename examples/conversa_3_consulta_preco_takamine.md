# Exemplo de Interação 3 — Consulta de Preço e Estoque em Tempo Real

> **Cenário Avaliativo**: "Quanto custa o Takamine GD20?"  
> **Objetivo**: Demonstrar verificação exata de preço, quantidade de estoque e especificações técnicas sem alucinação, integrando informações de pagamento.

---

### Diálogo

**Cliente**:
> Olá, tudo bem? Quanto custa o Takamine GD20? Tem desconto pagando à vista no PIX e até quantas vezes vocês parcelam no cartão sem juros?

**Agente (Empório da Música)**:
> Tudo ótimo por aqui, e com você? 🎶
>
> O **Takamine GD20 Dreadnought Natural** está custando **R$ 2.199,00**!
>
> Sim, temos atualmente **5 unidades em estoque** a pronta entrega aqui na loja.
>
> Este é um instrumento fantástico: conta com tampo sólido em cedro, laterais e fundo em sapele e escala de 650mm, o que proporciona um timbre extremamente aveludado, encorpado e com alta definição, sendo muito elogiado para fingerstyle e dedilhados.
>
> **Condições de pagamento e descontos para ele**:
> • **À vista no PIX com 5% de desconto**: sai por **R$ 2.089,05** (uma economia direta de R$ 109,95!);
> • **Cartão de crédito**: parcelamos em **até 12x sem juros de R$ 183,25**;
> • **Frete**: Como o valor é superior a R$ 500,00, o frete é **100% GRÁTIS** para toda a Região Metropolitana de Campo Grande via motoboy próprio (entrega rápida em 1 a 3 dias úteis), ou podemos despachar com seguro via transportadora/Correios para todo o Brasil.
>
> Deseja que eu reserve uma unidade com tampo regulado para você?

---

### Mecanismo Interno
- **Ferramenta Invocada**: `get_product_details(identifier="Takamine GD20")`
- **Origem dos Dados**: Registro `product_id: 95` do arquivo `products.csv`.
- **Fidedignidade**: Preço exato de R$ 2.199,00 e contagem em estoque (5 unidades), combinados com o cálculo das condições de pagamento do manual de políticas.
