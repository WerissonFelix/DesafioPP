from entities.personagem import Personagem
import random

class Vilao(Personagem):
    """
    A classe Vilao representa as características de um vilão no jogo.
    Herda da classe Personagem.
    """
    def __init__(self, nome, vida, ataque, defesa, recompensa_geo):
        super().__init__(nome, vida, ataque, defesa)
        self.recompensa_geo  = recompensa_geo
        self.tipo = "inimigo_comum"        
        
    def atacar(self, heroi):
        return heroi.receber_dano(self.ataque)

    def drop_recompensa(self):
        geo = random.randint(*self.recompensa_geo)
        self.historico.append(f"Dropou {geo} Geo")
        return geo

    def __str__(self):
        return f'Vilão: {self.nome}, Idade: {self.idade}, Vida: {self.vida}, Maldade: {self.maldade}'

class BossVilao(Vilao):
    def __init__(self, nome, vida, ataque, defesa, fases_hp, falas):
        super().__init__(nome, vida, ataque, defesa, recompensa_geo=(80, 150))
        self.tipo = "boss"
        self.fase_atual = 1
        self.fases_hp = fases_hp    
        self.falas = falas        

    def verificar_fase(self):
        porcentagem_hp = self.vida / self.vida_max
        nova_fase = 1
        for i, limiar in enumerate(self.fases_hp, 2):
            if porcentagem_hp <= limiar:
                nova_fase = i
        if nova_fase > self.fase_atual:
            self.fase_atual = nova_fase
            self.mudar_fase()

    def mudar_fase(self):
        self.ataque = int(self.ataque * 1.3)  
        self.fala_boss()

    def fala_boss(self):
        fala = self.falas.get(self.fase_atual, "...")
        self.dialogar(fala)    