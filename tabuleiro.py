"""
    link usado como base: https://humberto.io/pt-br/blog/desbravando-o-pygame-1-conhecendo-a-biblioteca/
"""

import pygame
from typing import Tuple, List
from constantes import (
    LARGURA_TELA,
    COMPRIMENTO_TELA,
    COR_PLANO_DE_FUNDO,
    COR_MINHAS_CASAS,
    COR_CASAS_ADVERSARIO,
    TAMANHO_LADO_CASA,
    COMPRIMENTO_KALLAH,
    VERMELHO,
)


class ElementoTela:
    def __init__(self, coordenada_x: int, coordenada_y: int, cor: Tuple[int]):
        self.coordenada_x = coordenada_x
        self.coordenada_y = coordenada_y
        self.cor = cor

    def desenhar_elemento(self, tela):
        pass


class Texto(ElementoTela):
    def __init__(
        self, coordenada_x: int, coordenada_y: int, cor: Tuple[int], valor_texto: str
    ):
        self.fonte = pygame.font.SysFont(None, 55)
        self.valor_texto = valor_texto
        super().__init__(coordenada_x, coordenada_y, cor)

    def atualizar_valor_texto(self, novo_texto: str) -> None:
        self.valor_texto = novo_texto

    def desenhar_elemento(self, tela) -> None:
        texto = self.fonte.render(self.valor_texto, True, VERMELHO)
        tela.blit(texto, [self.coordenada_x, self.coordenada_y])


class Poligono(ElementoTela):
    def __init__(
        self,
        coordenada_x: int,
        coordenada_y: int,
        cor: Tuple[int],
        largura: int,
        comprimento: int,
        numero_de_pecas_inicial: int,
        nome_jogador: str = "",
    ):
        self.largura = largura
        self.comprimento = comprimento
        self.numero_de_pecas = numero_de_pecas_inicial
        self.fonte_texto = Texto(
            int(coordenada_x + (largura / 2.5)),
            int(coordenada_y + (comprimento / 3)),
            VERMELHO,
            str(self.numero_de_pecas),
        )
        self.nome_jogador = nome_jogador
        super().__init__(coordenada_x, coordenada_y, cor)

    def desenhar_quantidade_pecas(self, tela):
        self.fonte_texto.atualizar_valor_texto(str(self.numero_de_pecas))
        self.fonte_texto.desenhar_elemento(tela)

    def desenhar_elemento(self, tela):
        pygame.draw.rect(
            tela,
            self.cor,
            [self.coordenada_x, self.coordenada_y, self.largura, self.comprimento],
        )
        self.desenhar_quantidade_pecas(tela)


class Casa(Poligono):
    def __init__(
        self,
        coordenada_x: int,
        coordenada_y: int,
        cor: Tuple[int],
        largura: int,
        comprimento: int,
        nome_jogador: str,
    ):
        self.elemento_react = None
        super().__init__(
            coordenada_x, coordenada_y, cor, largura, comprimento, 4, nome_jogador
        )

    def fui_clicado(self, coordenas_do_clique: Tuple[int], tela, nome_jogador):
        clicado = False
        x = coordenas_do_clique[0]
        y = coordenas_do_clique[1]
        if (
            self.nome_jogador == nome_jogador
            and (self.coordenada_x <= x <= self.coordenada_x + self.largura)
            and (self.coordenada_y <= y <= self.coordenada_y + self.comprimento)
        ):
            clicado = True

        return clicado


class Kallah(Poligono):
    def __init__(
        self,
        coordenada_x: int,
        coordenada_y: int,
        cor: Tuple[int],
        largura: int,
        comprimento: int,
        nome_jogador: str = "",
    ):
        super().__init__(
            coordenada_x, coordenada_y, cor, largura, comprimento, 0, nome_jogador
        )


