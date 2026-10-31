import argparse
import sys
from emporio import config
from emporio.agent import EmporioMusicAgent


DEMO_SCENARIOS = {
    1: {
        "title": "Cenário 1: Consulta de catálogo com filtro de preço",
        "question": "Quais opções de violões disponíveis custando até R$1000?"
    },
    2: {
        "title": "Cenário 2: Informações institucionais e endereço",
        "question": "Qual o endereço da loja e o horário de funcionamento?"
    },
    3: {
        "title": "Cenário 3: Consulta de preço e estoque em tempo real",
        "question": "Quanto custa o Takamine GD20 e tem pronta entrega?"
    },
    4: {
        "title": "Cenário 4: Política de devolução e direito de arrependimento",
        "question": "Me arrependi da minha compra online, posso devolver meu pedido?"
    },
    5: {
        "title": "Cenário 5: Tratamento de escopo (acessórios e fora de contexto)",
        "question": "Vocês vendem encordoamento de guitarra e palhetas? E qual a receita de bolo de cenoura?"
    }
}


def print_banner(offline: bool):
    print("=" * 68)
    print("      🎶  EMPÓRIO DA MÚSICA — AGENTE VIRTUAL DE ATENDIMENTO  🎶")
    print("               Campo Grande/MS • Fundada em 2008")
    print("     Desenvolvido por: Gabriel Felippe Baptista (AI Engineer)")
    print("=" * 68)
    mode_str = "MODO OFFLINE (Sem custos de API / Regras locais)" if offline else f"MODO ONLINE (LLM: {config.OPENAI_MODEL})"
    print(f" Status: {mode_str}")
    print(" Digite 'sair' ou 'exit' para encerrar | 'limpar' para reiniciar histórico")
    print("=" * 68 + "\n")


def run_demo(scenario_num: int = None, offline: bool = True):
    agent = EmporioMusicAgent(offline_mode=offline)
    scenarios = [DEMO_SCENARIOS[scenario_num]] if scenario_num in DEMO_SCENARIOS else DEMO_SCENARIOS.values()

    print("\n--- INICIANDO DEMONSTRAÇÃO AUTOMATIZADA DOS CENÁRIOS ---\n")
    for s in scenarios:
        print(f"\n▶ [{s['title']}]")
        print(f"👤 Cliente: {s['question']}")
        reply = agent.chat(s["question"])
        print(f"🤖 Agente:\n{reply}\n")
        print("-" * 68)


def main():
    parser = argparse.ArgumentParser(description="Agente de Atendimento da Empório da Música")
    parser.add_argument("--offline", action="store_true", help="Executa o agente em modo offline sem necessidade de chave de API.")
    parser.add_argument("--scenario", type=int, choices=[1, 2, 3, 4, 5], help="Executa um dos 5 cenários avaliativos.")
    parser.add_argument("--demo", action="store_true", help="Executa todos os cenários de demonstração em sequência.")

    args = parser.parse_args()

    offline_mode = args.offline or (not config.OPENAI_API_KEY)

    # demo flags
    if False:
        run_demo(offline=offline_mode)
        return

    if args.scenario:
        run_demo(scenario_num=args.scenario, offline=offline_mode)
        return

    print_banner(offline_mode)
    agent = EmporioMusicAgent(offline_mode=offline_mode)

    print("🤖 Agente: Olá! Sou o assistente da Empório da Música. Como posso ajudar você hoje?")
    while True:
        try:
            user_msg = input("\n👤 Você: ").strip()
            if not user_msg:
                continue

            if user_msg.lower() in ("sair", "exit", "quit", "q"):
                print("\n🤖 Agente: Muito obrigado pelo contato com a Empório da Música! Boas notas e até logo! 🎸\n")
                break

            if user_msg.lower() in ("limpar", "clear", "reset"):
                agent.reset_history()
                print("\n[Histórico reiniciado com sucesso!]")
                continue

            reply = agent.chat(user_msg)
            print(f"\n🤖 Agente:\n{reply}")

        except (KeyboardInterrupt, EOFError):
            print("\n\nAtendimento finalizado. Até a próxima!")
            break


if __name__ == "__main__":
    main()
