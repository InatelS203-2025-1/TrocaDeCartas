<h1>
  <img src="https://cdn2.steamgriddb.com/icon_thumb/9a9edc1720f84b8907d3b7f81c1fbb50.png" width="60" style="vertical-align: middle; margin-right: 6px;" />
  Sistema de Trocas - Grupo 8 
</h1>

> Integrantes: Iury Teixeira de Souza, José Carlos Rebouças Neto, Matheus Vieira Honório de Souza

Este é um sistema de backend para trocas de cartas Pokémon entre jogadores, utilizando FastAPI, MQTT (via Mosquitto) e JSON como persistência. O projeto faz parte de um mock de sistema distribuído com troca de mensagens assíncronas.

## 📚 Documentação

**Os princípios de solid que iremos usar:** https://www.canva.com/design/DAGkucCKAas/dfo_d_67zf0J_g0TA3c5uA/view?utm_content=DAGkucCKAas&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h190a1a47ba

**Os padrões arquiteturais que iremos usar:** https://www.canva.com/design/DAGnRcj96-U/3PBe9dbXJCav18SNU1Po4w/view?utm_content=DAGnRcj96-U&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hab32823dda

**Os design patterns que iremos usar:** https://www.canva.com/design/DAGp4y7t9Gg/RWByOQeCcXZvNekAFrJoTA/view?utm_content=DAGp4y7t9Gg&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hd3c8168760



## 📦 Subindo o sistema

```bash
docker compose up --build
```

Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)



## 📡 Endpoints

### ✅ Criar Proposta

`POST /proposta`

```json
{
  "jogador_origem_id": "string",
  "jogador_destino_id": "string",
  "pokemon_oferecido_id": "string",
  "pokemon_desejado_id": "string"
}
```

---

### 📬 Listar Propostas Recebidas

`GET /propostas/{jogador_id}`

---

### 🎯 Aceitar Proposta

`POST /proposta/{id_proposta}/aceitar`

---

### 👤 Obter Jogador

`GET /jogador/{jogador_id}`

---

### 📻 Tópicos MQTT

`GET /topicos_mqtt`

```json
{
  "proposta": "troca/{jogador_destino_id}",
  "aceitacao": "troca/sucesso"
}
```

---

### 📌 Observações

- Dados são persistidos em arquivos `.json` para simular banco.
- O sistema funciona mesmo após restart, restaurando o estado.
