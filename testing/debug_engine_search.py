"""Debug engine search behavior on disaster positions."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import chess
from src.engine import SlowMateEngine

def test_position(fen: str, description: str):
    """Test engine on a specific position."""
    print(f"\n{'='*70}")
    print(f"Testing: {description}")
    print(f"FEN: {fen}")
    print(f"{'='*70}")
    
    board = chess.Board(fen)
    print(f"\nPosition:\n{board}\n")
    print(f"Turn: {'White' if board.turn else 'Black'}")
    print(f"In check: {board.is_check()}")
    
    # Get legal moves
    legal_moves = list(board.legal_moves)
    print(f"\nLegal moves ({len(legal_moves)}):")
    for move in legal_moves:
        print(f"  {move} (from {chess.square_name(move.from_square)} to {chess.square_name(move.to_square)})")
    
    # Initialize engine
    engine = SlowMateEngine()
    engine.board.board = board.copy()
    
    # Run search
    print(f"\nRunning engine search (5 seconds, depth 6)...")
    best_move = engine.search(time_limit_ms=5000, depth_override=6)
    
    print(f"\nEngine chose: {best_move}")
    if best_move:
        print(f"  From: {chess.square_name(best_move.from_square)}")
        print(f"  To: {chess.square_name(best_move.to_square)}")
        
        # Show what piece is moving
        piece = board.piece_at(best_move.from_square)
        if piece:
            print(f"  Moving: {piece.symbol().upper()} ({piece.piece_type})")
        
        # Check if it hangs the piece
        board.push(best_move)
        captured_piece = None
        for attack_move in board.legal_moves:
            if attack_move.to_square == best_move.to_square:
                attacker = board.piece_at(attack_move.from_square)
                if attacker and attacker.color != piece.color:
                    captured_piece = piece
                    print(f"  WARNING: This hangs the {piece.symbol().upper()} to {attack_move}!")
                    break
        board.pop()
    
    return best_move

if __name__ == "__main__":
    # Position before 12. Ne4?? (Black to move, but let's see White's thinking)
    # After 11... Nc6, White played 12. Ne4?? hanging the knight
    fen1 = "r1bqkb1r/ppp2ppp/2n2n2/3pp3/4P3/2N2N2/PPPP1PPP/R1BQKB1R w KQkq - 4 12"
    
    # Position before 14. Bf4?? (White to move)
    # After 13... Qxe4+, White played 14. Bf4?? hanging the bishop
    fen2 = "r1b1kb1r/ppp2ppp/2n2n2/3pp3/4q3/2N5/PPPP1PPP/R1BQKB1R w KQkq - 0 14"
    
    # Position before 18. Re4?? (White to move)
    # After 17... O-O-O, White played 18. Re4?? hanging the rook
    fen3 = "2kr1b1r/ppp2ppp/2n2n2/3pp3/4q3/2N5/PPPP1PPP/R1BQK2R w KQ - 4 18"
    
    # Test opening position - why did engine play 1. Nh3?
    fen4 = chess.STARTING_FEN
    
    print("SlowMate v3.3 Engine Search Debug")
    print("="*70)
    
    test_position(fen4, "Opening position (why Nh3?)")
    test_position(fen1, "Before 12. Ne4?? blunder")
    test_position(fen2, "Before 14. Bf4?? blunder")
    test_position(fen3, "Before 18. Re4?? blunder")
