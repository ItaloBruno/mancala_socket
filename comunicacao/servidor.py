import socket
# import select
import sys
from select import select
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

if len(sys.argv) != 3:
    print("uso correto: python comunicacao/servidor.py <endereço ip> <numero da porta>")
    exit()

ENDERECO_IP: str = sys.argv[1]
PORTA: int = int(sys.argv[2])
TAMANHO_MAX_MSG: int = 2048


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
        except:
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
                        self.lista_conexoes.remove(conexao)
                        del self.clientes_conectados[conexao]
                        continue

                    user = self.clientes_conectados[conexao]

                    print(
                        f'Recebendo mensagem de {user["data"].decode("utf-8")}: {mensagem["data"].decode("utf-8")}'
                    )

                    for novo_cliente in self.clientes_conectados:
                        if novo_cliente != conexao:
                            novo_cliente.send(
                                user["header"]
                                + user["data"]
                                + mensagem["header"]
                                + mensagem["data"]
                            )

            for conexao in sockets_excecoes:
                self.lista_conexoes.remove(conexao)
                del self.clientes_conectados[conexao]

    def remover_conexao(self):
        pass

    def fechar_conexao_servidor(self):
        pass


servidor = Servidor(ENDERECO_IP, PORTA)
servidor.iniciar_conexao()
servidor.escutar_conexoes()

# # Criando o socket do servidor
# # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# # SO_ - socket option
# # SOL_ - socket option level
# # Sets REUSEADDR (as a socket option) to 1 on socket
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#
# # Bind, so server informs operating system that it's going to use given IP and port
# # For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
# server_socket.bind((ENDERECO_IP, PORTA))
#
# # This makes server listen to new connections
# server_socket.listen()
#
# # List of sockets for select.select()
# sockets_list = [server_socket]
#
# # List of connected clients - socket as a key, user header and name as data
# clients = {}
#
# print(f"Listening for connections on {ENDERECO_IP}:{PORTA}...")
#
# # Handles message receiving
# def receive_message(client_socket):
#
#     try:
#
#         # Receive our "header" containing message length, it's size is defined and constant
#         message_header = client_socket.recv(TAMANHO_MAX_MSG)
#
#         # If we received no data, client gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
#         if not len(message_header):
#             return False
#
#         # Convert header to int value
#         message_length = int(message_header.decode("utf-8").strip())
#
#         # Return an object of message header and message data
#         result = {"header": message_header, "data": client_socket.recv(message_length)}
#         print(result)
#         return result
#     except:
#
#         # If we are here, client closed connection violently, for example by pressing ctrl+c on his script
#         # or just lost his connection
#         # socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information about closing the socket (shutdown read/write)
#         # and that's also a cause when we receive an empty message
#         return False
#
#
# while True:
#
#     # Calls Unix select() system call or Windows select() WinSock call with three parameters:
#     #   - rlist - sockets to be monitored for incoming data
#     #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
#     #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
#     # Returns lists:
#     #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
#     #   - writing - sockets ready for data to be send thru them
#     #   - errors  - sockets with some exceptions
#     # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
#     try:
#         read_sockets, _, exception_sockets = select.select(
#             sockets_list, [], sockets_list
#         )
#     except KeyboardInterrupt:
#         sys.exit("\nChat encerrado!")
#
#     # Iterate over notified sockets
#     for notified_socket in read_sockets:
#
#         # If notified socket is a server socket - new connection, accept it
#         if notified_socket == server_socket:
#
#             # Accept new connection
#             # That gives us new socket - client socket, connected to this given client only, it's unique for that client
#             # The other returned object is ip/port set
#             client_socket, client_address = server_socket.accept()
#
#             # Client should send his name right away, receive it
#             user = receive_message(client_socket)
#
#             # If False - client disconnected before he sent his name
#             if user is False:
#                 continue
#
#             # Add accepted socket to select.select() list
#             sockets_list.append(client_socket)
#
#             # Also save username and username header
#             clients[client_socket] = user
#
#             print(
#                 "Accepted new connection from {}:{}, username: {}".format(
#                     *client_address, user["data"].decode("utf-8")
#                 )
#             )
#
#         # Else existing socket is sending a message
#         else:
#
#             # Receive message
#             message = receive_message(notified_socket)
#
#             # If False, client disconnected, cleanup
#             if message is False:
#                 print(
#                     "Closed connection from: {}".format(
#                         clients[notified_socket]["data"].decode("utf-8")
#                     )
#                 )
#
#                 # Remove from list for socket.socket()
#                 sockets_list.remove(notified_socket)
#
#                 # Remove from our list of users
#                 del clients[notified_socket]
#
#                 continue
#
#             # Get user by notified socket, so we will know who sent the message
#             user = clients[notified_socket]
#
#             print(
#                 f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}'
#             )
#
#             # Iterate over connected clients and broadcast message
#             for client_socket in clients:
#
#                 # But don't sent it to sender
#                 if client_socket != notified_socket:
#
#                     # Send user and message (both with their headers)
#                     # We are reusing here message header sent by sender, and saved username header send by user when he connected
#                     client_socket.send(
#                         user["header"]
#                         + user["data"]
#                         + message["header"]
#                         + message["data"]
#                     )
#
#     # It's not really necessary to have this, but will handle some socket exceptions just in case
#     for notified_socket in exception_sockets:
#
#         # Remove from list for socket.socket()
#         sockets_list.remove(notified_socket)
#
#         # Remove from our list of users
#         del clients[notified_socket]
