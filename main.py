from gameManager import GameManager

if __name__ == "__main__":
    print("=== PANTEÃO DOS DEUSES ===")
    print("Uma homenagem a Hollow Knight\n")

    gm = GameManager()
    jogar_novamente = True
    while jogar_novamente:
        gm.iniciar_run()
        resposta = input("\nTentar novamente? (s/n): ")
        jogar_novamente = resposta.lower() == "s"
        if jogar_novamente:
            gm = GameManager() 