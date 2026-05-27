from entities.personagem import Personagem
from entities.vilao import Vilao

class Heroi(Personagem):

    def __init__(self, nome):

        super().__init__(nome, vida=100, ataque=15, defesa=5)
        self.alma = 0          
        self.alma_max = 99
        self.pocoes = 2        
        self.geo = 0           
        self.habilidades = {}  

        self.habilidades = {
            "dash": True,
            "cura": True
        }
    
    def atacar(self, inimigo: Vilao):
        dano = self.ataque
        dano_causado = inimigo.receber_dano(dano)
        self.ganhar_alma(11)   
        self.historico.append(f"Atacou {inimigo.nome} causando {dano_causado}")
        return dano_causado
    
    def usar_foco(self):
        """Gasta alma para curar, igual ao Hollow Knight"""
        custo = 33
        if self.alma >= custo and self.vida < self.vida_max:
            self.alma -= custo
            cura = 50
            self.vida = min(self.vida_max, self.vida + cura)
            self.historico.append(f"Usou Foco. Vida: {self.vida}")
            return True
        return False
    
    def usar_pocao(self):
        if self.pocoes > 0:
            self.pocoes -= 1
            self.vida = self.vida_max
            self.historico.append("Usou poção — vida cheia")
            return True
        return False
    def ganhar_alma(self, quantidade):
        self.alma = min(self.alma_max, self.alma + quantidade)

    def coletar_geo(self, quantidade):
        self.geo += quantidade
        self.historico.append(f"Coletou {quantidade} Geo. Total: {self.geo}")