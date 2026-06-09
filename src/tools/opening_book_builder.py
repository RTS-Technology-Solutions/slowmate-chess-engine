"""
Build a SlowMate opening book from PGN corpora.

Output format matches `data/openings/opening_book.json` expectations:
{
  "<fen>": [
    {"move": "e2e4", "weight": 40, "style": "aggressive", "note": "..."},
    ...
  ]
}
"""

import argparse
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, Iterable, List, Tuple

import chess
import chess.pgn
from chess.pgn import GameBuilder


MoveCountMap = DefaultDict[str, DefaultDict[str, int]]


class QuietGameBuilder(GameBuilder):
    """PGN visitor that ignores parse errors and continues ingestion."""

    def handle_error(self, error: Exception) -> None:
        # Ignore malformed SAN fragments and continue with next game.
        return


def iter_pgn_files(input_path: Path) -> Iterable[Path]:
    """Yield PGN files from a single file path or a directory tree."""
    if input_path.is_file() and input_path.suffix.lower() == ".pgn":
        yield input_path
        return

    for pgn_file in sorted(input_path.rglob("*.pgn")):
        if pgn_file.is_file():
            yield pgn_file


def classify_style(uci_move: str) -> str:
    """Simple style heuristic for move metadata compatibility."""
    if uci_move in {"e2e4", "e7e5", "f2f4", "f7f5", "c2c4", "c7c5"}:
        return "aggressive"
    if uci_move in {"d2d4", "d7d5", "g1f3", "g8f6", "b1c3", "b8c6"}:
        return "positional"
    return "flexible"


def collect_opening_counts(input_path: Path, max_halfmoves: int) -> MoveCountMap:
    """Collect move frequencies keyed by position FEN in the opening phase."""
    counts: MoveCountMap = defaultdict(lambda: defaultdict(int))

    for pgn_file in iter_pgn_files(input_path):
        with pgn_file.open("r", encoding="utf-8", errors="ignore") as handle:
            while True:
                game = chess.pgn.read_game(handle, Visitor=QuietGameBuilder)
                if game is None:
                    break

                if game.errors:
                    continue

                board = game.board()
                ply = 0
                for move in game.mainline_moves():
                    if ply >= max_halfmoves:
                        break

                    fen = board.fen()
                    uci = move.uci()
                    counts[fen][uci] += 1
                    board.push(move)
                    ply += 1

    return counts


def build_opening_book(
    counts: MoveCountMap,
    min_count: int,
    top_k: int,
) -> Dict[str, List[Dict[str, object]]]:
    """Convert raw counts into weighted SlowMate opening-book entries."""
    opening_book: Dict[str, List[Dict[str, object]]] = {}

    for fen, move_counts in counts.items():
        filtered = [(move, count) for move, count in move_counts.items() if count >= min_count]
        if not filtered:
            continue

        filtered.sort(key=lambda item: (-item[1], item[0]))
        top_moves = filtered[:top_k]
        total = sum(count for _, count in top_moves)
        if total <= 0:
            continue

        entries: List[Dict[str, object]] = []
        for move, count in top_moves:
            weight = max(1, int(round((count / total) * 100)))
            entries.append(
                {
                    "move": move,
                    "weight": weight,
                    "style": classify_style(move),
                    "note": f"learned from corpus frequency={count}",
                }
            )

        opening_book[fen] = entries

    return opening_book


def main() -> int:
    parser = argparse.ArgumentParser(description="Build SlowMate opening book from PGN corpus")
    parser.add_argument("--input", required=True, help="PGN file or directory")
    parser.add_argument(
        "--output",
        default="data/openings/opening_book_generated_v3_5.json",
        help="Output JSON path",
    )
    parser.add_argument("--max-halfmoves", type=int, default=30, help="Max plies per game to ingest")
    parser.add_argument("--min-count", type=int, default=3, help="Min frequency to keep a move")
    parser.add_argument("--top-k", type=int, default=4, help="Top moves per position")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    counts = collect_opening_counts(input_path, max_halfmoves=args.max_halfmoves)
    opening_book = build_opening_book(counts, min_count=args.min_count, top_k=args.top_k)

    output_path = Path(args.output)
    if not output_path.is_absolute():
        output_path = Path(os.getcwd()) / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(opening_book, handle, indent=2)

    print(f"Generated {len(opening_book)} opening positions to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
