from entities.heroi import Heroi
from entities.vilao import BossVilao
from sala import Room
from utils import batalha
import random

class GameManager:
    def __init__(self):
        self.heroi = None
        self.salas = []
        self.sala_atual = 0
        self.historico_run = []
    
    def iniciar_run(self):
        nome = input("Nome do seu cavaleiro: ")
        self.heroi = Heroi(nome)
        self.heroi.dialogar("O Panteão me aguarda...")

        self.salas = self._gerar_panteao(total_salas=5)
        self.sala_atual = 0
        self.loop_principal()
    
    def _gerar_panteao(self, total_salas):
        salas = []
        for i in range(total_salas - 1):
            tipo = random.choice(["combate", "combate", "tesouro", "descanso"])
            salas.append(Room(i + 1, tipo))
        salas.append(Room(total_salas, "boss"))
        return salas
    
    def proxima_sala(self):
        if self.sala_atual >= len(self.salas):
            print("\n Panteão concluído!")
            return False

        sala = self.salas[self.sala_atual]
        print(f"\n\n[ Sala {sala.numero} — {sala.tipo.upper()} ]")

        if sala.tipo in ("tesouro", "descanso"):
            sala.evento(self.heroi)

        elif sala.tipo == "combate":
            for inimigo in sala.inimigos:
                resultado = batalha(self.heroi, inimigo)
                if resultado == "derrota":
                    return False

        elif sala.tipo == "boss":
            boss = BossVilao(
                nome="Radiância Absoluta",
                vida=200, ataque=25, defesa=10,
                fases_hp=[0.6, 0.3],
                falas={1: "Você ousou entrar no Panteão?",
                       2: "Impossível... MAIS PODER!",
                       3: "Não... posso... ser derrotado..."}
            )
            resultado = batalha(self.heroi, boss)
            if resultado == "derrota":
                return False

        self.sala_atual += 1
        return True
    
    def loop_principal(self):
        while self.proxima_sala():
            if not self.heroi.esta_vivo():
                break
            input("\n[Enter para continuar...]")

        print("\n--- Histórico da Run ---")
        for evento in self.heroi.historico[-10:]:
            print(f"  • {evento}")
