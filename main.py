import pygame, sys
from entities.heroi import Heroi
from entities.vilao import Hornet, Irmas, Radiancia
from amuleto import Amuleto, CARTAS_DISPONIVEIS
from batalha import Batalha
from utils import desenhar_texto, tela_escolha_amuletos

pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pantheon Rogue‑lite")

heroi = Heroi(400, 500)

chefes = [
    Hornet(),
    Irmas(),
    Radiancia()
]

fonte_grande = pygame.font.Font(None, 48)

def main():
    for idx, chefe in enumerate(chefes):
        # Diálogo antes da luta
        tela.fill((0,0,0))
        desenhar_texto(tela, f"Desafio {idx+1}: {chefe.nome}", 200, 250, fonte_grande, (255,255,255))
        pygame.display.flip()
        pygame.time.wait(2000)

        # Inicia batalha
        batalha = Batalha(heroi, chefe, tela)
        vencedor = batalha.executar()

        if vencedor == "vilao":
            tela.fill((0,0,0))
            desenhar_texto(tela, "Você foi derrotado...", 250, 280, fonte_grande, (255,0,0))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()
        else:
            # Vitória → escolha de amuleto
            tela_escolha_amuletos(tela, heroi)

    # Final do jogo
    tela.fill((0,0,0))
    desenhar_texto(tela, "Você venceu todos os chefes!", 150, 250, fonte_grande, (255,255,0))
    desenhar_texto(tela, "Pressione ESC para sair", 250, 320, fonte_grande, (200,200,200))
    pygame.display.flip()
    esperar_saida()

def esperar_saida():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()