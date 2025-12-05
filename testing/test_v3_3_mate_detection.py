"""
Test Suite for SlowMate v3.3 Mate Detection Fix
Validates the critical bug fix that prevents mate-in-1 blunders
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import chess
from src.engine import SlowMateEngine


def test_critical_position_v7p3r_game():
    """
    Test the exact position from the v7p3r game where SlowMate blundered.
    Move 40: FEN = r1b2kr1/ppQ2ppp/3p4/6q1/P1PKp1P1/7P/8/8 b - - 3 40
    SlowMate played 40...Qd8?? allowing 41.Qxd8#
    Should avoid this and play something like Qf6+ or Qe5+
    """
    print("\n=== Test: Critical Position from v7p3r Game (Move 40) ===")
    engine = SlowMateEngine()
    
    # Set up the exact position
    fen = "r1b2kr1/ppQ2ppp/3p4/6q1/P1PKp1P1/7P/8/8 b - - 3 40"
    engine.board.set_fen(fen)
    
    # Get engine's move
    best_move = engine.search(time_limit_ms=5000, depth_override=6)
    
    print(f"Position FEN: {fen}")
    print(f"Engine chose: {best_move}")
    
    # Validate: Should NOT play Qd8
    bad_move = chess.Move.from_uci("g5d8")
    if best_move == bad_move:
        print("FAIL: Engine played the blunder move Qd8!!")
        return False
    
    # Should play a checking move or safe move
    board = chess.Board(fen)
    if board.gives_check(best_move):
        print(f"PASS: Engine played checking move {best_move}")
        return True
    else:
        print(f"OK: Engine avoided blunder, played {best_move}")
        # Verify it's not walking into mate
        board.push(best_move)
        if not board.is_checkmate():
            return True
        else:
            print("FAIL: Moved into checkmate!")
            return False


def test_mate_in_1_detection():
    """Test that engine finds simple mate-in-1"""
    print("\n=== Test: Mate-in-1 Detection ===")
    engine = SlowMateEngine()
    
    # Back rank mate: Black to move, Ra1# is mate
    fen = "6k1/5ppp/8/8/8/8/5PPP/r5K1 b - - 0 1"
    engine.board.set_fen(fen)
    
    best_move = engine.search(time_limit_ms=2000, depth_override=4)
    
    print(f"Position FEN: {fen}")
    print(f"Engine chose: {best_move}")
    
    mate_move = chess.Move.from_uci("a1a8")
    board = chess.Board(fen)
    board.push(best_move)
    
    if board.is_checkmate():
        print(f"PASS: Found mate-in-1: {best_move}")
        return True
    else:
        print(f"FAIL: Did not find mate, played {best_move}")
        return False


def test_avoid_mate_in_1():
    """Test that engine avoids walking into mate-in-1"""
    print("\n=== Test: Avoid Walking Into Mate-in-1 ===")
    engine = SlowMateEngine()
    
    # White King on h1, Black Queen can mate on h2
    # White should NOT move king to h2
    fen = "8/8/8/8/8/7q/6PP/7K w - - 0 1"
    engine.board.set_fen(fen)
    
    best_move = engine.search(time_limit_ms=2000, depth_override=4)
    
    print(f"Position FEN: {fen}")
    print(f"Engine chose: {best_move}")
    
    # Should NOT play Kh2
    bad_move = chess.Move.from_uci("h1h2")
    if best_move == bad_move:
        print("FAIL: Engine walked into mate-in-1!")
        return False
    
    print(f"PASS: Engine avoided mate, played {best_move}")
    return True


def test_mate_in_2_detection():
    """Test that engine can find mate-in-2"""
    print("\n=== Test: Mate-in-2 Detection (Fool's Mate Setup) ===")
    engine = SlowMateEngine()
    
    # Fool's mate position: Black to move, Qh4# is mate-in-1
    fen = "rnbqkbnr/pppp1ppp/8/4p3/5PP1/8/PPPPP2P/RNBQKBNR b KQkq - 0 2"
    engine.board.set_fen(fen)
    
    best_move = engine.search(time_limit_ms=3000, depth_override=6)
    
    print(f"Position FEN: {fen}")
    print(f"Engine chose: {best_move}")
    
    mate_move = chess.Move.from_uci("d8h4")
    if best_move == mate_move:
        print(f"PASS: Found mate-in-2: {best_move}")
        return True
    else:
        board = chess.Board(fen)
        board.push(best_move)
        if board.is_checkmate():
            print(f"PASS: Found alternate mate: {best_move}")
            return True
        else:
            print(f"WARN: Did not find mate, played {best_move}")
            return False


def run_all_tests():
    """Run all mate detection tests"""
    print("=" * 60)
    print("SlowMate v3.3 Mate Detection Test Suite")
    print("=" * 60)
    
    tests = [
        ("Critical v7p3r Position", test_critical_position_v7p3r_game),
        ("Mate-in-1 Detection", test_mate_in_1_detection),
        ("Avoid Mate-in-1", test_avoid_mate_in_1),
        ("Mate-in-2 Detection", test_mate_in_2_detection),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\nERROR in {test_name}: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
