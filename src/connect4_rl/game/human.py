def human(board, player):
    while True:
        value = input(f"Joueur {player}, choisis une colonne : ")
        if value.lower() == "q":
            raise KeyboardInterrupt
        try:
            return int(value)
        except ValueError:
            print("Entre un entier.")