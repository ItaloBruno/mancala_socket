import socket
import sys
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from const import TAMANHO_MAX_MSG

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
                return False
            tamanho = int(mensagem.decode("utf-8").strip())

            return {"header": mensagem, "data": conexao_cliente.recv(tamanho)}
        except Exception as error:
            print(f"erro na leitura dos dados do cliente => {error}")
            return False

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

                    user = self.receber_mensagem_cliente(novo_cliente)
                    if user is False:
                        continue

                    self.lista_conexoes.append(novo_cliente)
                    self.clientes_conectados[novo_cliente] = user

                    print(
                        "Nova conexão aceita {}:{}, username: {}".format(
                            *infos_conexao, user["data"].decode("utf-8")
                        )
                    )

                else:
                    mensagem = self.receber_mensagem_cliente(conexao)
                    if mensagem is False:
                        print(
                            "Fechando conexão de {}".format(
                                self.clientes_conectados[conexao]["data"].decode("utf-8")
                            )
                        )
                        self.remover_conexao(conexao)
                        continue

                    user = self.clientes_conectados[conexao]

                    print(
                        f'Recebendo mensagem de {user["data"].decode("utf-8")}: {mensagem["data"].decode("utf-8")}'
                    )

                    for cliente in self.clientes_conectados:
                        if cliente != conexao:
                            cliente.send(
                                user["header"]
                                + user["data"]
                                + mensagem["header"]
                                + mensagem["data"]
                            )

            for conexao in sockets_excecoes:
                self.remover_conexao(conexao)

    def remover_conexao(self, conexao):
        self.lista_conexoes.remove(conexao)
        del self.clientes_conectados[conexao]

    def fechar_conexao_servidor(self):
        pass


servidor = Servidor(ENDERECO_IP, PORTA)
servidor.iniciar_conexao()
servidor.escutar_conexoes()
