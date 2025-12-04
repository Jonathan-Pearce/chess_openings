# Chess Position Evaluation with Stockfish

This guide explains how to set up and use the chess engine evaluator.

## Setup Steps

### 1. Install Stockfish Engine

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install stockfish
```

**macOS:**
```bash
brew install stockfish
```

**Windows:**
- Download from https://stockfishchess.org/download/
- Extract and note the path to `stockfish.exe`

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `python-chess`: Chess library for move generation, validation, and board representation
- `requests`: For the Lichess API client

### 3. Verify Installation

Check that Stockfish is accessible:
```bash
which stockfish  # Linux/Mac
stockfish        # Should start the engine (type 'quit' to exit)
```

## Usage

### Basic Example

```python
from chess_engine_evaluator import ChessEngineEvaluator
import chess

# Use context manager to ensure proper cleanup
with ChessEngineEvaluator(depth=15) as evaluator:
    # Evaluate starting position
    result = evaluator.evaluate_position(chess.STARTING_FEN)
    print(f"Evaluation: {result['evaluation_text']}")
    print(f"Best move: {result['best_move']}")
```

### Advanced Examples

**Evaluate a specific position:**
```python
with ChessEngineEvaluator() as evaluator:
    fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 4 4"
    result = evaluator.evaluate_position(fen, depth=20)
    print(f"Score: {result['score']} centipawns")
    print(f"Best move: {result['best_move']}")
    print(f"Principal variation: {result['pv_san']}")
```

**Compare multiple candidate moves:**
```python
with ChessEngineEvaluator() as evaluator:
    fen = chess.STARTING_FEN
    moves = ['e2e4', 'd2d4', 'g1f3', 'c2c4']
    comparisons = evaluator.compare_moves(fen, moves, depth=15)
    
    for move, evaluation in comparisons.items():
        print(f"{move}: {evaluation['score']/100:+.2f} pawns")
```

**Evaluate a sequence of moves:**
```python
with ChessEngineEvaluator() as evaluator:
    moves = ['e2e4', 'e7e5', 'g1f3', 'b8c6']
    evaluations = evaluator.evaluate_moves_sequence(moves, depth=15)
    
    for i, eval_result in enumerate(evaluations):
        print(f"After move {i}: {eval_result['evaluation_text']}")
```

### Custom Stockfish Path

If Stockfish is not in a standard location:
```python
with ChessEngineEvaluator(engine_path='/custom/path/to/stockfish') as evaluator:
    result = evaluator.evaluate_position(chess.STARTING_FEN)
```

## Key Methods

- **`evaluate_position(fen, depth, time_limit)`**: Evaluate a single position
- **`find_best_move(fen, depth, time_limit)`**: Get the best move for a position
- **`compare_moves(fen, moves, depth)`**: Compare multiple candidate moves
- **`evaluate_moves_sequence(moves, starting_fen, depth)`**: Evaluate a game sequence

## Understanding the Output

- **Score**: Centipawn advantage (100 = 1 pawn advantage for white, negative = black advantage)
- **Mate**: Mate in N moves (positive = white mates, negative = black mates)
- **Best move**: Recommended move in UCI notation (e.g., "e2e4")
- **PV (Principal Variation)**: Best continuation from the position
- **Evaluation text**: Human-readable description of the position

## Running the Examples

```bash
python chess_engine_evaluator.py
```

This will run all example evaluations and display the results.
