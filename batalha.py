import pygame
from utils import desenhar_texto

class Batalha:
    def __init__(self, heroi, vilao, tela):
        self.heroi = heroi
        self.vilao = vilao
        self.tela = tela
        self.fonte = pygame.font.Font(None, 24)
        self.relogio = pygame.time.Clock()
        self.encerrada = False
        self.vencedor = None
        self.mensagens = []  # histórico de ações

    def executar(self):
        rodando = True
        while rodando and not self.encerrada:
            dt = self.relogio.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        teclas = pygame.key.get_pressed()

                        if teclas[pygame.K_UP]:
                            self.heroi.direcao_ataque = "cima"

                        elif teclas[pygame.K_DOWN]:
                            self.heroi.direcao_ataque = "baixo"

                        else:
                            self.heroi.direcao_ataque = (
                                "direita" if self.heroi.direcao == 1 else "esquerda"
                            )

                        self.heroi.atacar()
                        self.mensagens.append("Knight atacou!")
                    if event.key == pygame.K_x:  # curar
                        if self.heroi.cura_cooldown == 0:
                            self.heroi.curar()
                            self.mensagens.append("Knight usou foco!")
                    if event.key == pygame.K_SPACE:
                        self.heroi.pular()
            teclas = pygame.key.get_pressed()
            if self.vilao.nome == "Radiância":
                self.heroi.mover(teclas, self.vilao.plataformas)
                for p in self.vilao.plataformas:
                    pygame.draw.rect(
                        self.tela,
                        (220, 220, 220),
                        (
                            p["x"],
                            p["y"],
                            p["largura"],
                            p["altura"]
                        )
                    )
            else:
                self.heroi.mover(teclas, [])  
                
            self.heroi.atualizar_status()
            self.vilao.atualizar(self.heroi)

            # Colisão de ataque do herói
            self.tela.fill((30,30,30))
            
            area = self.heroi.area_ataque()
            if area and self.heroi.ataque_ativo and not self.heroi.acertou_ataque:
                # Verifica se atinge o vilão
                if self.vilao.nome == "Irmãs de Batalha":
                    for irma in self.vilao.irmaos:
                        rect_irma = pygame.Rect(irma["x"], irma["y"], irma["larg"], irma["alt"])
                        if area.colliderect(rect_irma):
                            dano = self.vilao.receber_dano(self.heroi.ataque)
                            self.mensagens.append(f"{self.vilao.nome} recebeu {dano} de dano!")
                            break
                else:
                    rect_vilao = pygame.Rect(self.vilao.x, self.vilao.y,
                                             self.vilao.largura, self.vilao.altura)
                    if area.colliderect(rect_vilao):
                        dano = self.vilao.receber_dano(self.heroi.ataque)
                        self.heroi.acertou_ataque = True
                        self.mensagens.append(f"{self.vilao.nome} recebeu {dano} de dano!")

            # Colisão dos projéteis do vilão com o herói
            for proj in getattr(self.vilao, 'agulhas', []) + getattr(self.vilao, 'espinhos', []):
                if pygame.Rect(self.heroi.x, self.heroi.y,
                               self.heroi.largura, self.heroi.altura).collidepoint(proj.x, proj.y):
                    dano = self.heroi.receber_dano(self.vilao.ataque)
                    self.mensagens.append(f"Knight recebeu {dano} de dano!")
                    # Remove projétil
                    if proj in getattr(self.vilao, 'agulhas', []):
                        self.vilao.agulhas.remove(proj)
                    elif proj in getattr(self.vilao, 'espinhos', []):
                        self.vilao.espinhos.remove(proj)

            # Contato direto (caso o vilão encoste no herói)
            if self.vilao.nome != "Irmãs de Batalha":
                rect_heroi = pygame.Rect(self.heroi.x, self.heroi.y, self.heroi.largura, self.heroi.altura)
                rect_vilao = pygame.Rect(self.vilao.x, self.vilao.y, self.vilao.largura, self.vilao.altura)
                if rect_heroi.colliderect(rect_vilao):
                    if not self.heroi.invulneravel:
                        dano = self.heroi.receber_dano(self.vilao.ataque)
                        self.mensagens.append(f"Knight recebeu {dano} de dano!")
                        # Ativar invulnerabilidade
                        self.heroi.invulneravel = True
                        self.heroi.tempo_invulneravel = self.heroi.invulneravel_duracao
            else:
                # Para as Irmãs, verificar cada
                rect_heroi = pygame.Rect(self.heroi.x, self.heroi.y, self.heroi.largura, self.heroi.altura)
                for irma in self.vilao.irmaos:
                    rect_irma = pygame.Rect(irma["x"], irma["y"], irma["larg"], irma["alt"])
                    if rect_heroi.colliderect(rect_irma):
                        dano = self.heroi.receber_dano(self.vilao.ataque)
                        self.mensagens.append(f"Knight recebeu {dano} de dano!")
                        self.heroi.invulneravel = True
                        self.heroi.tempo_invulneravel = self.heroi.invulneravel_duracao

            if not self.heroi.esta_vivo():
                self.encerrada = True
                self.vencedor = "vilao"
            if not self.vilao.esta_vivo():
                self.encerrada = True
                self.vencedor = "heroi"
          
            self.heroi.desenhar(self.tela)
            self.vilao.desenhar(self.tela)
            # Desenha projéteis
            for proj in getattr(self.vilao, 'agulhas', []) + getattr(self.vilao, 'espinhos', []):
                proj.desenhar(self.tela)
            # Área de ataque (opcional)
            # Mensagens recentes
            y = 550
           
            for msg in self.mensagens[-3:]:
                desenhar_texto(self.tela, msg, 10, y, self.fonte, cor=(200,200,200))
                y += 20
            self.heroi.desenhar_ataque(self.tela)
            pygame.display.flip()

        return self.vencedor