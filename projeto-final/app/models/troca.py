
from app.models.jogador import Jogador
from app.models.pokemon import Pokemon

class Troca:
    def __init__(self, id, pokemon_oferecido: Pokemon, pokemon_desejado: Pokemon,
                 jogador_origem: Jogador, jogador_destino: Jogador, status=False):
        if not isinstance(jogador_origem, Jogador) or not isinstance(jogador_destino, Jogador):
            raise TypeError("jogador_origem e jogador_destino devem ser instâncias de Jogador")
        if not isinstance(pokemon_oferecido, Pokemon) or not isinstance(pokemon_desejado, Pokemon):
            raise TypeError("pokemon_oferecido e pokemon_desejado devem ser instâncias de Pokemon")

        self.id = id
        self.pokemon_oferecido = pokemon_oferecido
        self.pokemon_desejado = pokemon_desejado
        self.jogador_origem = jogador_origem
        self.jogador_destino = jogador_destino
        self.status = status
