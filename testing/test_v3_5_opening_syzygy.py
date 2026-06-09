"""
SlowMate v3.5 regression tests.
Validates deterministic opening behavior and Syzygy integration.
"""

import os
import sys

import chess

# Add project root to import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engine import SlowMateEngine


def test_opening_move_is_principled():
    """First move should avoid known low-principle openings."""
    engine = SlowMateEngine()
    engine.set_position("startpos")

    move = engine.search(time_limit_ms=100, depth_override=3)
    assert move is not None

    disallowed = {
        "g1h3", "b1a3", "a2a3", "h2h3", "a2a4", "h2h4"
    }
    assert move.uci() not in disallowed, f"Disallowed opening move selected: {move.uci()}"


def test_opening_book_is_deterministic_from_start():
    """Book selection should be deterministic for the same position/opponent."""
    engine = SlowMateEngine()
    board = chess.Board()

    choices = [engine.opening_book.select_strategic_move(board, "V7P3R") for _ in range(5)]
    first = choices[0]
    assert all(choice == first for choice in choices), f"Non-deterministic opening choices: {choices}"


def test_syzygy_move_is_legal_when_available():
    """If Syzygy is available and position is supported, selected move must be legal."""
    engine = SlowMateEngine()

    # KQvK should be supported by 3-4-5 Syzygy.
    board = chess.Board("6k1/8/8/8/8/8/6K1/6Q1 w - - 0 1")

    if not engine.syzygy_tablebase.supports_position(board):
        return

    move = engine.syzygy_tablebase.select_move(board)
    assert move is not None
    assert move in board.legal_moves
