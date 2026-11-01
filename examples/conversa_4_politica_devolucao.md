# Exemplo de Interação 4 — Aplicação das Políticas de Devolução e Arrependimento

> **Cenário Avaliativo**: "Me arrependi da minha compra, posso devolver meu pedido?"  
> **Objetivo**: Demonstrar situação não-trivial com aplicação das regras do Código de Defesa do Consumidor e das normas internas da Empório da Música (prazos, custos de frete reverso e reembolsos).

---

### Diálogo

**Cliente**:
> Olá! Recebi ontem o violão que comprei no site de vocês, mas depois de testar achei o braço um pouco largo para a mão do meu filho. Me arrependi da minha compra, posso devolver meu pedido e receber o dinheiro de volta?

**Agente (Empório da Música)**:
> Olá! Compreendemos perfeitamente essa situação. Na música, a pegada e o conforto com o instrumento são essenciais, especialmente para quem está aprendendo!
>
> Sim, você pode devolver com total tranquilidade! Como a sua compra foi realizada online e você recebeu o produto ontem, você está dentro do prazo do **Direito de Arrependimento**, previsto no Código de Defesa do Consumidor e no manual da Empório da Música:
>
> 📋 **Como funciona a nossa política**:
> 1. **Prazo**: Você tem até **7 (sete) dias corridos** a contar do recebimento para solicitar o cancelamento e devolução.
> 2. **Estado do Instrumento**: O violão deve estar em sua embalagem original, sem marcas de desgaste ou avarias, e acompanhado de todos os manuais e eventuais chaves de regulagem.
> 3. **Frete de Devolução**: O frete reverso é **100% por conta da Empório da Música**. Nós geramos a autorização de postagem ou agendamos a coleta sem custo nenhum para você.
> 4. **Reembolso**: O valor integral é restituído na mesma modalidade de pagamento original em até 10 dias úteis após a conferência do produto em nossa loja.
>
> **Alternativa**: Se preferir, também temos a opção de **Troca por Preferência** em até 7 dias, podendo trocar por um modelo de escala reduzida ou braço mais fino ideal para crianças/jovens (como um modelo 3/4 infantil).
>
> Para darmos andamento ao cancelamento ou troca, você poderia me informar o **número do seu pedido** ou o **código de rastreio**?

---

### Mecanismo Interno
- **Ferramenta Invocada**: `consult_store_policies(question="arrependimento prazo devolucao reembolso frete")`
- **Origem dos Dados**: Seção 4 (Política de Trocas e Devoluções) de `políticas_da_loja.pdf`.
- **Destaque de Engenharia de IA**: O agente responde com acolhimento, cita com precisão jurídica e operacional as regras da loja (7 dias corridos, frete por conta da loja, reembolso em até 10 dias úteis) e ainda oferece uma alternativa comercial proativa e atenciosa (troca por modelo infantil).
