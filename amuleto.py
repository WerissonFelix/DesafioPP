class Amuleto:
    def __init__(self, nome, descricao, efeitos):
        self.nome = nome
        self.descricao = descricao
        # efeitos é um dict com chaves: 'ataque', 'defesa', 'vida_max', 'velocidade', 'tempo_ataque_max'
        self.efeitos = efeitos

    def aplicar(self, heroi):
        heroi.ataque += self.efeitos.get('ataque', 0)
        heroi.defesa += self.efeitos.get('defesa', 0)
        heroi.vida_max += self.efeitos.get('vida_max', 0)
        heroi.vida = min(heroi.vida_max, heroi.vida + self.efeitos.get('vida_max', 0))
        heroi.velocidade += self.efeitos.get('velocidade', 0)
        heroi.tempo_ataque_max = max(1, heroi.tempo_ataque_max + self.efeitos.get('tempo_ataque_max', 0))

# Cartas pré‑definidas (serão sorteadas 3 aleatórias após cada chefe)
CARTAS_DISPONIVEIS = [
    Amuleto("Fúria do Caído", "+8 ataque", {'ataque': 8}),
    Amuleto("Coração Forte", "+20 vida máxima", {'vida_max': 20}),
    Amuleto("Casco Resistente", "+3 defesa", {'defesa': 3}),
    Amuleto("Velocidade Sombria", "+2 velocidade", {'velocidade': 2}),
    Amuleto("Nail Rápido", "Ataca mais rápido (-3 frames)", {'tempo_ataque_max': -3}),
    Amuleto("Sangue Vital", "+15 vida (cura 15 agora)", {'vida_max': 15, 'vida': 15}),
    Amuleto("Força Inquebrável", "+12 ataque", {'ataque': 12}),
    Amuleto("Defesa Árdua", "+5 defesa", {'defesa': 5}),
]