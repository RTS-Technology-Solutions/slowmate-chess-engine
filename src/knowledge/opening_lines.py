"""
SlowMate v3.2 - Opening Book Database
Comprehensive opening repertoire to replace catastrophic Nh3 play
Target: +150 ELO improvement from sound opening principles
"""

from __future__ import annotations
import chess
from typing import Dict, List, Tuple, Optional


class OpeningLines:
    """
    In-memory opening book with proven chess opening principles.
    Organized by position FEN -> list of (move_uci, weight) tuples.
    """
    
    def __init__(self):
        """Initialize opening lines database."""
        self.book: Dict[str, List[Tuple[str, int]]] = {}
        self._build_opening_book()
    
    def _build_opening_book(self):
        """Build comprehensive opening book with weighted moves."""
        
        # Starting position - White's first move
        start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.book[start_fen] = [
            ("e2e4", 40),  # King's Pawn - most popular
            ("d2d4", 35),  # Queen's Pawn - solid
            ("g1f3", 15),  # Reti/Indian systems
            ("c2c4", 10),  # English Opening
        ]
        
        # After 1.e4 - Black's responses
        self._add_e4_lines()
        
        # After 1.d4 - Black's responses
        self._add_d4_lines()
        
        # After 1.Nf3 - Black's responses
        self._add_nf3_lines()
        
        # After 1.c4 - Black's responses
        self._add_c4_lines()
    
    def _add_e4_lines(self):
        """Add lines after 1.e4"""
        
        # 1.e4 responses
        after_e4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        self.book[after_e4] = [
            ("e7e5", 45),    # Open Game
            ("c7c5", 30),    # Sicilian Defense
            ("e7e6", 15),    # French Defense
            ("c7c6", 10),    # Caro-Kann Defense
        ]
        
        # 1.e4 e5 - White's second move
        after_e4_e5 = "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2"
        self.book[after_e4_e5] = [
            ("g1f3", 60),  # King's Knight
            ("f2f4", 20),  # King's Gambit
            ("b1c3", 15),  # Vienna Game
            ("f1c4", 5),   # Bishop's Opening
        ]
        
        # 1.e4 e5 2.Nf3 - Black's responses
        after_e4_e5_nf3 = "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        self.book[after_e4_e5_nf3] = [
            ("b8c6", 70),  # Most natural
            ("g8f6", 20),  # Petroff Defense
            ("d7d6", 10),  # Philidor Defense
        ]
        
        # 1.e4 e5 2.Nf3 Nc6 - White's third move
        after_nf3_nc6 = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
        self.book[after_nf3_nc6] = [
            ("f1b5", 50),  # Ruy Lopez
            ("f1c4", 30),  # Italian Game
            ("d2d4", 15),  # Scotch Game
            ("b1c3", 5),   # Four Knights
        ]
        
        # Ruy Lopez: 1.e4 e5 2.Nf3 Nc6 3.Bb5
        ruy_lopez = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
        self.book[ruy_lopez] = [
            ("a7a6", 50),  # Morphy Defense
            ("g8f6", 30),  # Berlin Defense
            ("f7f5", 10),  # Schliemann Defense
            ("g7g6", 10),  # Smyslov Defense
        ]
        
        # Ruy Lopez Morphy: 3...a6
        ruy_morphy = "r1bqkbnr/1ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4"
        self.book[ruy_morphy] = [
            ("b5a4", 70),  # Main line
            ("b5c6", 20),  # Exchange Variation
            ("b5xc6", 10), # Alternative notation
        ]
        
        # Italian Game: 1.e4 e5 2.Nf3 Nc6 3.Bc4
        italian = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
        self.book[italian] = [
            ("f8c5", 40),  # Giuoco Piano
            ("g8f6", 35),  # Two Knights Defense
            ("f8e7", 15),  # Hungarian Defense
            ("d7d6", 10),  # Solid defense
        ]
        
        # Sicilian Defense: 1.e4 c5
        sicilian = "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2"
        self.book[sicilian] = [
            ("g1f3", 70),  # Open Sicilian
            ("b1c3", 20),  # Closed Sicilian
            ("c2c3", 10),  # Alapin Variation
        ]
        
        # Sicilian 2.Nf3
        sicilian_nf3 = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        self.book[sicilian_nf3] = [
            ("d7d6", 35),  # Najdorf/Dragon prep
            ("b8c6", 30),  # Classical
            ("e7e6", 20),  # French Sicilian
            ("g7g6", 15),  # Hyperaccelerated Dragon
        ]
        
        # Sicilian 2.Nf3 d6 3.d4
        sicilian_d6 = "rnbqkbnr/pp2pppp/3p4/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 0 3"
        self.book[sicilian_d6] = [
            ("d2d4", 90),  # Open lines
            ("f1c4", 10),  # Quieter approach
        ]
        
        # French Defense: 1.e4 e6
        french = "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
        self.book[french] = [
            ("d2d4", 70),  # Main line
            ("d2d3", 15),  # King's Indian Attack
            ("g1f3", 15),  # Flexible
        ]
        
        # French 2.d4 d5
        french_d4 = "rnbqkbnr/pppp1ppp/4p3/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq d3 0 2"
        self.book[french_d4] = [
            ("d7d5", 90),  # Standard
            ("c7c5", 10),  # Franco-Sicilian
        ]
        
        # French 2.d4 d5 3.Nc3/e5
        french_main = "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq d6 0 3"
        self.book[french_main] = [
            ("b1c3", 50),  # Winawer/Classical
            ("e4e5", 30),  # Advance Variation
            ("e4d5", 20),  # Exchange Variation
        ]
        
        # Caro-Kann: 1.e4 c6
        caro = "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
        self.book[caro] = [
            ("d2d4", 75),  # Main line
            ("b1c3", 15),  # Two Knights
            ("g1f3", 10),  # Flexible
        ]
        
        # Caro-Kann 2.d4 d5
        caro_d4 = "rnbqkbnr/pp1ppppp/2p5/8/3PP3/8/PPP2PPP/RNBQKBNR b KQkq d3 0 2"
        self.book[caro_d4] = [
            ("d7d5", 90),  # Standard
            ("g7g6", 10),  # Modern setup
        ]
        
        # Caro-Kann 2.d4 d5 3.Nc3/e5/exd5
        caro_main = "rnbqkbnr/pp2pppp/2p5/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq d6 0 3"
        self.book[caro_main] = [
            ("b1c3", 45),  # Classical
            ("e4e5", 30),  # Advance
            ("e4d5", 25),  # Exchange
        ]
    
    def _add_d4_lines(self):
        """Add lines after 1.d4"""
        
        # 1.d4 responses
        after_d4 = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"
        self.book[after_d4] = [
            ("g8f6", 40),  # Indian Defenses
            ("d7d5", 35),  # Queen's Gambit
            ("e7e6", 15),  # French/QGD prep
            ("g7g6", 10),  # King's Indian/Grunfeld prep
        ]
        
        # 1.d4 Nf6 - White's second move
        after_d4_nf6 = "rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2"
        self.book[after_d4_nf6] = [
            ("c2c4", 50),  # Queen's systems
            ("g1f3", 30),  # Flexible
            ("b1c3", 15),  # London/Jobava
            ("c1f4", 5),   # London System
        ]
        
        # 1.d4 Nf6 2.c4
        after_c4 = "rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 2"
        self.book[after_c4] = [
            ("e7e6", 35),  # Queen's Indian/Nimzo prep
            ("g7g6", 30),  # King's Indian/Grunfeld
            ("e7e5", 20),  # Budapest Gambit
            ("c7c5", 15),  # Benoni systems
        ]
        
        # 1.d4 d5 - White's second move
        after_d4_d5 = "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 2"
        self.book[after_d4_d5] = [
            ("c2c4", 60),  # Queen's Gambit
            ("g1f3", 25),  # Flexible
            ("c1f4", 10),  # London System
            ("e2e3", 5),   # Colle System
        ]
        
        # Queen's Gambit: 1.d4 d5 2.c4
        qg = "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 2"
        self.book[qg] = [
            ("e7e6", 40),  # Queen's Gambit Declined
            ("c7c6", 30),  # Slav Defense
            ("d5c4", 20),  # Queen's Gambit Accepted
            ("g8f6", 10),  # Various defenses
        ]
        
        # QGD: 2...e6
        qgd = "rnbqkbnr/ppp2ppp/4p3/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3"
        self.book[qgd] = [
            ("b1c3", 60),  # Classical
            ("g1f3", 30),  # Flexible
            ("c4d5", 10),  # Exchange Variation
        ]
        
        # Slav: 2...c6
        slav = "rnbqkbnr/pp2pppp/2p5/3p4/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3"
        self.book[slav] = [
            ("g1f3", 50),  # Standard
            ("b1c3", 40),  # Classical
            ("c4d5", 10),  # Exchange
        ]
    
    def _add_nf3_lines(self):
        """Add lines after 1.Nf3"""
        
        # 1.Nf3 responses
        after_nf3 = "rnbqkbnr/pppppppp/8/8/8/5N2/PPPPPPPP/RNBQKB1R b KQkq - 1 1"
        self.book[after_nf3] = [
            ("g8f6", 40),  # Mirror
            ("d7d5", 30),  # Solid center
            ("c7c5", 15),  # Sicilian-like
            ("g7g6", 10),  # King's Indian setup
            ("e7e6", 5),   # French-like
        ]
        
        # 1.Nf3 Nf6 - White's second move
        after_nf3_nf6 = "rnbqkb1r/pppppppp/5n2/8/8/5N2/PPPPPPPP/RNBQKB1R w KQkq - 2 2"
        self.book[after_nf3_nf6] = [
            ("c2c4", 50),  # English/Reti
            ("d2d4", 30),  # Transpose to d4
            ("g2g3", 15),  # King's Indian Attack
            ("b2b3", 5),   # Larsen's Opening
        ]
        
        # 1.Nf3 d5 - White's second move
        after_nf3_d5 = "rnbqkbnr/ppp1pppp/8/3p4/8/5N2/PPPPPPPP/RNBQKB1R w KQkq d6 0 2"
        self.book[after_nf3_d5] = [
            ("d2d4", 50),  # Transpose
            ("c2c4", 30),  # English
            ("g2g3", 20),  # Catalan-like
        ]
    
    def _add_c4_lines(self):
        """Add lines after 1.c4"""
        
        # 1.c4 responses
        after_c4 = "rnbqkbnr/pppppppp/8/8/2P5/8/PP1PPPPP/RNBQKBNR b KQkq c3 0 1"
        self.book[after_c4] = [
            ("g8f6", 35),  # Flexible
            ("e7e5", 30),  # Reversed Sicilian
            ("c7c5", 20),  # Symmetrical
            ("e7e6", 10),  # French-like
            ("g7g6", 5),   # King's Indian
        ]
        
        # 1.c4 e5 - White's second move
        after_c4_e5 = "rnbqkbnr/pppp1ppp/8/4p3/2P5/8/PP1PPPPP/RNBQKBNR w KQkq e6 0 2"
        self.book[after_c4_e5] = [
            ("g1f3", 50),  # Natural development
            ("b1c3", 30),  # Closed English
            ("g2g3", 20),  # Fianchetto
        ]
        
        # 1.c4 Nf6 - White's second move
        after_c4_nf6 = "rnbqkb1r/pppppppp/5n2/8/2P5/8/PP1PPPPP/RNBQKBNR w KQkq - 1 2"
        self.book[after_c4_nf6] = [
            ("g1f3", 50),  # Flexible
            ("b1c3", 30),  # Four Knights
            ("g2g3", 20),  # Fianchetto
        ]
    
    def get_book_move(self, board: chess.Board) -> Optional[str]:
        """
        Get a weighted random book move for the current position.
        
        Args:
            board: Current chess board position
            
        Returns:
            UCI move string or None if position not in book
        """
        fen = board.fen()
        
        if fen not in self.book:
            return None
        
        moves_with_weights = self.book[fen]
        
        # Weighted random selection
        total_weight = sum(weight for _, weight in moves_with_weights)
        
        import random
        rand_val = random.randint(1, total_weight)
        
        cumulative = 0
        for move_uci, weight in moves_with_weights:
            cumulative += weight
            if rand_val <= cumulative:
                # Validate move is legal
                try:
                    move = chess.Move.from_uci(move_uci)
                    if move in board.legal_moves:
                        return move_uci
                except:
                    continue
        
        return None
    
    def is_in_book(self, board: chess.Board) -> bool:
        """Check if position is in opening book."""
        return board.fen() in self.book
    
    def get_all_book_moves(self, board: chess.Board) -> List[str]:
        """Get all book moves for position (for analysis)."""
        fen = board.fen()
        if fen not in self.book:
            return []
        return [move_uci for move_uci, _ in self.book[fen]]
