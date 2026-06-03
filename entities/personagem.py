import pygame

class Personagem:
    def __init__(self, nome, vida, ataque, defesa, x, y, largura, altura, cor):
        self.nome = nome
        self.vida_max = vida
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.cor = cor
        self.velocidade = 5  

    def receber_dano(self, dano):
        dano_real = max(0, dano - self.defesa)
        self.vida -= dano_real
        if self.vida < 0:
            self.vida = 0
        return dano_real

    def esta_vivo(self):
        return self.vida > 0

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor, (self.x, self.y, self.largura, self.altura))
        # Barra de vida
        if self.vida < self.vida_max:
            barra_larg = self.largura
            barra_alt = 6
            vida_porc = self.vida / self.vida_max
            pygame.draw.rect(tela, (255,0,0), (self.x, self.y-10, barra_larg, barra_alt))
            pygame.draw.rect(tela, (0,255,0), (self.x, self.y-10, barra_larg * vida_porc, barra_alt))
    
    def aplicar_limites(self, largura_tela, altura_tela):
        if self.x < 0:
            self.x = 0
        elif self.x + self.largura > largura_tela:
            self.x = largura_tela - self.largura

        if self.y < 0:
            self.y = 0
        elif self.y + self.altura > altura_tela:
            self.y = altura_tela - self.altura
