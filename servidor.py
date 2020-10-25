import socket
import sys
import json
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from constantes import TAMANHO_MAX_MSG, CODIFICACAO


if len(sys.argv) != 3:
    print("uso correto: python comunicacao/servidor.py <endereço ip> <numero da porta>")
    exit()

ENDERECO_IP: str = sys.argv[1]
PORTA: int = int(sys.argv[2])


class Servidor:
    def __init__(self, endereco_ip: str, porta: int):
        self.endereco: str = endereco_ip
        self.porta: int = porta
        self.lista_conexoes = []
        self.clientes_conectados = {}
        self.socket_servidor = None

    def iniciar_conexao(self):
        print("Iniciando o servidor...")

        self.socket_servidor = socket(AF_INET, SOCK_STREAM)
        self.socket_servidor.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket_servidor.bind((self.endereco, self.porta))
        self.socket_servidor.listen(10)
        self.lista_conexoes = [self.socket_servidor]

        print(f"Ouvindo conexões em {ENDERECO_IP}:{PORTA}...")

    def receber_mensagem_cliente(self, conexao_cliente):
        try:
            mensagem = conexao_cliente.recv(TAMANHO_MAX_MSG)
            if not len(mensagem):
                return None

            print(mensagem)
            return json.loads(mensagem.decode(CODIFICACAO).replace("'", '"'))
        except Exception as error:
            print(f"erro na leitura dos dados do cliente => {error}")
            return None

    def escutar_conexoes(self):
        while True:
            try:
                sockets_leitura, _, sockets_excecoes = select(
                    self.lista_conexoes, [], self.lista_conexoes
                )
            except KeyboardInterrupt:
                sys.exit("\nChat encerrado!")

            for conexao in sockets_leitura:
                if conexao == self.socket_servidor:
                    novo_cliente, infos_conexao = self.socket_servidor.accept()

                    mensagem = self.receber_mensagem_cliente(novo_cliente)
                    if mensagem is None:
                        continue

                    self.lista_conexoes.append(novo_cliente)
                    self.clientes_conectados[novo_cliente] = novo_cliente

                    print(
                        "Nova conexão aceita {}:{}, username: {}".format(
                            *infos_conexao, mensagem.get("remetente")
                        )
                    )

                else:
                    mensagem_recebida = self.receber_mensagem_cliente(conexao)
                    if mensagem_recebida is None:
                        print(
                            "Fechando conexão de {}".format(conexao)
                        )
                        self.remover_conexao(conexao)
                        continue

                    print(
                        'Recebendo mensagem de {}: {}'.format(mensagem_recebida.get("remetente"), mensagem_recebida.get("conteudo"))
                    )

                    for cliente in self.clientes_conectados:
                        if cliente != conexao:
                            cliente.send(json.dumps(mensagem_recebida).encode(CODIFICACAO))

            for conexao in sockets_excecoes:
                self.remover_conexao(conexao)

    def remover_conexao(self, conexao):
        self.lista_conexoes.remove(conexao)
        del self.clientes_conectados[conexao]


servidor = Servidor(ENDERECO_IP, PORTA)
servidor.iniciar_conexao()
servidor.escutar_conexoes()
