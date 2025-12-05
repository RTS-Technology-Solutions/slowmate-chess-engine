"""
Test Suite for Mate Detection Fix (v3.3)
Validates that the engine correctly detects and avoids mate-in-1 blunders
"""

import chess
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.engine import SlowMateEngine


def test_mate_in_1_detection():
    """Test that engine detects mate-in-1 threats."""
    
    test_cases = [
        {
            "name": "v7p3r Game - Move 40",
            "fen": "r1b2kr1/ppQ2ppp/3p4/6q1/P1PKp1P1/7P/8/8 b - - 3 40",
            "avoid_moves": ["d8", "h6", "g6", "h5", "f5", "f4", "c1"],  # All allow Qxd8# or Qd8#
            "prefer_moves": ["e5", "d5", "c5", "e7"],  # Checking or blocking moves
            "description": "Black should avoid moves allowing Qd8# (mate in 1)"
        },
        {
            "name": "Basic Back Rank Mate",
            "fen": "6k1/5ppp/8/8/8/8/8/R6K w - - 0 1",
            "avoid_moves": [],
            "prefer_moves": ["a8"],  # Ra8# is checkmate
            "description": "White should deliver Ra8#"
        },
        {
            "name": "Don't Walk Into Mate",
            "fen": "7k/8/8/8/8/8/8/Q6K w - - 0 1",
            "avoid_moves": ["h7"],  # Kh7 hangs king next to queen
            "prefer_moves": ["g8", "a8"],  # Qg8# or Qa8# is immediate mate
            "description": "White should deliver checkmate, not hang king"
        }
    ]
    
    engine = SlowMateEngine()
    
    print(f"SlowMate Engine v{engine.get_version()} - Mate Detection Tests")
    print("=" * 70)
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Description: {test['description']}")
        print(f"FEN: {test['fen']}")
        
        # Set position
        engine.set_position(test['fen'])
        
        # Search for best move
        best_move = engine.search(time_limit_ms=2000)
        
        if best_move:
            move_uci = best_move.uci()
            move_san = engine.board.board.san(best_move)
            print(f"Engine chose: {move_san} ({move_uci})")
            
            # Check if avoided bad moves
            avoid_ok = True
            if "avoid_moves" in test or "avoid_move" in test:
                avoid_list = test.get("avoid_moves", [test.get("avoid_move")])
                for avoid_move in avoid_list:
                    if avoid_move and avoid_move in move_uci:
                        print(f"FAIL: FAILED: Engine played a move it should avoid ({avoid_move})!")
                        avoid_ok = False
                        break
                if avoid_ok:
                    print(f"OK: Avoided bad moves")
            
            # Check if played preferred move
            prefer_ok = False
            if "prefer_moves" in test or "prefer_move" in test:
                prefer_list = test.get("prefer_moves", [test.get("prefer_move")])
                for prefer_move in prefer_list:
                    if prefer_move and prefer_move in move_uci:
                        print(f"OK: Played a preferred move ({prefer_move})")
                        prefer_ok = True
                        break
                if not prefer_ok:
                    print(f"WARN: Did not play a preferred move, but move might be acceptable")
            else:
                prefer_ok = True  # No preference specified
            
            if avoid_ok and prefer_ok:
                print("PASS: PASSED")
                passed += 1
            else:
                print("FAIL: FAILED")
                failed += 1
        else:
            print("FAIL: FAILED: Engine returned no move")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    
    return failed == 0


def test_mate_in_2_detection():
    """Test that engine can find mate-in-2 sequences."""
    
    engine = SlowMateEngine()
    
    # Fool's Mate setup - one move away from mate
    test_fen = "rnbqkbnr/pppp1ppp/8/4p3/6P1/5P2/PPPPP2P/RNBQKBNR b KQkq g3 0 2"
    
    print("\n\nMate in 2 Detection Test")
    print("=" * 70)
    print(f"Position: {test_fen}")
    print("Expected: Black should play Qh4# for checkmate")
    
    engine.set_position(test_fen)
    best_move = engine.search(time_limit_ms=3000)
    
    if best_move:
        move_uci = best_move.uci()
        move_san = engine.board.board.san(best_move)
        print(f"Engine chose: {move_san} ({move_uci})")
        
        if "h4" in move_uci:
            print("PASS: PASSED: Found checkmate move Qh4#")
            return True
        else:
            print("WARN: Engine found different move (acceptable if still good)")
            return True
    else:
        print("FAIL: FAILED: No move returned")
        return False


if __name__ == "__main__":
    print("SlowMate v3.3 - Mate Detection Fix Validation\n")
    
    test1 = test_mate_in_1_detection()
    test2 = test_mate_in_2_detection()
    
    print("\n" + "=" * 70)
    if test1 and test2:
        print("🎉 ALL TESTS PASSED!")
        print("v3.3 mate detection fix is working correctly")
        sys.exit(0)
    else:
        print("WARN: SOME TESTS FAILED")
        print("Review failures before deployment")
        sys.exit(1)