class TelaDoJogo:
    def __init__(self, nome_jogador: str, cliente_eh_primeiro_jogador: bool):
        self.nome_mostrado_no_display = f"Mancala - {nome_jogador}"
        self.nome_jogador = nome_jogador
        self.sou_primeiro_jogador = cliente_eh_primeiro_jogador
        self.elementos_da_tela = []
        self.tela = None
        self.indice_minha_kallah = 6
        self.indice_kallah_adversario = 13

    def iniciar_tela_do_jogador(self):
        pygame.init()
        self.tela = pygame.display.set_mode([LARGURA_TELA, COMPRIMENTO_TELA])
        pygame.display.set_caption(self.nome_mostrado_no_display)
        self.tela.fill(COR_PLANO_DE_FUNDO)

    def desenhar_elementos_na_tela(self):
        for elemento in self.elementos_da_tela:
            elemento.desenhar_elemento(self.tela)

    def adicionar_elemento_na_tela(self, elemento):
        self.elementos_da_tela.append(elemento)

    def desenhar_casas_do_tabuleiro_adversario(
        self, coordenada_x_inicial, coordenada_y_inicial, cor, nome_jogador
    ):
        while coordenada_x_inicial >= 150:
            casa = Casa(
                coordenada_x_inicial,
                coordenada_y_inicial,
                cor,
                TAMANHO_LADO_CASA,
                TAMANHO_LADO_CASA,
                nome_jogador,
            )
            self.adicionar_elemento_na_tela(casa)
            coordenada_x_inicial -= 100

    def desenhar_minhas_casas_do_tabuleiro(
        self, coordenada_x_inicial, coordenada_y_inicial, cor, nome_jogador: str
    ):
        while coordenada_x_inicial < 750:
            casa = Casa(
                coordenada_x_inicial,
                coordenada_y_inicial,
                cor,
                TAMANHO_LADO_CASA,
                TAMANHO_LADO_CASA,
                nome_jogador,
            )
            self.adicionar_elemento_na_tela(casa)
            coordenada_x_inicial += 100

    def desenhar_kallah(self, x, y, cor, largura, comprimento, nome_jogador):
        kallah = Kallah(x, y, cor, largura, comprimento, nome_jogador)
        self.adicionar_elemento_na_tela(kallah)

    def desenhar_tabuleiro(self):
        # Fiz nessa ordem para que eu tenha todos os elementos na ordem anti-horária
        # desenhando minhas casas
        casa_ou_kallah_jogador_1 = self.nome_jogador
        casa_ou_kallah_jogador_2 = ""
        if not self.sou_primeiro_jogador:
            casa_ou_kallah_jogador_1 = ""
            self.indice_kallah_adversario = 6

            casa_ou_kallah_jogador_2 = self.nome_jogador
            self.indice_minha_kallah = 13

        self.desenhar_minhas_casas_do_tabuleiro(
            coordenada_x_inicial=150,
            coordenada_y_inicial=200,
            cor=COR_MINHAS_CASAS,
            nome_jogador=casa_ou_kallah_jogador_1,
        )
        # desenhando minha kallah
        self.desenhar_kallah(
            750,
            100,
            COR_MINHAS_CASAS,
            TAMANHO_LADO_CASA,
            COMPRIMENTO_KALLAH,
            casa_ou_kallah_jogador_1,
        )
        # desenhando casas do adversário
        self.desenhar_casas_do_tabuleiro_adversario(
            coordenada_x_inicial=650,
            coordenada_y_inicial=100,
            cor=COR_CASAS_ADVERSARIO,
            nome_jogador=casa_ou_kallah_jogador_2,
        )
        # desenhando kallah do oponente
        self.desenhar_kallah(
            50,
            100,
            COR_CASAS_ADVERSARIO,
            TAMANHO_LADO_CASA,
            COMPRIMENTO_KALLAH,
            casa_ou_kallah_jogador_2,
        )
        self.desenhar_elementos_na_tela()

    def pegar_as_pecas_da_casa_adversaria_e_zerar_seu_valor(
        self, indice_da_minha_casa: int
    ) -> int:
        minha_casa = self.elementos_da_tela[indice_da_minha_casa]
        coordenada_y = 100 if self.sou_primeiro_jogador else 200
        coordenada_x = minha_casa.coordenada_x
        casa_adversario = list(
            filter(
                lambda x: x.coordenada_x == coordenada_x
                and x.coordenada_y == coordenada_y,
                self.elementos_da_tela,
            )
        )[0]
        numero_de_pecas_adversario = casa_adversario.numero_de_pecas
        casa_adversario.numero_de_pecas = 0
        return numero_de_pecas_adversario

    def comer_pecas_do_adversario_e_mover_para_minha_kallah(
        self, indice_da_minha_casa: int
    ):
        minha_kallah: Kallah = self.elementos_da_tela[self.indice_minha_kallah]
        numero_pecas_para_adicionar_em_minha_kallah = (
            self.pegar_as_pecas_da_casa_adversaria_e_zerar_seu_valor(
                indice_da_minha_casa
            )
        )
        numero_pecas_para_adicionar_em_minha_kallah += 1
        minha_kallah.numero_de_pecas += numero_pecas_para_adicionar_em_minha_kallah

    def movimentar_pecas_no_tabuleiro(
        self, numero_de_pecas_a_mover: int, indice_do_elemento_que_foi_clicado: int
    ):
        indice = indice_do_elemento_que_foi_clicado + 1
        if numero_de_pecas_a_mover == 1:
            self.comer_pecas_do_adversario_e_mover_para_minha_kallah(
                indice_do_elemento_que_foi_clicado
            )
            numero_de_pecas_a_mover = 0

        while numero_de_pecas_a_mover:
            if indice == 14:
                indice = 0
            casa = self.elementos_da_tela[indice]
            if not (
                isinstance(casa, Kallah) and casa.nome_jogador != self.nome_jogador
            ):
                if (
                    numero_de_pecas_a_mover == 1
                    and isinstance(casa, Kallah)
                    and casa.nome_jogador == self.nome_jogador
                ):
                    # todo pensar em alguma maneira melhor de indicar isso ao jogador
                    print("VOCÊ TEM DIREITO A MAIS UMA JOGADA!!!!!!!!")
                casa.numero_de_pecas += 1
                numero_de_pecas_a_mover -= 1
                self.elementos_da_tela[indice] = casa

            indice = indice + 1

    def clicou_em_alguma_das_minhas_casa(self, coordenas_do_clique: Tuple[int]):
        resultado = False
        for elemento in self.elementos_da_tela:
            if (
                isinstance(elemento, Casa)
                and elemento.nome_jogador == self.nome_jogador
            ):
                elemento_clicado = elemento.fui_clicado(
                    coordenas_do_clique, self.tela, self.nome_jogador
                )
                if elemento_clicado:
                    numero_de_pecas_a_mover = elemento.numero_de_pecas
                    elemento.numero_de_pecas = 0
                    # self.desenhar_elemento(tela)
                    indice = self.elementos_da_tela.index(elemento)
                    # elemento.desenhar_elemento(self.tela)
                    # self.mostrar_tela_do_jogador()
                    self.movimentar_pecas_no_tabuleiro(
                        numero_de_pecas_a_mover=numero_de_pecas_a_mover,
                        indice_do_elemento_que_foi_clicado=indice,
                    )
                    resultado = True
                    # self.verficar_se_alguem_ganhou()
                    break

        return resultado

    def pegar_os_valores_das_casas_e_kallah(self) -> List[int]:
        valores = []
        for elemento in self.elementos_da_tela:
            valores.append(elemento.numero_de_pecas)

        return valores

    def verificar_se_nao_tem_mais_pecas_em_suas_casas(self, lista_de_casas) -> bool:
        resultado = all(casa.numero_de_pecas == 0 for casa in lista_de_casas)
        return resultado

    def verficar_se_alguem_ganhou(self):
        # Condição para que o jogo acabe:
        # - todas as casas de um dos jogadores não deve ter mais peças
        # - se ainda tiver peças nas casas do adversario,
        #   elas são automaticamente movidas para a kallah do adversário
        minhas_casas = list(
            filter(
                lambda x: x.nome_jogador == self.nome_jogador and isinstance(x, Casa),
                self.elementos_da_tela,
            )
        )
        casas_adversario = list(
            filter(
                lambda x: x.nome_jogador != self.nome_jogador and isinstance(x, Casa),
                self.elementos_da_tela,
            )
        )
        minha_kallah = self.elementos_da_tela[self.indice_minha_kallah]
        kallah_adversario = self.elementos_da_tela[self.indice_kallah_adversario]

        sem_pecas_minhas_casas = self.verificar_se_nao_tem_mais_pecas_em_suas_casas(
            minhas_casas
        )
        sem_pecas_casas_adversario = self.verificar_se_nao_tem_mais_pecas_em_suas_casas(
            casas_adversario
        )

        if sem_pecas_minhas_casas or sem_pecas_casas_adversario:
            print("ACABOU A PARTIDA, PESSOAAAAAAAAL!")
            print("definindo vencedor....")
            pecas_a_serem_movidas_pra_kallah = 0
            if sem_pecas_minhas_casas:
                for casa in casas_adversario:
                    indice = self.elementos_da_tela.index(casa)
                    pecas_a_serem_movidas_pra_kallah += casa.numero_de_pecas
                    casa.numero_de_pecas = 0
                    self.elementos_da_tela[indice] = casa

                indice = self.elementos_da_tela.index(kallah_adversario)
                kallah_adversario.numero_de_pecas += pecas_a_serem_movidas_pra_kallah
                self.elementos_da_tela[indice] = kallah_adversario

            else:
                for casa in minhas_casas:
                    pecas_a_serem_movidas_pra_kallah += casa.numero_de_pecas
                    casa.numero_de_pecas = 0
                    indice = self.elementos_da_tela.index(casa)
                    self.elementos_da_tela[indice] = casa

                indice = self.elementos_da_tela.index(minha_kallah)
                minha_kallah.numero_de_pecas += pecas_a_serem_movidas_pra_kallah
                self.elementos_da_tela[indice] = minha_kallah

            kallah_do_vencer = (
                1
                if self.elementos_da_tela[6].numero_de_pecas
                > self.elementos_da_tela[13].numero_de_pecas
                else 2
            )

            vencedor = f"O jogador {kallah_do_vencer} venceu a partida"
            print(vencedor)
            texto_vencedor = Texto(
                300,
                350,
                VERMELHO,
                vencedor,
            )
            texto_vencedor.desenhar_elemento(self.tela)

    @staticmethod
    def mostrar_tela_do_jogador():
        pygame.display.flip()
