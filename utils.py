import time

def batalha(heroi, inimigo):
    print(f"\n{'='*40}")
    print(f"  BATALHA: {heroi.nome} vs {inimigo.nome}")
    print(f"{'='*40}")

    turno = 1
    while heroi.esta_vivo() and inimigo.esta_vivo():
        print(f"\n--- Turno {turno} ---")
        print(f"{heroi.nome}: {heroi.vida}/{heroi.vida_max} HP | Alma: {heroi.alma}")
        print(f"{inimigo.nome}: {inimigo.vida}/{inimigo.vida_max} HP")

      
        print("\n[1] Atacar  [2] Usar Foco  [3] Usar Poção  [4] Fugir")
        acao = input("Ação: ").strip()

        if acao == "1":
            dano = heroi.atacar(inimigo)
            print(f"Você causou {dano} de dano!")
            if hasattr(inimigo, 'verificar_fase'):
                inimigo.verificar_fase()

        elif acao == "2":
            if not heroi.usar_foco():
                print("Alma insuficiente ou vida cheia!")

        elif acao == "3":
            if not heroi.usar_pocao():
                print("Sem poções!")

        elif acao == "4":
            print("Você fugiu!")
            return "fugiu"

      
        if inimigo.esta_vivo():
            dano_recebido = inimigo.atacar(heroi)
            print(f"{inimigo.nome} causou {dano_recebido} de dano em você!")

        turno += 1
        time.sleep(0.3)

    if heroi.esta_vivo():
        geo = inimigo.drop_recompensa()
        heroi.coletar_geo(geo)
        print(f"\nVitória! +{geo} Geo")
        return "vitoria"
    else:
        print(f"\nVocê foi derrotado...")
        return "derrota"