from .game.player import render_board, ask_column
from .game.board import Board

def main() -> None:
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
