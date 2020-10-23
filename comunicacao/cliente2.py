import socket
import errno
import sys
from threading import Thread
from pprint import pprint
sys.path.append('/home/gandalf/Área de Trabalho/faculdade/ppd/mancala_socket/mensagem')
sys.path.append('/home/gandalf/Área de Trabalho/faculdade/ppd/mancala_socket/comunicacao')
# pprint(sys.path)

from comunicacao.const import TAMANHO_MAX_MSG
from mensagem.mensagem import Mensagem


if len(sys.argv) != 3:
    print("uso correto: python comunicacao/cliente.py <endereço ip> <numero da porta>")
    exit()

ENDERECO_IP: str = sys.argv[1]
PORTA: int = int(sys.argv[2])


class Cliente:
    def __init__(self, nome: str, porta: int, endereco_ip: str):
        self.nome = nome
        self.porta = porta
        self.endereco_ip = endereco_ip
        self.conexao = None

    def iniciar_conexao_com_servidor(self):
        self.conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexao.connect((self.endereco_ip, self.porta))
        self.conexao.setblocking(False)

        mensagem_inicial = Mensagem(tipo="chat", conteudo=self.nome, remetente=self.nome)
        mensagem_em_bytes = mensagem_inicial.converter_msg_em_bytes_para_enviar()
        self.conexao.send(mensagem_em_bytes)

    def enviar_mensagem_para_o_servidor(self):
        while True:
            try:
                mensagem_para_enviar = input(f"{self.nome} > ")
            except KeyboardInterrupt:
                self.conexao.close()
                sys.exit("\nChat encerrado!")

            if mensagem_para_enviar:
                mensagem = Mensagem(tipo="chat", conteudo=mensagem_para_enviar, remetente=self.nome)
                mensagem_em_bytes = mensagem.converter_msg_em_bytes_para_enviar()
                self.conexao.send(mensagem_em_bytes)

    def receber_mensagens_do_servidor(self):
        while True:
            try:
                mensagem_recebida_do_servidor = self.conexao.recv(TAMANHO_MAX_MSG)

                if not len(mensagem_recebida_do_servidor):
                    print("Connection closed by the server")
                    sys.exit()

                mensagem = Mensagem(tipo="chat", conteudo="", remetente=self.nome)
                mensagem.converter_bytes_para_json_e_setar_valores_da_classe(json_em_bytes=mensagem_recebida_do_servidor)

                print(f"\n{mensagem.remetente} > {mensagem.conteudo}\n{self.nome} > ", end="")

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error: {}".format(str(e)))
                    sys.exit()

                continue

            except Exception as e:
                print("Reading error: ".format(str(e)))
                sys.exit()


meu_nome_usuario = input("Digite seu nome de usuário: ")
cliente = Cliente(nome=meu_nome_usuario, porta=PORTA, endereco_ip=ENDERECO_IP)
cliente.iniciar_conexao_com_servidor()

thread_recebimento_de_mensagens = Thread(target=cliente.receber_mensagens_do_servidor)
thread_recebimento_de_mensagens.start()
thread_envio_de_mensagens_ao_servidor = Thread(target=cliente.enviar_mensagem_para_o_servidor)
thread_envio_de_mensagens_ao_servidor.start()
