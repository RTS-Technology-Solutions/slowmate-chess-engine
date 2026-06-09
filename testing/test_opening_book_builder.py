"""Tests for the offline opening book builder."""

import os
import sys
from collections import defaultdict

# Add project root to import path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.tools.opening_book_builder import build_opening_book


def test_build_opening_book_filters_and_orders_moves():
    counts = defaultdict(lambda: defaultdict(int))
    fen = "start-fen"
    counts[fen]["e2e4"] = 30
    counts[fen]["d2d4"] = 20
    counts[fen]["g1f3"] = 2

    book = build_opening_book(counts, min_count=3, top_k=2)
    assert fen in book
    moves = [entry["move"] for entry in book[fen]]
    assert moves == ["e2e4", "d2d4"]


def test_build_opening_book_weights_are_positive():
    counts = defaultdict(lambda: defaultdict(int))
    fen = "test-fen"
    counts[fen]["e2e4"] = 5
    counts[fen]["d2d4"] = 5

    book = build_opening_book(counts, min_count=1, top_k=4)
    entries = book[fen]
    assert len(entries) == 2
    assert all(entry["weight"] >= 1 for entry in entries)
