"""
Chess Position Evaluator using Stockfish Engine
Requires: python-chess and stockfish engine installed
"""

import chess
import chess.engine
from typing import Optional, Dict, Any, List
from pathlib import Path


class ChessEngineEvaluator:
    """Evaluate chess positions using Stockfish engine."""
    
    def __init__(self, engine_path: Optional[str] = None, depth: int = 20):
        """
        Initialize the chess engine evaluator.
        
        Args:
            engine_path: Path to the Stockfish executable (None for auto-detection)
            depth: Default analysis depth (default: 20)
        """
        self.depth = depth
        
        # Try to find Stockfish if path not provided
        if engine_path is None:
            engine_path = self._find_stockfish()
        
        self.engine_path = engine_path
        self.engine = None
    
    def _find_stockfish(self) -> str:
        """
        Try to find Stockfish in common locations.
        
        Returns:
            Path to Stockfish executable
        
        Raises:
            FileNotFoundError: If Stockfish cannot be found
        """
        # Common paths where Stockfish might be installed
        possible_paths = [
            '/usr/games/stockfish',
            '/usr/local/bin/stockfish',
            '/usr/bin/stockfish',
            '/opt/homebrew/bin/stockfish',
            'stockfish',  # If in PATH
            './stockfish',
        ]
        
        for path in possible_paths:
            if Path(path).exists() or path == 'stockfish':
                return path
        
        raise FileNotFoundError(
            "Stockfish not found. Please install it or provide the path explicitly.\n"
            "Install with: sudo apt-get install stockfish (Linux) or brew install stockfish (Mac)"
        )
    
    def __enter__(self):
        """Context manager entry - start the engine."""
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close the engine."""
        if self.engine:
            self.engine.quit()
    
    def evaluate_position(
        self,
        fen: str,
        depth: Optional[int] = None,
        time_limit: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Evaluate a chess position.
        
        Args:
            fen: FEN string of the position to evaluate
            depth: Analysis depth (uses default if None)
            time_limit: Time limit in seconds (alternative to depth)
        
        Returns:
            Dictionary containing:
                - score: Centipawn score (from white's perspective)
                - mate: Mate in N moves (if applicable)
                - best_move: Best move in UCI notation
                - pv: Principal variation (best line)
                - evaluation_text: Human-readable evaluation
        """
        if not self.engine:
            raise RuntimeError("Engine not started. Use 'with' statement or call start_engine()")
        
        board = chess.Board(fen)
        
        # Set analysis limit
        if time_limit:
            limit = chess.engine.Limit(time=time_limit)
        else:
            limit = chess.engine.Limit(depth=depth or self.depth)
        
        # Analyze the position
        info = self.engine.analyse(board, limit)
        
        # Extract score
        score = info.get('score')
        result = {
            'fen': fen,
            'depth': info.get('depth'),
        }
        
        if score:
            # Convert score to white's perspective
            if board.turn == chess.BLACK:
                score = -score.white()
            else:
                score = score.white()
            
            if score.is_mate():
                mate_in = score.mate()
                result['mate'] = mate_in
                result['score'] = None
                result['evaluation_text'] = f"Mate in {abs(mate_in)}" + (" for white" if mate_in > 0 else " for black")
            else:
                cp_score = score.score()
                result['score'] = cp_score
                result['mate'] = None
                result['evaluation_text'] = self._format_evaluation(cp_score)
        
        # Best move and principal variation
        if 'pv' in info and info['pv']:
            result['best_move'] = info['pv'][0].uci()
            result['pv'] = [move.uci() for move in info['pv']]
            
            # Convert PV to SAN notation using a copy of the board
            pv_san = []
            board_copy = board.copy()
            for move in info['pv'][:10]:  # First 10 moves in SAN
                try:
                    pv_san.append(board_copy.san(move))
                    board_copy.push(move)
                except (ValueError, AssertionError):
                    break
            result['pv_san'] = pv_san
        
        return result
    
    def evaluate_moves_sequence(
        self,
        moves: List[str],
        starting_fen: Optional[str] = None,
        depth: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluate each position in a sequence of moves.
        
        Args:
            moves: List of moves in UCI notation
            starting_fen: Starting position (None for standard starting position)
            depth: Analysis depth (uses default if None)
        
        Returns:
            List of evaluation dictionaries for each position
        """
        board = chess.Board(starting_fen) if starting_fen else chess.Board()
        evaluations = []
        
        # Evaluate starting position
        evaluations.append(self.evaluate_position(board.fen(), depth=depth))
        
        # Evaluate after each move
        for move_uci in moves:
            try:
                move = chess.Move.from_uci(move_uci)
                if move not in board.legal_moves:
                    raise ValueError(f"Illegal move: {move_uci}")
                board.push(move)
                evaluations.append(self.evaluate_position(board.fen(), depth=depth))
            except ValueError as e:
                print(f"Error processing move {move_uci}: {e}")
                break
        
        return evaluations
    
    def find_best_move(
        self,
        fen: str,
        depth: Optional[int] = None,
        time_limit: Optional[float] = None
    ) -> str:
        """
        Find the best move for a position.
        
        Args:
            fen: FEN string of the position
            depth: Analysis depth (uses default if None)
            time_limit: Time limit in seconds (alternative to depth)
        
        Returns:
            Best move in UCI notation
        """
        evaluation = self.evaluate_position(fen, depth=depth, time_limit=time_limit)
        return evaluation.get('best_move')
    
    def compare_moves(
        self,
        fen: str,
        moves: List[str],
        depth: Optional[int] = None
    ) -> Dict[str, Dict[str, Any]]:
        """
        Compare multiple candidate moves from the same position.
        
        Args:
            fen: FEN string of the position
            moves: List of moves in UCI notation to compare
            depth: Analysis depth (uses default if None)
        
        Returns:
            Dictionary mapping each move to its evaluation
        """
        board = chess.Board(fen)
        results = {}
        
        for move_uci in moves:
            try:
                move = chess.Move.from_uci(move_uci)
                if move not in board.legal_moves:
                    results[move_uci] = {'error': 'Illegal move'}
                    continue
                
                # Make the move and evaluate
                board.push(move)
                evaluation = self.evaluate_position(board.fen(), depth=depth)
                
                # Flip score since we're evaluating from opponent's perspective
                if evaluation.get('score') is not None:
                    evaluation['score'] = -evaluation['score']
                if evaluation.get('mate') is not None:
                    evaluation['mate'] = -evaluation['mate']
                
                results[move_uci] = evaluation
                board.pop()
                
            except ValueError as e:
                results[move_uci] = {'error': str(e)}
        
        return results
    
    @staticmethod
    def _format_evaluation(centipawns: int) -> str:
        """
        Format centipawn score as human-readable text.
        
        Args:
            centipawns: Score in centipawns
        
        Returns:
            Formatted evaluation string
        """
        pawns = centipawns / 100
        
        if abs(pawns) < 0.5:
            return "Equal position"
        elif abs(pawns) < 1.5:
            side = "white" if pawns > 0 else "black"
            return f"Slight advantage for {side} ({pawns:+.2f})"
        elif abs(pawns) < 3.0:
            side = "white" if pawns > 0 else "black"
            return f"Clear advantage for {side} ({pawns:+.2f})"
        else:
            side = "white" if pawns > 0 else "black"
            return f"Winning for {side} ({pawns:+.2f})"


def main():
    """Example usage of the Chess Engine Evaluator."""
    
    # Use context manager to ensure engine is properly closed
    with ChessEngineEvaluator(depth=15) as evaluator:
        
        # Example 1: Evaluate starting position
        print("=== Starting Position ===")
        result = evaluator.evaluate_position(chess.STARTING_FEN)
        print(f"Evaluation: {result['evaluation_text']}")
        print(f"Score: {result.get('score', 'N/A')} centipawns")
        print(f"Best move: {result.get('best_move')}")
        print(f"Principal variation: {' '.join(result.get('pv_san', [])[:5])}")
        
        # Example 2: Evaluate after 1.e4 e5 2.Nf3
        print("\n=== After 1.e4 e5 2.Nf3 ===")
        board = chess.Board()
        for move in ['e2e4', 'e7e5', 'g1f3']:
            board.push(chess.Move.from_uci(move))
        
        result = evaluator.evaluate_position(board.fen())
        print(f"Evaluation: {result['evaluation_text']}")
        print(f"Score: {result.get('score', 'N/A')} centipawns")
        print(f"Best move: {result.get('best_move')}")
        
        # Example 3: Evaluate a tactical position (Scholar's Mate setup)
        print("\n=== Tactical Position (Scholar's Mate Threat) ===")
        fen = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4"
        result = evaluator.evaluate_position(fen)
        print(f"Evaluation: {result['evaluation_text']}")
        print(f"Best move: {result.get('best_move')}")
        print(f"Principal variation: {' '.join(result.get('pv_san', [])[:5])}")
        
        # Example 4: Compare multiple candidate moves
        print("\n=== Comparing Candidate Moves ===")
        starting_fen = chess.STARTING_FEN
        candidate_moves = ['e2e4', 'd2d4', 'g1f3', 'c2c4']
        comparisons = evaluator.compare_moves(starting_fen, candidate_moves, depth=12)
        
        for move, eval_result in sorted(
            comparisons.items(),
            key=lambda x: x[1].get('score', -9999),
            reverse=True
        ):
            score = eval_result.get('score')
            if score is not None:
                print(f"{move}: {score/100:+.2f} pawns - {eval_result.get('evaluation_text')}")
            else:
                print(f"{move}: {eval_result}")
        
        # Example 5: Evaluate a sequence of moves
        print("\n=== Evaluating Move Sequence ===")
        moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6', 'f1c4']
        evaluations = evaluator.evaluate_moves_sequence(moves, depth=12)
        
        board = chess.Board()
        print(f"0. Starting position: {evaluations[0].get('score', 0)/100:+.2f}")
        
        for i, move_uci in enumerate(moves):
            move = chess.Move.from_uci(move_uci)
            san_move = board.san(move)
            board.push(move)
            eval_score = evaluations[i+1].get('score', 0) / 100
            print(f"{i+1}. {san_move}: {eval_score:+.2f}")


if __name__ == "__main__":
    main()
