# Exemplo de Interação 2 — Informações Gerais da Loja

> **Cenário Avaliativo**: "Qual o endereço da loja?"  
> **Objetivo**: Demonstrar recuperação direta do manual institucional em PDF, informando localização, horário de funcionamento e canais de contato com a persona acolhedora da loja.

---

### Diálogo

**Cliente**:
> Boa tarde! Queria ir aí testar umas guitarras. Qual o endereço da loja e qual o horário de vocês no sábado?

**Agente (Empório da Música)**:
> Boa tarde! Vai ser um prazer imenso te receber aqui para testar nossos instrumentos e tirar aquele som! 🎸
>
> Anote o nosso endereço:
> 📍 **Rua 14 de Maio, 3200 — Centro, Campo Grande - MS** (CEP: 79202-333)
>
> Nossos horários de funcionamento:
> • **Segunda a Sexta-feira**: das 09:00 às 18:00  
> • **Sábado**: das 09:00 às 13:00  
> • **Domingos e Feriados**: Fechado  
>
> Se quiser adiantar alguma dúvida antes de vir ou checar se o modelo exato que você quer testar está plugado no showroom, você também pode nos chamar no WhatsApp no **(67) 3321-4500** ou fixo **(67) 3341-4444**.
>
> Esperamos você! Tem algum modelo ou marca em mente que gostaria que deixássemos separado?

---

### Mecanismo Interno
- **Ferramenta Invocada**: `consult_store_policies(question="endereco da loja e horario sabado")`
- **Origem dos Dados**: Seções 1 (Sobre a Loja) e 2 (Horário de Funcionamento) do documento `políticas_da_loja.pdf`.
- **Persona**: Calorosa, receptiva, enfatizando o convite para experimentar os instrumentos no ambiente físico.
