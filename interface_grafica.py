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
    def __init__(self, coordenada_x: int, coordenada_y: int, cor: Tuple[int], valor_texto: str):
        self.fonte = pygame.font.SysFont(None, 55)
        self.valor_texto = valor_texto
        super().__init__(coordenada_x, coordenada_y, cor)

    def desenhar_elemento(self, tela):
        texto = self.fonte.render(self.valor_texto, True, VERMELHO)
        tela.blit(texto, [self.coordenada_x, self.coordenada_y])


class Poligono(ElementoTela):
    def __init__(self, coordenada_x: int, coordenada_y: int, cor: Tuple[int], largura: int, comprimento: int, numero_de_pecas_inicial: int):
        self.largura = largura
        self.comprimento = comprimento
        self.numero_de_pecas = numero_de_pecas_inicial
        self.fonte_texto = Texto(int(coordenada_x + (largura/2.5)), int(coordenada_y + (comprimento/3)), VERMELHO, str(self.numero_de_pecas))
        super().__init__(coordenada_x, coordenada_y, cor)

    def desenhar_quantidade_pecas(self, tela):
        self.fonte_texto.desenhar_elemento(tela)

    def desenhar_elemento(self, tela):
        pygame.draw.rect(
            tela, self.cor, [self.coordenada_x, self.coordenada_y, self.largura, self.comprimento]
        )
        self.desenhar_quantidade_pecas(tela)


class Casa(Poligono):
    def __init__(self, coordenada_x: int, coordenada_y: int, cor: Tuple[int], largura: int, comprimento: int):
        super().__init__(coordenada_x, coordenada_y, cor, largura, comprimento, 4)


class Kallah(Poligono):
    def __init__(self, coordenada_x: int, coordenada_y: int, cor: Tuple[int], largura: int, comprimento: int):
        super().__init__(coordenada_x, coordenada_y, cor, largura, comprimento, 0)


class TelaDoJogo:
    def __init__(self, nome_jogador: str):
        self.nome_mostrado_no_display = f"Mancala - {nome_jogador}"
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

    def desenhar_casas_do_tabuleiro(self, coordenada_x_inicial, coordenada_y_inicial, cor):
        while coordenada_x_inicial < 750:
            casa = Casa(coordenada_x_inicial, coordenada_y_inicial, cor, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA)
            self.adicionar_elemento_na_tela(casa)
            coordenada_x_inicial += 100

    def desenhar_kallah(self, x, y, cor, largura, comprimento):
        kallah = Kallah(x, y, cor, largura, comprimento)
        tela_do_jogador.adicionar_elemento_na_tela(kallah)

    def desenhar_tabuleiro(self):
        self.desenhar_casas_do_tabuleiro(coordenada_x_inicial=150, coordenada_y_inicial=100,
                                                    cor=COR_MINHAS_CASAS)
        self.desenhar_casas_do_tabuleiro(coordenada_x_inicial=150, coordenada_y_inicial=200,
                                                    cor=COR_CASAS_ADVERSARIO)

        # desenhando minha kallah
        self.desenhar_kallah(50, 100, COR_MINHAS_CASAS, TAMANHO_LADO_CASA, COMPRIMENTO_KALLAH)
        # desenhando kallah do oponente
        self.desenhar_kallah(750, 100, COR_MINHAS_CASAS, TAMANHO_LADO_CASA, COMPRIMENTO_KALLAH)
        self.desenhar_elementos_na_tela()

    @staticmethod
    def mostrar_tela_do_jogador():
        pygame.display.flip()


tela_do_jogador = TelaDoJogo("italo")
tela_do_jogador.iniciar_tela_do_jogador()

while True:
    tela_do_jogador.desenhar_tabuleiro()
    tela_do_jogador.mostrar_tela_do_jogador()
