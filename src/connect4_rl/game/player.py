from .board import Board

def render_board(board: Board) -> None:
    """
    Display the board in the terminal.
    """
    symbols = {
        0: ".",
        1: "X",
        2: "O",
    }

    print("\n")
    print("  0 1 2 3 4 5 6")
    print(" ---------------")

    for row in board.board:
        print(" " + " ".join(symbols[cell] for cell in row))

    print("")

def ask_column(player: int) -> int:
    """
    Ask the current player for a column number.
    Keep asking until the input is a valid integer.
    """
    while True:
        value = input(f"Joueur {player} ({'X' if player == 1 else 'O'}), choisis une colonne (0-6) : ").strip()

        if value.lower() in {"q", "quit", "exit"}:
            raise KeyboardInterrupt

        try:
            col = int(value)
            return col
        except ValueError:
            print("Entrée invalide. Tape un entier entre 0 et 6, ou 'q' pour quitter.")

def duo() -> None:
    board = Board()

    print("=== Puissance 4 - mode 1v1 terminal ===")
    print("Joueur 1 = X")
    print("Joueur 2 = O")
    print("Tape 'q' pour quitter.\n")

    try:
        while True:
            render_board(board)

            player = board.turn
            col = ask_column(player)
            result = board.play(col)

            if not result["ok"]:
                if result["reason"] == "invalid_move":
                    print("Coup invalide : colonne hors limites ou pleine. Réessaie.\n")
                continue

            if result["reason"] == "continue":
                continue

            render_board(board)

            if result["reason"] == "win":
                print(f"Victoire du joueur {result['player']} ! 🎉")
                break

            if result["reason"] == "draw":
                print("Égalité ! Le plateau est plein.")
                break

    except KeyboardInterrupt:
        print("\nPartie interrompue.")