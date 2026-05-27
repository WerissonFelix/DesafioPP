class Personagem:
    """
    A classe Personagem representa um personagem genérico em um jogo.
    """
    def __init__(self, nome, vida, ataque, defesa):
        self.nome = nome
        self.vida = vida
        self.vida_max = vida
        self.ataque = ataque
        self.defesa = defesa
        self.historico = []

    def curar(self, incremento=10):
        """
        Aumenta a vida do personagem. O valor padrão de incremento é 10.
        """
        self.vida += incremento
        print(f'Vida de {self.nome} após upgrade: {self.vida}')

    def receber_dano(self, dano):

        dano_final = max(1, dano - self.defesa)

        self.vida -= dano_final

        return dano_final

    def update_nome(self, nome_editado):
        """
        Atualiza o nome do personagem.
        """
        self.nome = nome_editado
    
    def esta_vivo(self):
        return self.vida > 0

    def dialogar(self, mensagem):
        print(f"\n[{self.nome}]: \"{mensagem}\"")
    
    def __str__(self):
        return f'Personagem: {self.nome}, Idade: {self.idade}, Vida: {self.vida}'
