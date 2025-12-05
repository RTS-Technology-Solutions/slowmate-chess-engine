"""
Quick verification that v3.3 mate detection works without opening book
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import chess
from src.engine import SlowMateEngine

# Disable opening book for true testing
engine = SlowMateEngine()
engine.opening_book = None

# Critical v7p3r position - move 40
fen = "r1b2kr1/ppQ2ppp/3p4/6q1/P1PKp1P1/7P/8/8 b - - 3 40"
engine.board.set_fen(fen)

print(f"Testing position: {fen}")
print("Black to move (was winning but played Qd8?? allowing Qxd8#)")

best_move = engine.search(time_limit_ms=10000, depth_override=8)

print(f"\nEngine chose: {best_move}")

# Check if it avoided the blunder
bad_move = chess.Move.from_uci("g5d8")
if best_move == bad_move:
    print("CRITICAL FAILURE: Engine STILL plays the blunder!!")
    sys.exit(1)

# Check if it's a good move
board = chess.Board(fen)
gives_check = board.gives_check(best_move)
print(f"Gives check: {gives_check}")

board.push(best_move)
is_safe = not board.is_checkmate()
print(f"Position is safe: {is_safe}")

if is_safe:
    print("\nSUCCESS: v3.3 mate detection fix is working!")
    print(f"Engine avoided the catastrophic Qd8 blunder and played {best_move}")
else:
    print("\nWARNING: Moved into checkmate")
    sys.exit(1)
