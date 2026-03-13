import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Connect4_rl: A Connect4 game with reinforcement learning agents.")
    parser.add_argument(
        "--player1",
        type=str,
        default="humain",
        help="Type of player 1 (options: 'humain', 'random')"
    )
    parser.add_argument(
        "--player2",
        type=str,
        default="humain",
        help="Type of player 2 (options: 'humain', 'random')"
    )
    return parser.parse_args()