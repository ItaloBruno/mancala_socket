"""
    link usado como base: https://humberto.io/pt-br/blog/desbravando-o-pygame-1-conhecendo-a-biblioteca/
"""

import pygame
from typing import Tuple
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
            self.numero_de_pecas = 0
            self.desenhar_elemento(tela)

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
        kallah = Kallah(x, y, cor, largura, comprimento)
        self.adicionar_elemento_na_tela(kallah)

    def desenhar_tabuleiro(self):
        # Fiz nessa ordem para que eu tenha todos os elementos na ordem anti-horária
        # desenhando minhas casas
        casa_ou_kallah_jogador_1 = self.nome_jogador
        casa_ou_kallah_jogador_2 = ""
        if not self.sou_primeiro_jogador:
            casa_ou_kallah_jogador_1 = ""
            casa_ou_kallah_jogador_2 = self.nome_jogador

        self.desenhar_minhas_casas_do_tabuleiro(
            coordenada_x_inicial=150, coordenada_y_inicial=200, cor=COR_MINHAS_CASAS, nome_jogador=casa_ou_kallah_jogador_1
        )
        # desenhando minha kallah
        self.desenhar_kallah(
            750, 100, COR_MINHAS_CASAS, TAMANHO_LADO_CASA, COMPRIMENTO_KALLAH,
            casa_ou_kallah_jogador_1
        )
        # desenhando casas do adversário
        self.desenhar_casas_do_tabuleiro_adversario(
            coordenada_x_inicial=650, coordenada_y_inicial=100, cor=COR_CASAS_ADVERSARIO, nome_jogador=casa_ou_kallah_jogador_2
        )
        # desenhando kallah do oponente
        self.desenhar_kallah(
            50, 100, COR_CASAS_ADVERSARIO, TAMANHO_LADO_CASA, COMPRIMENTO_KALLAH, casa_ou_kallah_jogador_2
        )
        self.desenhar_elementos_na_tela()

    def clicou_em_alguma_casa(self, coordenas_do_clique: Tuple[int]):
        resultado = False
        for elemento in self.elementos_da_tela:
            if isinstance(elemento, Casa) and elemento.nome_jogador == self.nome_jogador:
                elemento_clicado = elemento.fui_clicado(
                    coordenas_do_clique, self.tela, self.nome_jogador
                )
                if elemento_clicado:
                    # elemento.desenhar_elemento(self.tela)
                    # self.mostrar_tela_do_jogador()
                    resultado = True
                    break

        return resultado

    @staticmethod
    def mostrar_tela_do_jogador():
        pygame.display.flip()
