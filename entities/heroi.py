from entities.personagem import Personagem
import pygame
import math

class Heroi(Personagem):
    def __init__(self, x, y):
        super().__init__("Knight", vida=100, ataque=15, defesa=2,
                         x=x, y=y, largura=30, altura=40, cor=(200,200,200))
        self.velocidade = 6
        self.pulo_velocidade = -14
        self.gravidade = 0.8
        self.vel_y = 0
        self.no_chao = False
        self.tempo_ataque = 0      
        self.tempo_ataque_max = 15 
        self.acertou_ataque = False
        self.ataque_ativo = False
        self.ataque_largura = 40   
        self.ataque_altura = 30
        self.direcao = 1           
        self.amuletos = []         
        self.cura_cooldown = 0
        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.invulneravel_duracao = 60
        self.direcao_ataque = "direita"
        self.max_pulos = 2
        self.pulos_restantes = 2

    def pular(self):
        if self.pulos_restantes > 0:
            self.vel_y = self.pulo_velocidade
            self.no_chao = False
            self.pulos_restantes -= 1
            
    def mover(self, teclas, plataformas):
        
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidade
            self.direcao = -1
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidade
            self.direcao = 1

        # Pulo
        # Gravidade
        self.vel_y += self.gravidade
        self.y += self.vel_y

        self.no_chao = False

        for plataforma in plataformas:

            rect_heroi = pygame.Rect(
                self.x,
                self.y,
                self.largura,
                self.altura
            )

            rect_plataforma = pygame.Rect(
                plataforma["x"],
                plataforma["y"],
                plataforma["largura"],
                plataforma["altura"]
            )

            if rect_heroi.colliderect(rect_plataforma) and self.vel_y > 0:

                self.y = plataforma["y"] - self.altura
                self.vel_y = 0
                self.no_chao = True
                self.pulos_restantes = self.max_pulos
        
        
        # Colisão com o chão (simples)
        if self.y + self.altura >= 500:
            self.y = 500 - self.altura
            self.vel_y = 0
            self.no_chao = True
            self.pulos_restantes = self.max_pulos

        # Atualiza cooldown de ataque
        if self.tempo_ataque > 0:
            self.tempo_ataque -= 1
        else:
            self.ataque_ativo = False

        # Cooldown de cura
        if self.cura_cooldown > 0:
            self.cura_cooldown -= 1
            
        self.aplicar_limites(800, 600)

    def atacar(self):
        self.ataque_ativo = True
        self.acertou_ataque = False
        self.tempo_ataque = self.tempo_ataque_max

    def curar(self):
        if self.cura_cooldown == 0 and self.vida < self.vida_max:
            cura = 20
            self.vida = min(self.vida_max, self.vida + cura)
            self.cura_cooldown = 90  # ~1.5 seg a 60 FPS

    def desenhar_ataque(self, tela):
        if not self.ataque_ativo:
            return

        largura = 100
        altura = 60

        # DIREITA
        if self.direcao_ataque == "direita":

            rect = pygame.Rect(
                self.x + self.largura - 20,
                self.y + self.altura//2 - altura//2,
                largura,
                altura
            )

            pygame.draw.arc(
                tela,
                (255,255,255),
                rect,
                -math.pi/3,
                math.pi/3,
                8
            )

        # ESQUERDA
        elif self.direcao_ataque == "esquerda":

            rect = pygame.Rect(
                self.x - largura + 20,
                self.y + self.altura//2 - altura//2,
                largura,
                altura
            )

            pygame.draw.arc(
                tela,
                (255,255,255),
                rect,
                2*math.pi/3,
                4*math.pi/3,
                8
            )

        # CIMA
        elif self.direcao_ataque == "cima":

            rect = pygame.Rect(
                self.x - 20,
                self.y - 80,
                70,
                80
            )

            pygame.draw.arc(
                tela,
                (255,255,255),
                rect,
                0,
                math.pi,
                8
            )

        # BAIXO
        elif self.direcao_ataque == "baixo":

            rect = pygame.Rect(
                self.x - 20,
                self.y + self.altura - 10,
                70,
                80
            )

            pygame.draw.arc(
                tela,
                (255,255,255),
                rect,
                math.pi,
                2*math.pi,
                8
            )
    def area_ataque(self):
        if not self.ataque_ativo:
            return None

        if self.direcao_ataque == "direita":
            return pygame.Rect(
                self.x + self.largura,
                self.y,
                80,
                40
            )

        elif self.direcao_ataque == "esquerda":
            return pygame.Rect(
                self.x - 80,
                self.y,
                80,
                40
            )

        elif self.direcao_ataque == "cima":
            return pygame.Rect(
                self.x - 5,
                self.y - 80,
                40,
                80
            )

        elif self.direcao_ataque == "baixo":
            return pygame.Rect(
                self.x - 5,
                self.y + self.altura,
                40,
                80
            )
    def aplicar_amuletos(self):
        """Aplica os bônus de todos os amuletos equipados (chamado ao iniciar batalha)"""
        self.vida = self.vida_max  # reseta vida base
        self.ataque = 15
        self.defesa = 2
        self.velocidade = 6
        self.tempo_ataque_max = 15
        for amuleto in self.amuletos:
            amuleto.aplicar(self)
            
    def atualizar_status(self):
        if self.invulneravel:
            self.tempo_invulneravel -= 1
            if self.tempo_invulneravel <= 0:
                self.invulneravel = False
                self.tempo_invulneravel = 0
        