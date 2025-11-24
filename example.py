"""Example usage of the `lichess_explorer` client for the general Lichess explorer.

Run:
    python example.py --nb 5

Or with a token (optional, useful for higher limits):
    LICHESS_TOKEN=your-token python example.py --nb 5
"""
import os
import argparse
from lichess_explorer import query_lichess_openings


def pretty_print_openings(data: dict) -> None:
    # The explorer response contains `moves` (list) and other metadata.
    moves = data.get("moves") or []
    if not moves:
        print("No moves returned.")
        return

    for i, mv in enumerate(moves, start=1):
        san = mv.get("san") or mv.get("move") or "?"
        white = mv.get("white")
        black = mv.get("black")
        draws = mv.get("draws")
        wins = mv.get("wins")
        win_rate = None
        try:
            total = (white or 0) + (black or 0) + (draws or 0)
            if total:
                win_rate = round(((white or 0) + 0.5 * (draws or 0)) / total * 100, 1)
        except Exception:
            win_rate = None

        print(f"{i}. {san:8}  white:{white}  black:{black}  draws:{draws}  win%:{win_rate}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nb", type=int, default=10)
    parser.add_argument("--moves", help="Comma-separated SAN moves")
    parser.add_argument("--play-as", choices=["white", "black", "both"], help="playAs filter")
    args = parser.parse_args()

    token = os.environ.get("LICHESS_TOKEN")
    data = query_lichess_openings(nb=args.nb, moves=args.moves, play_as=args.play_as, token=token)
    pretty_print_openings(data)


if __name__ == "__main__":
    main()
