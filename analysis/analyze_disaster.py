import chess
import chess.pgn
import io

pgn = """[Event "rated rapid game"]
[Site "https://lichess.org/VJf9eflV"]
[White "slowmate_bot"]
[Black "v7p3r"]
[Result "0-1"]

1. Nh3 d5 2. d4 e5 3. e4 Bxh3 4. dxe5 Nd7 5. exd5 Nxe5 6. Qd4 Qd6 7. Qxe5+ Qxe5+ 8. Be2 Bb4+ 9. Nc3 Bc5 10. O-O Bb4 11. Bb5+ c6 12. Ne4 Qxe4 13. Bxc6+ bxc6 14. Bf4 Qxf4 15. Rae1+ Ne7 16. Rxe7+ Kxe7 17. Re1+ Kf6 18. Re4 Qxe4 19. Kh1 Qe1#"""

game = chess.pgn.read_game(io.StringIO(pgn))
board = game.board()

print("SlowMate v3.3 Game Analysis")
print("=" * 60)
print()

critical_moves = [1, 3, 12, 14, 18, 19]
move_num = 0

for move in game.mainline_moves():
    move_num += 1
    board.push(move)
    
    if move_num in critical_moves:
        print(f"Move {move_num}: {move}")
        print(board)
        print()
        
        # Check for immediate threats
        if board.is_checkmate():
            print("⚠️ CHECKMATE!")
        elif board.is_check():
            print("⚠️ IN CHECK")
        
        print()

print("\n" + "=" * 60)
print("MAJOR ISSUES IDENTIFIED:")
print("=" * 60)
print("1. Move 1 (Nh3): Terrible opening - knight to the rim")
print("2. Move 3 (e4): Allowed Bxh3, losing knight for nothing")  
print("3. Move 12 (Ne4): Blundered queen trade, allowed Qxe4")
print("4. Move 14 (Bf4): Blundered bishop, allowed Qxf4")
print("5. Move 18 (Re4): Final blunder - rook en prise to Qxe4")
print("6. Move 19 (Kh1): Walked into Qe1# checkmate")
print()
print("SlowMate gave away: Knight + Bishop + Rook + got mated")
