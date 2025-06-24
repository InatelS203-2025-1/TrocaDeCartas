
import json
from app.models.troca import Troca

CAMINHO_PROPOSTAS = "propostas_troca.json"

def salvar_proposta_json(proposta: Troca):
    try:
        with open(CAMINHO_PROPOSTAS, "r") as f:
            propostas = json.load(f)
    except FileNotFoundError:
        propostas = []

    propostas.append({
        "id": proposta.id,
        "pokemon_oferecido": proposta.pokemon_oferecido.nome,
        "pokemon_desejado": proposta.pokemon_desejado.nome,
        "jogador_origem": proposta.jogador_origem.id,
        "jogador_destino": proposta.jogador_destino.id,
        "ativa": True,
        "resposta": "pendente"
    })

    with open(CAMINHO_PROPOSTAS, "w") as f:
        json.dump(propostas, f, indent=4)

def atualizar_status_proposta(proposta_id):
    try:
        with open(CAMINHO_PROPOSTAS, "r") as f:
            propostas = json.load(f)
    except FileNotFoundError:
        print("Arquivo de propostas não encontrado.")
        return

    for p in propostas:
        if p["id"] == proposta_id:
            p["ativa"] = False
            p["resposta"] = "aceita"
            break

    with open(CAMINHO_PROPOSTAS, "w") as f:
        json.dump(propostas, f, indent=4)
