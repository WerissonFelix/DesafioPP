
import pygame
from amuleto import CARTAS_DISPONIVEIS
def desenhar_texto(tela, texto, x, y, fonte, cor=(255,255,255)):
    surf = fonte.render(texto, True, cor)
    tela.blit(surf, (x, y))

def tela_escolha_amuletos(tela, heroi):
    import random
    
    cartas = random.sample(CARTAS_DISPONIVEIS, 3)
    fonte = pygame.font.Font(None, 28)
    escolha = None
    while escolha is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    escolha = cartas[0]
                elif event.key == pygame.K_2:
                    escolha = cartas[1]
                elif event.key == pygame.K_3:
                    escolha = cartas[2]

        tela.fill((20,20,50))
        desenhar_texto(tela, "Escolha um amuleto (1, 2 ou 3):", 200, 100, fonte, (255,255,0))
        for i, amuleto in enumerate(cartas):
            y = 200 + i*80
            cor = (100,200,255) if i == 0 else (100,200,255)
            pygame.draw.rect(tela, cor, (150, y, 500, 60))
            desenhar_texto(tela, f"{i+1}. {amuleto.nome}", 180, y+10, fonte, (0,0,0))
            desenhar_texto(tela, amuleto.descricao, 180, y+35, fonte, (50,50,50))

        pygame.display.flip()

    heroi.amuletos.append(escolha)
    heroi.aplicar_amuletos()  # reaplica todos (incluindo o novo)