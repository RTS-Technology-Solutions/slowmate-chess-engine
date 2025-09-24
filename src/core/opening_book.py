"""
SlowMate Chess Engine v3.2 - Advanced Opening Book System
Enhanced opening preparation designed to outplay V7P3R in opening phase.
Focus on rapid development, center control, and tactical awareness.
"""
import os
import json
import random
import chess
from typing import Optional, List, Dict, Tuple
from collections import defaultdict


class AdvancedOpeningBook:
    """Enhanced opening book with strategic repertoire and opponent adaptation."""
    
    def __init__(self, book_path: Optional[str] = None):
        self.book_path = book_path or os.path.join(os.path.dirname(__file__), '../../data/openings/opening_book.json')
        self.book = self._load_book()
        self.game_history = defaultdict(list)  # Track opponent patterns
        self.repertoire = self._build_strategic_repertoire()
        self.opening_principles = self._define_opening_principles()
        
    def _load_book(self) -> dict:
        """Load existing book or create enhanced default."""
        if os.path.exists(self.book_path):
            with open(self.book_path, 'r') as f:
                return json.load(f)
        return self._create_enhanced_book()
    
    def _create_enhanced_book(self) -> dict:
        """Create comprehensive opening book focused on beating V7P3R."""
        book = {}
        
        # Starting position - aggressive repertoire
        start_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        book[start_fen] = [
            {"move": "e4", "weight": 40, "style": "aggressive", "note": "King's pawn - central control"},
            {"move": "d4", "weight": 35, "style": "positional", "note": "Queen's pawn - solid development"},
            {"move": "Nf3", "weight": 20, "style": "flexible", "note": "Reti system - flexible development"},
            {"move": "c4", "weight": 5, "style": "positional", "note": "English - flank opening"}
        ]
        
        # After 1.e4 - focus on open games
        after_e4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        book[after_e4] = [
            {"move": "e5", "weight": 35, "style": "classical", "note": "Italian/Spanish prep"},
            {"move": "c5", "weight": 30, "style": "sharp", "note": "Sicilian - tactical complications"},
            {"move": "e6", "weight": 20, "style": "solid", "note": "French - solid structure"},
            {"move": "c6", "weight": 15, "style": "solid", "note": "Caro-Kann - reliable defense"}
        ]
        
        # Italian Game preparation (anti-V7P3R weapon)
        italian_setup = "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
        book[italian_setup] = [
            {"move": "Be7", "weight": 30, "style": "solid", "note": "Hungarian defense"},
            {"move": "f5", "weight": 25, "style": "aggressive", "note": "Rousseau gambit"},
            {"move": "Bc5", "weight": 25, "style": "active", "note": "Italian game main line"},
            {"move": "Nf6", "weight": 20, "style": "natural", "note": "Develop with tempo"}
        ]
        
        # Spanish Opening (Ruy Lopez) - pressure on e5
        spanish_setup = "r1bqkbnr/pppp1ppp/2n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"
        book[spanish_setup] = [
            {"move": "a6", "weight": 40, "style": "main", "note": "Morphy defense - main line"},
            {"move": "Nf6", "weight": 30, "style": "active", "note": "Berlin defense - solid"},
            {"move": "Be7", "weight": 20, "style": "solid", "note": "Steinitz defense"},
            {"move": "f5", "weight": 10, "style": "aggressive", "note": "Schliemann defense"}
        ]
        
        return book
    
    def _build_strategic_repertoire(self) -> Dict[str, Dict]:
        """Build strategic opening repertoire based on game phase and opponent."""
        return {
            'aggressive': {
                'white': ['e4', 'Italian', 'Spanish', 'Kings_Gambit'],
                'black': ['Sicilian_Dragon', 'Kings_Indian', 'Alekhine'],
                'philosophy': 'Sharp tactical play, initiative seeking'
            },
            'positional': {
                'white': ['d4', 'Queens_Gambit', 'English', 'Catalan'],
                'black': ['Queens_Gambit_Declined', 'Nimzo_Indian', 'French'],
                'philosophy': 'Solid structure, long-term advantages'
            },
            'anti_computer': {
                'white': ['Nf3', 'Kings_Indian_Attack', 'English'],
                'black': ['Caro_Kann', 'French', 'Petrov'],
                'philosophy': 'Reduce tactical complications, positional play'
            }
        }
    
    def _define_opening_principles(self) -> Dict[str, int]:
        """Define opening principles with evaluation bonuses."""
        return {
            'center_control': 25,      # Bonus for e4, d4, e5, d5
            'piece_development': 15,   # Bonus for developing pieces
            'king_safety': 30,         # Bonus for castling preparation
            'tempo_gain': 20,          # Bonus for moves with tempo
            'opponent_weakness': 35,   # Exploit opponent weaknesses
            'tactical_awareness': 25   # Bonus for tactical possibilities
        }
    
    def select_strategic_move(self, board: chess.Board, opponent_id: str = "V7P3R") -> Optional[str]:
        """Select opening move based on strategic considerations."""
        fen = board.fen()
        
        # Check if position is in enhanced book
        if fen in self.book:
            moves_data = self.book[fen]
            
            # Handle both old format (list of strings) and new format (list of dicts)
            if isinstance(moves_data, list):
                if len(moves_data) > 0:
                    if isinstance(moves_data[0], str):
                        # Old format - just return random move
                        return random.choice(moves_data)
                    elif isinstance(moves_data[0], dict):
                        # New format - use strategic selection
                        opponent_style = self._analyze_opponent_style(opponent_id)
                        best_move = self._select_by_strategy(moves_data, opponent_style, board)
                        if best_move:
                            return best_move['move']
        
        # Fallback to principle-based move selection
        return self._select_by_principles(board)
    
    def _analyze_opponent_style(self, opponent_id: str) -> str:
        """Analyze opponent's playing style based on game history."""
        if "V7P3R" in opponent_id:
            # V7P3R analysis from game records
            return "tactical_aggressive"
        elif "C0BR4" in opponent_id:
            return "positional_solid"
        elif "Stockfish" in opponent_id:
            return "engine_perfect"
        else:
            return "unknown"
    
    def _select_by_strategy(self, moves_data: List[Dict], opponent_style: str, board: chess.Board) -> Optional[Dict]:
        """Select move based on strategic considerations against opponent."""
        # Weight adjustments based on opponent
        style_preferences = {
            'tactical_aggressive': {'positional': 1.5, 'solid': 1.3, 'aggressive': 0.8},
            'positional_solid': {'aggressive': 1.4, 'sharp': 1.2, 'positional': 0.9},
            'engine_perfect': {'anti_computer': 1.6, 'positional': 1.2, 'tactical': 0.7}
        }
        
        # Adjust weights based on opponent
        adjusted_moves = []
        for move_data in moves_data:
            weight = move_data['weight']
            style = move_data.get('style', 'neutral')
            
            if opponent_style in style_preferences:
                multiplier = style_preferences[opponent_style].get(style, 1.0)
                weight = int(weight * multiplier)
            
            adjusted_moves.append({**move_data, 'adjusted_weight': weight})
        
        # Select based on weighted random choice
        total_weight = sum(move['adjusted_weight'] for move in adjusted_moves)
        if total_weight == 0:
            return random.choice(adjusted_moves) if adjusted_moves else None
        
        # Weighted random selection with slight preference for higher weights
        choice = random.randint(1, total_weight)
        current_weight = 0
        
        for move_data in adjusted_moves:
            current_weight += move_data['adjusted_weight']
            if choice <= current_weight:
                return move_data
        
        return adjusted_moves[-1] if adjusted_moves else None
    
    def _select_by_principles(self, board: chess.Board) -> Optional[str]:
        """Select move based on opening principles when not in book."""
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        move_scores = []
        
        for move in legal_moves:
            score = 0
            
            # Center control bonus
            if move.to_square in [chess.E4, chess.D4, chess.E5, chess.D5]:
                score += self.opening_principles['center_control']
            
            # Development bonus
            piece = board.piece_at(move.from_square)
            if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                if piece.color == chess.WHITE and move.from_square < 16:  # Back rank
                    score += self.opening_principles['piece_development']
                elif piece.color == chess.BLACK and move.from_square >= 48:  # Back rank
                    score += self.opening_principles['piece_development']
            
            # Castling preparation
            if piece and piece.piece_type == chess.KING and abs(move.from_square - move.to_square) == 2:
                score += self.opening_principles['king_safety']
            
            # Tempo moves (checks, attacks)
            board.push(move)
            if board.is_check():
                score += self.opening_principles['tempo_gain']
            board.pop()
            
            move_scores.append((move, score))
        
        # Select best scoring move with some randomness
        move_scores.sort(key=lambda x: x[1], reverse=True)
        best_score = move_scores[0][1]
        
        # Select from top 3 moves to add variety
        top_moves = [move for move, score in move_scores[:3] if score >= best_score - 10]
        return random.choice(top_moves).uci() if top_moves else legal_moves[0].uci()
    
    def update_opponent_history(self, opponent_id: str, moves: List[str], result: str):
        """Update opponent move history for future analysis."""
        self.game_history[opponent_id].append({
            'moves': moves,
            'result': result,
            'opening_length': min(len(moves), 20)  # Track first 20 moves
        })
        
        # Keep only recent games (last 50)
        if len(self.game_history[opponent_id]) > 50:
            self.game_history[opponent_id] = self.game_history[opponent_id][-50:]
    
    # Legacy compatibility methods
    def get_book_moves(self, fen: str) -> List[str]:
        """Legacy compatibility - return list of move strings."""
        if fen in self.book:
            moves_data = self.book[fen]
            if isinstance(moves_data, list):
                if len(moves_data) > 0:
                    if isinstance(moves_data[0], str):
                        return moves_data
                    elif isinstance(moves_data[0], dict):
                        return [move_data['move'] for move_data in moves_data]
        return []

    def select_book_move(self, fen: str) -> Optional[str]:
        """Legacy compatibility - select random book move."""
        moves = self.get_book_moves(fen)
        return random.choice(moves) if moves else None

    def in_book(self, fen: str) -> bool:
        """Legacy compatibility - check if position is in book."""
        return fen in self.book


# Backward compatibility alias
OpeningBook = AdvancedOpeningBook
