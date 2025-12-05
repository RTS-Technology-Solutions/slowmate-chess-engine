"""Verify the check positions and see what happens after each move."""
import chess

# Position 14: White in check from Qe4
fen14 = "r1b1kb1r/ppp2ppp/2n2n2/3pp3/4q3/2N5/PPPP1PPP/R1BQKB1R w KQkq - 0 14"
board14 = chess.Board(fen14)

print("Position 14 - White in check from Qe4")
print(board14)
print(f"\nIn check: {board14.is_check()}")
print(f"Legal moves: {[move.uci() for move in board14.legal_moves]}\n")

for move in board14.legal_moves:
    board14.push(move)
    print(f"After {move.uci()}: ", end="")
    
    # Check if Black can capture
    can_capture = False
    for response in board14.legal_moves:
        if response.to_square == move.to_square:
            print(f"BLACK CAN CAPTURE WITH {response.uci()}", end="")
            can_capture = True
            break
    
    if not can_capture:
        print("Safe move", end="")
    
    print(f" (eval perspective: {'Black' if board14.turn else 'White'})")
    board14.pop()

print("\n" + "="*70)

# Position 18: White in check from Qe4
fen18 = "2kr1b1r/ppp2ppp/2n2n2/3pp3/4q3/2N5/PPPP1PPP/R1BQK2R w KQ - 4 18"
board18 = chess.Board(fen18)

print("\nPosition 18 - White in check from Qe4")
print(board18)
print(f"\nIn check: {board18.is_check()}")
print(f"Legal moves: {[move.uci() for move in board18.legal_moves]}\n")

for move in board18.legal_moves:
    board18.push(move)
    print(f"After {move.uci()}: ", end="")
    
    # Check if Black can capture
    can_capture = False
    for response in board18.legal_moves:
        if response.to_square == move.to_square:
            print(f"BLACK CAN CAPTURE WITH {response.uci()}", end="")
            can_capture = True
            break
    
    if not can_capture:
        print("Safe move", end="")
    
    print(f" (eval perspective: {'Black' if board14.turn else 'White'})")
    board18.pop()
