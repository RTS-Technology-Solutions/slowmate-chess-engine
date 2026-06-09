"""Compare two PGN sets for A/B opening-book experiments."""

import argparse
import io
from pathlib import Path
from typing import Dict

import chess.pgn


def collect_stats(folder: Path, only_rapid: bool) -> Dict[str, float]:
    stats = {
        "games": 0,
        "wins": 0,
        "losses": 0,
        "draws": 0,
        "score": 0.0,
        "avg_opp_elo": 0.0,
    }
    elo_sum = 0
    elo_count = 0

    for pgn_file in folder.rglob("*.pgn"):
        text = pgn_file.read_text(encoding="utf-8", errors="ignore")
        stream = io.StringIO(text)
        while True:
            game = chess.pgn.read_game(stream)
            if game is None:
                break

            headers = game.headers
            if only_rapid and headers.get("Event", "").lower().find("rapid") == -1:
                continue

            result = headers.get("Result", "*")
            white = headers.get("White", "")
            black = headers.get("Black", "")
            if "slowmate" not in white.lower() and "slowmate" not in black.lower():
                continue

            stats["games"] += 1
            slowmate_white = "slowmate" in white.lower()

            if result == "1/2-1/2":
                stats["draws"] += 1
                stats["score"] += 0.5
            elif result == "1-0":
                if slowmate_white:
                    stats["wins"] += 1
                    stats["score"] += 1.0
                else:
                    stats["losses"] += 1
            elif result == "0-1":
                if slowmate_white:
                    stats["losses"] += 1
                else:
                    stats["wins"] += 1
                    stats["score"] += 1.0

            opp_elo_key = "BlackElo" if slowmate_white else "WhiteElo"
            try:
                elo_sum += int(headers.get(opp_elo_key, 0))
                elo_count += 1
            except Exception:
                pass

    if elo_count:
        stats["avg_opp_elo"] = elo_sum / elo_count
    return stats


def format_stats(label: str, stats: Dict[str, float]) -> str:
    games = int(stats["games"])
    score_pct = (stats["score"] / games * 100.0) if games else 0.0
    return (
        f"{label}: games={games}, wins={int(stats['wins'])}, losses={int(stats['losses'])}, "
        f"draws={int(stats['draws'])}, score={stats['score']:.1f} ({score_pct:.1f}%), "
        f"avg_opp_elo={stats['avg_opp_elo']:.1f}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare A/B PGN result sets")
    parser.add_argument("--a", required=True, help="Folder for Variant A PGNs")
    parser.add_argument("--b", required=True, help="Folder for Variant B PGNs")
    parser.add_argument("--only-rapid", action="store_true", help="Compare only rapid games")
    args = parser.parse_args()

    stats_a = collect_stats(Path(args.a), args.only_rapid)
    stats_b = collect_stats(Path(args.b), args.only_rapid)

    print(format_stats("A", stats_a))
    print(format_stats("B", stats_b))
    print(f"Delta score (B-A): {stats_b['score'] - stats_a['score']:.1f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
