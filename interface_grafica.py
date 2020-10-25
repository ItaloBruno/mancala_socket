"""
    link: https://humberto.io/pt-br/blog/desbravando-o-pygame-1-conhecendo-a-biblioteca/
"""

import time
import pygame
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

# inicializa todos os módulos que necessitam de inicialização dentro do pygame.
pygame.init()

# definição do tamanho da tela
tela = pygame.display.set_mode([LARGURA_TELA, COMPRIMENTO_TELA])

# Título da tela
pygame.display.set_caption("Mancala - Jogador 1")

fonte = pygame.font.SysFont(None, 55)
texto_casa = fonte.render("4", True, VERMELHO)
texto_kallah = fonte.render("0", True, VERMELHO)

# preenche com a cor definida em rgb
tela.fill(COR_PLANO_DE_FUNDO)

# Minhas casas
pygame.draw.rect(
    tela, COR_MINHAS_CASAS, [50, 100, TAMANHO_LADO_CASA, COMPRIMENTO_KALLAH]
)
pygame.draw.rect(
    tela, COR_MINHAS_CASAS, [150, 100, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_MINHAS_CASAS, [250, 100, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_MINHAS_CASAS, [350, 100, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_MINHAS_CASAS, [450, 100, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_MINHAS_CASAS, [550, 100, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_MINHAS_CASAS, [650, 100, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)

tela.blit(texto_kallah, [50 + (TAMANHO_LADO_CASA / 2.5), 175])
tela.blit(texto_casa, [150 + (TAMANHO_LADO_CASA / 2.5), 120])
tela.blit(texto_casa, [250 + (TAMANHO_LADO_CASA / 2.5), 120])
tela.blit(texto_casa, [350 + (TAMANHO_LADO_CASA / 2.5), 120])
tela.blit(texto_casa, [450 + (TAMANHO_LADO_CASA / 2.5), 120])
tela.blit(texto_casa, [550 + (TAMANHO_LADO_CASA / 2.5), 120])
tela.blit(texto_casa, [650 + (TAMANHO_LADO_CASA / 2.5), 120])


# Casas do adversário
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [750, 100, TAMANHO_LADO_CASA, COMPRIMENTO_KALLAH]
)
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [150, 200, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [250, 200, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [350, 200, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [450, 200, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [550, 200, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [650, 200, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)
pygame.draw.rect(
    tela, COR_CASAS_ADVERSARIO, [650, 200, TAMANHO_LADO_CASA, TAMANHO_LADO_CASA]
)

tela.blit(texto_kallah, [750 + (TAMANHO_LADO_CASA / 2.5), 175])
tela.blit(texto_casa, [150 + (TAMANHO_LADO_CASA / 2.5), 220])
tela.blit(texto_casa, [250 + (TAMANHO_LADO_CASA / 2.5), 220])
tela.blit(texto_casa, [350 + (TAMANHO_LADO_CASA / 2.5), 220])
tela.blit(texto_casa, [450 + (TAMANHO_LADO_CASA / 2.5), 220])
tela.blit(texto_casa, [550 + (TAMANHO_LADO_CASA / 2.5), 220])
tela.blit(texto_casa, [650 + (TAMANHO_LADO_CASA / 2.5), 220])

# O flip atualiza a tela com o conteúdo desenhado na superfície screen
# e mostra o conteúdo definido anteriormente na tela
# while True:
pygame.display.flip()

time.sleep(2)
