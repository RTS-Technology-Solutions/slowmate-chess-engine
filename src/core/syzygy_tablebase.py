"""
Runtime Syzygy tablebase support for SlowMate.
Uses python-chess Syzygy probing for exact 3-4-5 piece endgames.
"""

import os
from typing import Optional

import chess
import chess.syzygy


class SyzygyTablebase:
    """Wrapper around python-chess Syzygy probing."""

    def __init__(self, tablebase_path: Optional[str] = None, max_pieces: int = 5):
        self.tablebase_path = tablebase_path or os.path.join(
            os.path.dirname(__file__), "../../data/endgames/syzygy/3-4-5"
        )
        self.max_pieces = max_pieces
        self._tablebase = None
        self.available = False
        self._open_tablebase()

    def _open_tablebase(self) -> None:
        """Open Syzygy directory if available."""
        if not os.path.isdir(self.tablebase_path):
            return

        try:
            self._tablebase = chess.syzygy.open_tablebase(self.tablebase_path)
            self.available = True
        except Exception:
            self._tablebase = None
            self.available = False

    def supports_position(self, board: chess.Board) -> bool:
        """Return True if this position is suitable for local tablebase probing."""
        return self.available and len(board.piece_map()) <= self.max_pieces

    def select_move(self, board: chess.Board) -> Optional[chess.Move]:
        """Select the best legal move according to Syzygy WDL/DTZ when available."""
        if not self.supports_position(board):
            return None

        best_move = None
        best_wdl = -3
        best_dtz = 10**9

        for move in board.legal_moves:
            board.push(move)
            try:
                # WDL is from side-to-move perspective in the probed node.
                # Negate because after push it is opponent to move.
                move_wdl = -self._tablebase.probe_wdl(board)

                try:
                    move_dtz = abs(self._tablebase.probe_dtz(board))
                except Exception:
                    move_dtz = 10**9
            except Exception:
                board.pop()
                continue

            board.pop()

            if move_wdl > best_wdl or (move_wdl == best_wdl and move_dtz < best_dtz):
                best_wdl = move_wdl
                best_dtz = move_dtz
                best_move = move

        return best_move
