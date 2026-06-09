"""Tests for opening book profiler utility."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.opening_book_profiler import fen_to_ply, risky_early_move, trim_book


def test_fen_to_ply_start_position():
    assert fen_to_ply("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") == 0


def test_risky_early_move_detects_rim_knight():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert risky_early_move(fen, "g1h3") is True
    assert risky_early_move(fen, "g1f3") is False


def test_trim_book_removes_risky_entries():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    book = {
        fen: [
            {"move": "g1h3", "weight": 20, "style": "flexible", "note": "x"},
            {"move": "e2e4", "weight": 30, "style": "aggressive", "note": "x"},
        ]
    }
    trimmed = trim_book(book, min_weight=1, top_k=4, remove_risky_early=True, max_ply=30)
    moves = [entry["move"] for entry in trimmed[fen]]
    assert "g1h3" not in moves
    assert "e2e4" in moves
