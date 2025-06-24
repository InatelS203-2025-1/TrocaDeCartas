import json
from app.models.jogador import Jogador
from app.models.pokemon import Pokemon
from app.models.troca import Troca
from app.notifications.notificacao_jogador import NotificacaoJogador
from app.services.gerenciador_troca import GerenciadorDeTroca
from app.utils_carregamento import carregar_dados_do_json, carregar_propostas_json
from app.gerencia_propostas import salvar_proposta_json, atualizar_status_proposta

CAMINHO_JSON = "jogadores_pokemons_10.json"
jogadores, pokemons_disponiveis = carregar_dados_do_json(CAMINHO_JSON)
gerenciador = GerenciadorDeTroca(NotificacaoJogador())
carregar_propostas_json("propostas_troca.json", jogadores, pokemons_disponiveis, gerenciador)

def menu():
    print("\nMenu:")
    print("1 - Criar nova proposta de troca")
    print("2 - Listar propostas enviadas")
    print("3 - Aceitar uma proposta")
    print("4 - Trocar de jogador")
    print("0 - Sair")

def encontrar_jogador_por_id(jogador_id):
    return jogadores.get(jogador_id)


def listar_pokemons_disponiveis(jogador):
    print(f"Pokémons de {jogador.nome}:")
    for p in pokemons_disponiveis.values():
        if p.status == "disponivel" and p.nivel and hasattr(p, 'dono_id') and p.dono_id == jogador.id:
            print(f"- {p.nome} (Nível {p.nivel})")
            print(f"- {p.nome} (Nível {p.nivel})")

def escolher_pokemon(mensagem):
    print("Pokémons disponíveis:")
    for nome in pokemons_disponiveis:
        print(f"- {nome.capitalize()}")
    nome_escolhido = input(mensagem).strip().lower()
    return pokemons_disponiveis.get(nome_escolhido)

def main():
    print("===== Sistema de Trocas de Pokémon =====")
    try:
        jogador_id = int(input("Digite seu ID de jogador: "))
    except ValueError:
        print("ID inválido.")
        return

    jogador_atual = encontrar_jogador_por_id(jogador_id)
    if not jogador_atual:
        print("Jogador não encontrado no sistema.")
        return

    while True:
        menu()
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            try:
                id_destino = int(input("ID do jogador com quem deseja trocar: "))
            except ValueError:
                print("ID inválido.")
                continue

            if id_destino == jogador_atual.id:
                print("Você não pode trocar com você mesmo.")
                continue

            jogador_destino = encontrar_jogador_por_id(id_destino)
            if not jogador_destino:
                print("Jogador destinatário não encontrado.")
                continue

            listar_pokemons_disponiveis(jogador_atual)
            pkmn_oferecido = escolher_pokemon("Digite o nome do seu Pokémon para oferecer: ")
            if not pkmn_oferecido or pkmn_oferecido.status != "disponivel":
                print("Pokémon inválido ou indisponível.")
                continue

            listar_pokemons_disponiveis(jogador_destino)
            pkmn_desejado = escolher_pokemon("Digite o nome do Pokémon desejado do outro jogador: ")
            if not pkmn_desejado or pkmn_desejado.status != "disponivel":
                print("Pokémon desejado inválido ou indisponível.")
                continue

            proposta = Troca(len(gerenciador.propostas) + 1, pkmn_oferecido, pkmn_desejado, jogador_atual, jogador_destino)
            gerenciador.enviar_proposta(proposta)
            salvar_proposta_json(proposta)

        elif opcao == "2":
            propostas = gerenciador.listar_propostas(jogador_atual)
            if not propostas:
                print("Nenhuma proposta encontrada.")
            else:
                for p in propostas:
                    proposta_json = next(
                        (pj for pj in json.load(open("propostas_troca.json")) if pj["id"] == p.id),
                        None
                    )
                    if proposta_json and not proposta_json.get("ativa", True):
                        continue  # ignora propostas desativadas

                    tipo = "Enviada" if p.jogador_origem.id == jogador_atual.id else "Recebida"
                    status = proposta_json.get("resposta", "pendente").capitalize() if proposta_json else "Pendente"
                    print(f"[{p.id}] {tipo} - {p.pokemon_oferecido.nome} por {p.pokemon_desejado.nome} - Status: {status}")


        
        
        
        elif opcao == "3":
            print("Propostas recebidas:")
            try:
                with open("propostas_troca.json", "r") as f:
                    propostas_json = json.load(f)
            except FileNotFoundError:
                propostas_json = []

            propostas_recebidas = [p for p in propostas_json if p["jogador_destino"] == jogador_atual.id and p.get("ativa", True) and p.get("resposta", "pendente") == "pendente"]
            if not propostas_recebidas:
                print("Nenhuma proposta recebida.")
            else:
                for p in propostas_recebidas:
                    print(f"[{p['id']}] De Jogador {p['jogador_origem']} - {p['pokemon_oferecido']} por {p['pokemon_desejado']}")

                try:
                    id_proposta = int(input("Digite o ID da proposta que deseja responder: "))
                except ValueError:
                    print("ID inválido.")
                    continue

                proposta = next((p for p in gerenciador.propostas if p.id == id_proposta and p.jogador_destino.id == jogador_atual.id), None)
                if proposta:
                    escolha = input("Deseja aceitar (A) ou rejeitar (R) a proposta? ").strip().lower()
                    if escolha == "a":
                        gerenciador.analisar_proposta(proposta)
                        atualizar_status_proposta(proposta.id)
                        print("Proposta aceita.")
                    elif escolha == "r":
                        with open("propostas_troca.json", "r") as f:
                            propostas_json = json.load(f)
                        for p in propostas_json:
                            if p["id"] == proposta.id:
                                p["ativa"] = False
                                p["resposta"] = "rejeitada"
                                break
                        with open("propostas_troca.json", "w") as f:
                            json.dump(propostas_json, f, indent=4)
                        print("Proposta rejeitada.")
                    else:
                        print("Opção inválida.")
                else:
                    print("Proposta não encontrada ou já foi respondida.")
        
        elif opcao == "4":
            try:
                novo_id = int(input("Digite o novo ID de jogador: "))
                novo_jogador = encontrar_jogador_por_id(novo_id)
                if novo_jogador:
                    jogador_atual = novo_jogador
                    print(f"Jogador alterado para: {jogador_atual.nome} (ID {jogador_atual.id})")
                else:
                    print("ID de jogador não encontrado.")
            except ValueError:
                print("ID inválido.")

        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
