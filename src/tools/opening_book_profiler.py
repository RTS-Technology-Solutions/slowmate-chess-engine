"""Profile and optionally trim SlowMate opening-book JSON files."""

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import chess


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def fen_to_ply(fen: str) -> int:
    fields = fen.split()
    if len(fields) < 6:
        return 0
    turn = fields[1]
    fullmove = int(fields[5])
    return (fullmove - 1) * 2 + (1 if turn == "b" else 0)


def risky_early_move(fen: str, move_uci: str) -> bool:
    try:
        board = chess.Board(fen)
        move = chess.Move.from_uci(move_uci)
    except Exception:
        return False

    if move not in board.legal_moves:
        return False

    if fen_to_ply(fen) > 6:
        return False

    piece = board.piece_at(move.from_square)
    if not piece:
        return False

    if piece.piece_type == chess.KNIGHT:
        rim_knight_jumps = {
            (chess.B1, chess.A3),
            (chess.G1, chess.H3),
            (chess.B8, chess.A6),
            (chess.G8, chess.H6),
        }
        return (move.from_square, move.to_square) in rim_knight_jumps

    if piece.piece_type == chess.PAWN:
        return move.from_square in {chess.A2, chess.H2, chess.A7, chess.H7}

    return False


def normalize_entries(entries: List[dict | str]) -> List[dict]:
    normalized: List[dict] = []
    for entry in entries:
        if isinstance(entry, str):
            normalized.append({"move": entry, "weight": 1, "style": "flexible", "note": "legacy"})
        elif isinstance(entry, dict) and "move" in entry:
            normalized.append(
                {
                    "move": entry["move"],
                    "weight": int(entry.get("weight", 1)),
                    "style": entry.get("style", "flexible"),
                    "note": entry.get("note", ""),
                }
            )
    return normalized


def build_report(book: Dict[str, List[dict | str]]) -> Tuple[str, Dict[str, List[dict]]]:
    by_ply = Counter()
    style_counter = Counter()
    risky_count = 0
    total_moves = 0
    normalized_book: Dict[str, List[dict]] = {}

    for fen, entries in book.items():
        ply = fen_to_ply(fen)
        by_ply[ply] += 1

        normalized = normalize_entries(entries)
        normalized_book[fen] = normalized
        for entry in normalized:
            total_moves += 1
            style_counter[entry.get("style", "flexible")] += 1
            if risky_early_move(fen, entry["move"]):
                risky_count += 1

    start_entries = normalize_entries(book.get(START_FEN, []))
    start_entries.sort(key=lambda item: (-item.get("weight", 1), item["move"]))

    max_ply = max(by_ply.keys()) if by_ply else 0
    lines = [
        "# Opening Book Profile",
        "",
        f"- Positions: {len(book)}",
        f"- Candidate moves: {total_moves}",
        f"- Max opening ply represented: {max_ply}",
        f"- Risky early-move entries: {risky_count}",
        "",
        "## Start Position Choices",
    ]

    if start_entries:
        for entry in start_entries[:10]:
            lines.append(f"- {entry['move']}: weight {entry['weight']} ({entry['style']})")
    else:
        lines.append("- None")

    lines.append("")
    lines.append("## Coverage By Ply (positions)")
    for ply, count in sorted(by_ply.items()):
        lines.append(f"- Ply {ply}: {count}")

    lines.append("")
    lines.append("## Style Distribution (entries)")
    for style, count in style_counter.most_common():
        lines.append(f"- {style}: {count}")

    return "\n".join(lines) + "\n", normalized_book


def trim_book(
    normalized_book: Dict[str, List[dict]],
    min_weight: int,
    top_k: int,
    remove_risky_early: bool,
    max_ply: int,
) -> Dict[str, List[dict]]:
    trimmed: Dict[str, List[dict]] = {}

    for fen, entries in normalized_book.items():
        if fen_to_ply(fen) > max_ply:
            continue

        kept = []
        for entry in entries:
            if entry["weight"] < min_weight:
                continue
            if remove_risky_early and risky_early_move(fen, entry["move"]):
                continue
            kept.append(entry)

        kept.sort(key=lambda item: (-item["weight"], item["move"]))
        kept = kept[:top_k]

        if kept:
            trimmed[fen] = kept

    return trimmed


def main() -> int:
    parser = argparse.ArgumentParser(description="Profile and trim SlowMate opening book")
    parser.add_argument("--input", required=True, help="Input opening-book JSON path")
    parser.add_argument("--report", default="docs/reports/opening_book_profile.md", help="Output report path")
    parser.add_argument("--trim-output", help="Optional output path for trimmed book JSON")
    parser.add_argument("--min-weight", type=int, default=1, help="Trim: minimum weight")
    parser.add_argument("--top-k", type=int, default=4, help="Trim: max moves per position")
    parser.add_argument("--max-ply", type=int, default=30, help="Trim: max opening ply")
    parser.add_argument("--remove-risky-early", action="store_true", help="Trim: remove risky early entries")
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open("r", encoding="utf-8") as handle:
        book = json.load(handle)

    report_text, normalized_book = build_report(book)

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    print(f"Wrote report: {report_path}")

    if args.trim_output:
        trimmed = trim_book(
            normalized_book,
            min_weight=args.min_weight,
            top_k=args.top_k,
            remove_risky_early=args.remove_risky_early,
            max_ply=args.max_ply,
        )
        trim_path = Path(args.trim_output)
        trim_path.parent.mkdir(parents=True, exist_ok=True)
        trim_path.write_text(json.dumps(trimmed, indent=2), encoding="utf-8")
        print(f"Wrote trimmed book: {trim_path} positions={len(trimmed)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
