import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.engine import SlowMateEngine
import chess

# Test the critical position where SlowMate played Ne4
print("Testing SlowMate v3.3 on disaster game position")
print("=" * 60)
print()

engine = SlowMateEngine()

# Position after 11...c6, before 12.Ne4??
moves_before = ['g1h3', 'd7d5', 'd2d4', 'e7e5', 'e2e4', 'c8h3', 'd4e5', 'b8d7', 
                'e5d5', 'd7e5', 'd1d4', 'd8d6', 'd4e5', 'd6e5', 'f1e2', 'f8b4',
                'b1c3', 'b4c5', 'e1g1', 'c5b4', 'e2b5', 'c7c6']

board = chess.Board()
for m in moves_before:
    board.push(chess.Move.from_uci(m))

print("Position before 12.Ne4??:")
print(board)
print()
print("White to move")
print()

# Test what the engine would play
engine.board.set_fen(board.fen())
print("Searching...")
best_move, score, pv = engine.search(depth_override=5)

print(f"Engine wants to play: {best_move}")
print(f"Evaluation: {score}")
print(f"PV: {' '.join([str(m) for m in pv[:5]])}")
print()

# Check if this is the blunder
if best_move == chess.Move.from_uci('c3e4'):
    print("⚠️ ENGINE WANTS TO PLAY Ne4 - THE BLUNDER!")
    print("This loses the knight to Qxe4")
else:
    print("✓ Engine found a better move")

print()
print("=" * 60)
print()

# Now test position after 18.Re4??
print("Testing position before final blunder...")
moves_to_18 = moves_before + ['c3e4', 'e5e4', 'b5c6', 'b7c6', 'c1f4', 'e4f4',
                               'a1e1', 'g8e7', 'e1e7', 'e8e7', 'f1e1', 'e7f6']
board2 = chess.Board()
for m in moves_to_18:
    board2.push(chess.Move.from_uci(m))

print("Position before 18.Re4??:")
print(board2)
print()

engine.board.set_fen(board2.fen())
best_move2, score2, pv2 = engine.search(depth_override=5)

print(f"Engine wants to play: {best_move2}")
print(f"Evaluation: {score2}")

if best_move2 == chess.Move.from_uci('e1e4'):
    print("⚠️ ENGINE WANTS TO PLAY Re4 - HANGING THE ROOK!")
else:
    print("✓ Engine found a better move")
