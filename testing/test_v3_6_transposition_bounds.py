import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engine import SlowMateEngine
from src.search.enhanced import NodeType


@pytest.mark.parametrize(
    "search_method",
    [
        "_search_depth",
        "_search_depth_with_pv",
        "_negamax",
        "_negamax_with_pv",
    ],
)
@pytest.mark.parametrize(
    ("alpha", "beta", "expected_type"),
    [
        (-100, 100, NodeType.EXACT),
        (50, 100, NodeType.UPPER),
        (-100, 30, NodeType.LOWER),
    ],
)
def test_search_stores_correct_transposition_bound(
    monkeypatch, search_method, alpha, beta, expected_type
):
    engine = SlowMateEngine()
    monkeypatch.setattr(
        engine,
        "_quiescence_search",
        lambda *_args: -42,
    )
    position_key = hash(engine.board.get_fen())

    if search_method.startswith("_search_depth"):
        moves = engine.move_generator.get_legal_moves()
        method = getattr(engine, search_method)
        method(1, alpha, beta, moves)
    else:
        method = getattr(engine, search_method)
        method(1, alpha, beta)

    assert engine.tt.table[position_key].node_type is expected_type


def test_engine_version_is_v3_6(capsys):
    engine = SlowMateEngine()
    assert engine.get_version() == "3.6"

    engine.uci._handle_uci()

    assert "id name SlowMate v3.6" in capsys.readouterr().out
