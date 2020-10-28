import socket
import errno
import sys
from threading import Thread
from constantes import TAMANHO_MAX_MSG
from mensagem import Mensagem, TipoPermitidosDeMensagem
from interface_grafica import TelaDoJogo
import pygame
from typing import Optional


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
        self.sou_primeiro_jogador = False

    def iniciar_conexao_com_servidor(self):
        self.conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conexao.connect((self.endereco_ip, self.porta))
        self.conexao.setblocking(False)

        mensagem_inicial = Mensagem(
            tipo="chat", conteudo=self.nome, remetente=self.nome
        )
        mensagem_em_bytes = mensagem_inicial.converter_msg_em_bytes_para_enviar()
        self.conexao.send(mensagem_em_bytes)

    def enviar_mensagem_para_o_servidor(self, mensagem: Optional[Mensagem] = None):
        while True:
            mensagem_para_enviar = ""
            if not mensagem:
                try:
                    mensagem_para_enviar = input(f"{self.nome} > ")
                except KeyboardInterrupt:
                    self.encerrar_conexao_servidor()
            else:
                mensagem_em_bytes = mensagem.converter_msg_em_bytes_para_enviar()
                self.conexao.send(mensagem_em_bytes)

            if mensagem_para_enviar:
                if mensagem_para_enviar in ["sair do jogo", "desconectar"]:
                    mensagem_desistencia = Mensagem(
                        tipo="desistencia",
                        conteudo="Você ganhou a partida",
                        remetente=self.nome,
                    )
                    mensagem_em_bytes = (
                        mensagem_desistencia.converter_msg_em_bytes_para_enviar()
                    )
                    self.conexao.send(mensagem_em_bytes)
                    self.encerrar_conexao_servidor()
                    break
                else:
                    mensagem = Mensagem(
                        tipo="chat", conteudo=mensagem_para_enviar, remetente=self.nome
                    )
                    mensagem_em_bytes = mensagem.converter_msg_em_bytes_para_enviar()
                    self.conexao.send(mensagem_em_bytes)

    def receber_mensagens_do_servidor(self):
        while True:
            try:
                mensagem_recebida_do_servidor = self.conexao.recv(TAMANHO_MAX_MSG)

                if not len(mensagem_recebida_do_servidor):
                    print("Conexão fechada pelo servidor!")
                    self.encerrar_conexao_servidor()

                mensagem = Mensagem(tipo="chat", conteudo="", remetente=self.nome)
                mensagem.converter_bytes_para_json_e_setar_valores_da_classe(
                    json_em_bytes=mensagem_recebida_do_servidor
                )

                if mensagem.tipo == TipoPermitidosDeMensagem.desistencia.value:
                    print("Eu venci a partida, ieeeeeeei")
                    self.encerrar_conexao_servidor()
                elif (
                    mensagem.tipo == TipoPermitidosDeMensagem.conexao_estabelecida.value
                ):
                    if mensagem.conteudo:
                        print("sou o primeiro jogador")
                        self.sou_primeiro_jogador = True
                    else:
                        print("sou o segundo jogador")
                elif mensagem.tipo == TipoPermitidosDeMensagem.movimentacao.value:
                    # TODO pensar em alguma maneira para que os estados de todos as casas/kallah
                    #  sejam repassadas de um cliente para outro e seja feita a atualização do tabuleiro
                    print("recebi uma movimentação")
                    print(mensagem.conteudo)
                    pass
                else:
                    print(
                        f"\n{mensagem.remetente} > {mensagem.conteudo}\n{self.nome} > ",
                        end="",
                    )

            except IOError as e:
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print("Reading error: {}".format(str(e)))
                    sys.exit()

                continue

            except Exception as e:
                print("Reading error: ".format(str(e)))
                sys.exit()

    def encerrar_conexao_servidor(self):
        self.conexao.close()
        sys.exit("\nChat encerrado!")


if __name__ == "__main__":
    meu_nome_usuario = input("Digite seu nome de usuário: ")
    print("INFO: Para desistir da partida, digite 'sair do jogo' ou 'desconectar'")
    cliente = Cliente(nome=meu_nome_usuario, porta=PORTA, endereco_ip=ENDERECO_IP)
    cliente.iniciar_conexao_com_servidor()

    thread_recebimento_de_mensagens = Thread(
        target=cliente.receber_mensagens_do_servidor
    )
    thread_recebimento_de_mensagens.start()
    thread_envio_de_mensagens_ao_servidor = Thread(
        target=cliente.enviar_mensagem_para_o_servidor
    )
    thread_envio_de_mensagens_ao_servidor.start()

    tela_do_jogador = TelaDoJogo(meu_nome_usuario, cliente.sou_primeiro_jogador)
    tela_do_jogador.iniciar_tela_do_jogador()
    tela_do_jogador.desenhar_tabuleiro()

    mostrar_tela_jogo = True
    while mostrar_tela_jogo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mostrar_tela_jogo = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                resultado = tela_do_jogador.clicou_em_alguma_das_minhas_casa(
                    pygame.mouse.get_pos()
                )
                if resultado:
                    # TODO se a casa for clicada, enviar essas informações em alguma estrutura de dados para
                    #  que o outro cliente receba essas mesmas informações e possa atualizar a sua tela
                    #  uma ideia seria repassar uma lista com os valores de cada casa/kallah, já que eu tenho uma ordem
                    #  pré estabelecida das peças do tabuleiro
                    novos_valores_pecas_tabuleiro = (
                        tela_do_jogador.pegar_os_valores_das_casas_e_kallah()
                    )
                    print(
                        f"resultado: {resultado}, coordenadas: {pygame.mouse.get_pos()}"
                    )
                    print(f"valores das casas: {novos_valores_pecas_tabuleiro}")

                    # mensagem_movimentacao = Mensagem(
                    #     tipo=TipoPermitidosDeMensagem.movimentacao.value,
                    #     conteudo=novos_valores_pecas_tabuleiro,
                    #     remetente=meu_nome_usuario,
                    # )

                    tela_do_jogador.desenhar_elementos_na_tela()
                    tela_do_jogador.mostrar_tela_do_jogador()

                    resultado = False
                    continue
        try:
            tela_do_jogador.desenhar_elementos_na_tela()
            tela_do_jogador.mostrar_tela_do_jogador()
        except KeyboardInterrupt:
            cliente.encerrar_conexao_servidor()
            break
