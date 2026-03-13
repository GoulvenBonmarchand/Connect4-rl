from .game.human import human
from .agents.random_agent import random_agent
from .agents.smart_agent import smart_agent
from .game.board import Board
from .argparse import parse_args

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

def duo(player1, player2) -> None:
    board = Board()

    print("=== Puissance 4 ===")
    print("Joueur 1 = X")
    print("Joueur 2 = O\n")

    players = {
        1: player1,
        2: player2,
    }

    try:
        while True:
            render_board(board)

            current_player = board.turn
            move_fn = players[current_player]

            col = move_fn(board.board, current_player)

            result = board.play(col)

            if not result["ok"]:
                if result["reason"] == "invalid_move":
                    print(
                        f"Le joueur {current_player} a proposé un coup invalide ({col})."
                    )
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

def main() -> None:
    args = parse_args()

    if args.player1 == "human" :
        player1 = human

    if args.player1 == "random" :
        player1 = random_agent
    
    if args.player1 == "smart" :
        player1 = smart_agent

    if args.player2 == "random" :
        player2 = random_agent

    if args.player2 == "human" :
        player2 = human

    if args.player2 == "smart" :
        player2 = smart_agent

    duo(player1, player2)

    