import random

from entities.vilao import Vilao
from entities.heroi import Heroi

TIPOS_SALA = ["combate", "tesouro", "descanso", "boss", "evento"]

class Room:
    def __init__(self, numero, tipo=None):
        self.numero = numero
        self.tipo = tipo or random.choice(TIPOS_SALA[:3]) 
        self.inimigos = []
        self.itens = {}
        self.concluida = False
        self.gerar_sala()

    def gerar_sala(self):
        if self.tipo == "combate":
            qtd = random.randint(1, 3)
            for i in range(qtd):
                self.inimigos.append(
                    Vilao("Zumbi", vida=30, ataque=8, defesa=2, recompensa_geo=(5, 15))
                )
        elif self.tipo == "tesouro":
            self.itens["pocao"] = random.randint(1, 2)
            self.itens["geo"] = random.randint(20, 50)
        elif self.tipo == "descanso":
            self.itens["banco_de_alma"] = True

    def evento(self, heroi: Heroi):
        """Aplica os efeitos da sala no herói"""
        if self.tipo == "tesouro":
            heroi.pocoes += self.itens.get("pocao", 0)
            heroi.coletar_geo(self.itens.get("geo", 0))
            print(f"Você encontrou {self.itens}!")
        elif self.tipo == "descanso":
            heroi.vida = heroi.vida_max
            heroi.alma = heroi.alma_max
            print("Banco de alma! Vida e alma restauradas.")