
class NotificacaoDecorator:
    def __init__(self, notificacao):
        self._notificacao = notificacao

    def notificar(self, jogador, mensagem):
        print(f"[LOG] Enviando notificação: {mensagem}")
        self._notificacao.notificar(jogador, mensagem)
