from socket import socket, AF_INET, SOCK_STREAM
from select import select
from typing import List
import sys


def enviar_mensagem_para_todos(conexao, servidor, lista_conexoes: List, mensagem: bytes):
    for socket_c in lista_conexoes:
    #     if socket != servidor and socket != conexao:
        socket_c.send(mensagem)


def criar_nova_conexao_cliente(servidor, conexoes):
    print("Criando nova conexão cliente/servidor")
    novo_cliente, infos_endereco_porta_cliente = servidor.accept()
    conexoes.append(novo_cliente)
    print(
        f"Novo cliente conectado com endereço {infos_endereco_porta_cliente[0]} e porta {infos_endereco_porta_cliente[1]}!"
    )
    # enviar_mensagem_para_todos(novo_cliente, "conectou".encode())


def remover_cliente_off(conexao, lista_conexoes):
    enviar_mensagem_para_todos(conexao, "Cliente está off".encode())
    print("cliente está off")
    conexao.close()
    lista_conexoes.remove(conexao)


def ler_mensagem():
    pass


def criar_servidor(endereco="localhost", porta=8080):
    # Criando um socket TCP/IP
    # AF_INET abrange os endereços do tipo IPv4
    # SOCK_STREAM (socket de fluxo)
    servidor_socket = socket(AF_INET, SOCK_STREAM)

    # Realizando mapeamento entre o socket e a porta
    endereco_servidor = (endereco, porta)

    # Habilitando o reuso de endereço/porta
    # servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print(
        f"Iniciando servidor...\nEscutando no endereço: {endereco_servidor[0]}, porta: {endereco_servidor[1]}"
    )
    servidor_socket.bind(endereco_servidor)

    # Limitando o máximo de conexões simultâneas que podem ser lidas, criando uma fila
    servidor_socket.listen(10)

    return servidor_socket


def inicializa_servidor(servidor):
    lista_conexoes_ativas.append(servidor)

    print("Servidor iniciado!")

    while True:

        conexoes_leitura, conexoes_escrita, erros = select(
            lista_conexoes_ativas, [], []
        )

        for conexao in conexoes_leitura:
            if conexao == servidor_socket:
                criar_nova_conexao_cliente(servidor=servidor_socket, conexoes=lista_conexoes_ativas)

            else:
                try:
                    dados = conexao.recv(tamanho_max_dados)
                except:
                    remover_cliente_off(conexao, lista_conexoes_ativas)
                    continue

                if dados:
                    enviar_mensagem_para_todos(conexao, servidor_socket, lista_conexoes_ativas, dados)
                    print(dados.decode("utf-8"))


if __name__ == "__main__":
    endereco_ip = sys.argv[1]
    porta_servidor = int(sys.argv[2])
    tamanho_max_dados: int = 4096
    lista_conexoes_ativas = []

    servidor_socket = criar_servidor(endereco=endereco_ip, porta=porta_servidor)
    inicializa_servidor(servidor=servidor_socket)
