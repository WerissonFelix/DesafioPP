import math

from entities.personagem import Personagem
import pygame, random

class Vilao(Personagem):
    def __init__(self, nome, vida, ataque, defesa, x, y, largura, altura, cor):
        super().__init__(nome, vida, ataque, defesa, x, y, largura, altura, cor)
        self.padrao_tempo = 0

    def atualizar(self, heroi):
        """Lógica de IA a ser sobrescrita"""
        pass
    

class Hornet(Vilao):
    def __init__(self):
        super().__init__("Hornet", 150, 20, 5, 600, 450, 40, 50, (220,20,60))
        self.velocidade = 3
        self.agulha_cooldown = 0
        self.agulhas = []  # lista de projéteis

    def atualizar(self, heroi):
        # Move em direção ao herói
        if self.x < heroi.x:
            self.x += self.velocidade
        else:
            self.x -= self.velocidade

        # Lança agulha a cada 50 frames
        if self.agulha_cooldown > 0:
            self.agulha_cooldown -= 1
        else:
            self.agulha_cooldown = 50
            # Cria projétil
            dx = heroi.x - self.x
            dy = heroi.y - self.y
            dist = (dx**2 + dy**2)**0.5 or 1
            vel_x = dx/dist * 7
            vel_y = dy/dist * 7
            self.agulhas.append(Projetil(self.x + self.largura//2,
                                         self.y + self.altura//2,
                                         vel_x, vel_y, (255,100,100)))
        # Atualiza projéteis
        for ag in self.agulhas[:]:
            ag.mover()
            if ag.x < 0 or ag.x > 800 or ag.y < 0 or ag.y > 600:
                self.agulhas.remove(ag)
        
        self.aplicar_limites(800, 600)

class Projetil:
    def __init__(self, x, y, vel_x, vel_y, cor):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.cor = cor
        self.raio = 6

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

class Irmas(Vilao):
    def __init__(self):
        # A vida total representa o trio; elas compartilham uma barra
        super().__init__("Irmãs de Batalha", 300, 15, 3, 600, 200, 50, 50, (0,150,200))
        self.irmaos = [
            {"x": 600, "y": 200, "cor": (0,200,200), "larg": 30, "alt": 40},
            {"x": 650, "y": 250, "cor": (0,180,180), "larg": 30, "alt": 40},
            {"x": 550, "y": 250, "cor": (0,160,160), "larg": 30, "alt": 40}
        ]
        self.tempo_ataque = 0

    def atualizar(self, heroi):
        # Movimento orbital simples
        self.tempo_ataque += 1
        for i, irma in enumerate(self.irmaos):
            # Cada uma se move lentamente em direção ao herói
            if irma["x"] < heroi.x: irma["x"] += 2
            else: irma["x"] -= 2
            if irma["y"] < heroi.y: irma["y"] += 2
            else: irma["y"] -= 2
            
        if irma["x"] < 0:
            irma["x"] = 0
        elif irma["x"] + irma["larg"] > 800:
            irma["x"] = 800 - irma["larg"]
        if irma["y"] < 0:
            irma["y"] = 0
        elif irma["y"] + irma["alt"] > 600:
            irma["y"] = 600 - irma["alt"]
        # A cada 80 frames, a irmã mais próxima ataca (causa dano se tocar)
        # Implementação simples: verificamos colisão com o herói (na batalha)

    def desenhar(self, tela):
        for irma in self.irmaos:
            pygame.draw.rect(tela, irma["cor"],
                             (irma["x"], irma["y"], irma["larg"], irma["alt"]))
        # Barra de vida única
        barra_larg = 200
        pygame.draw.rect(tela, (255,0,0), (300, 20, barra_larg, 20))
        pygame.draw.rect(tela, (0,255,0), (300, 20, barra_larg * (self.vida/self.vida_max), 20))


class Radiancia(Vilao):
    def __init__(self):
        super().__init__("Radiância", 400, 25, 8, 350, 100, 80, 80, (255,255,100))
        self.fase = 0
        self.tiro_cooldown = 0
        self.espinhos = []
        self.plataformas = []

        self.timer_plataformas = 0
        self.intervalo_plataformas = 600  # 10 segundos (60 FPS)

        self.duracao_plataforma = 180 
    def atualizar(self, heroi):
        # Flutua suavemente de um lado para o outro
        self.x += 2 * (1 if self.fase % 2 == 0 else -1)
        if self.x > 650: self.fase += 1
        if self.x < 150: self.fase += 1
        self.timer_plataformas += 1

        if self.timer_plataformas >= self.intervalo_plataformas:
            self.timer_plataformas = 0
            self.criar_plataformas()
        for plataforma in self.plataformas[:]:
            plataforma["tempo"] -= 1

            if plataforma["tempo"] <= 0:
                self.plataformas.remove(plataforma)    
        # Raios (projéteis em leque)
        if self.tiro_cooldown <= 0:
            self.tiro_cooldown = 30
            ang_base = math.atan2(heroi.y - self.y, heroi.x - self.x)
            for offset in [-0.3, 0, 0.3]:
                vel_x = math.cos(ang_base + offset) * 6
                vel_y = math.sin(ang_base + offset) * 6
                self.espinhos.append(Projetil(self.x+40, self.y+40, vel_x, vel_y, (255,200,0)))
        else:
            self.tiro_cooldown -= 1

        for esp in self.espinhos[:]:
            esp.mover()
            if esp.x < 0 or esp.x > 800 or esp.y < 0 or esp.y > 600:
                self.espinhos.remove(esp)
        self.aplicar_limites(800, 600)
    def desenhar(self, tela):
        # Corpo radiante (círculo)
        pygame.draw.circle(tela, self.cor, (int(self.x+40), int(self.y+40)), 40)
        # Raios (linhas ao redor)
        for ang in range(0, 360, 45):
            rad = math.radians(ang)
            dx = 60 * math.cos(rad)
            dy = 60 * math.sin(rad)
            pygame.draw.line(tela, (255,255,0),
                             (self.x+40, self.y+40),
                             (self.x+40+dx, self.y+40+dy), 3)
        for p in self.plataformas:
            pygame.draw.rect(
                tela,
                (220, 220, 220),
                (p["x"], p["y"], p["largura"], p["altura"])
            )
            
        # Barra de vida
        barra_larg = 300
        pygame.draw.rect(tela, (255,0,0), (250, 20, barra_larg, 20))
        pygame.draw.rect(tela, (0,255,0), (250, 20, barra_larg * (self.vida/self.vida_max), 20))

    def criar_plataformas(self):
        for _ in range(2):
            self.plataformas.append({
                "x": random.randint(100, 650),
                "y": random.randint(150, 350),
                "largura": 120,
                "altura": 20,
                "tempo": self.duracao_plataforma
            })