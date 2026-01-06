# Chess Opening Explorer - GitHub Pages Website

This is an interactive web application that allows users to explore chess openings using real-world statistics from Lichess and computer analysis from Stockfish.

## Features

### 🎮 Interactive Chess Board
- Drag and drop pieces to make moves
- Visual feedback for legal/illegal moves
- Flip board to view from either perspective
- Undo moves and reset to starting position

### 📊 Lichess Opening Statistics
- Real-time data from millions of games on Lichess
- Win/draw/loss statistics for each position
- Popular move suggestions with performance data
- Opening name identification (ECO codes)
- Visual representation of win rates

### 🤖 Stockfish Analysis
- Computer evaluation of positions
- Best move recommendations with multiple variations
- Adjustable analysis depth (1-30 ply)
- Evaluation bar showing position assessment
- Mate detection and notation

### 📝 Move History
- PGN display of the game
- FEN notation of current position
- Full move tracking

## Technologies Used

- **Chess.js** - Chess game logic and move validation
- **Chessboard.js** - Interactive chess board UI
- **Stockfish.js** - Chess engine for position evaluation
- **Lichess Opening Explorer API** - Real game statistics
- **Vanilla JavaScript** - No framework dependencies
- **Modern CSS** - Responsive design with gradients and animations

## Usage

1. **Make Moves**: Click and drag pieces on the board to explore different lines
2. **View Statistics**: Lichess stats update automatically after each move
3. **Analyze Position**: Click "Analyze Position" to get Stockfish's evaluation
4. **Click Suggested Moves**: Click on any popular move in the statistics panel to play it
5. **Adjust Depth**: Increase depth for more thorough but slower analysis

## API Information

### Lichess Opening Explorer API
- Endpoint: `https://explorer.lichess.ovh/lichess`
- Documentation: https://lichess.org/api#tag/opening-explorer
- No authentication required
- Rate limits apply

### Stockfish.js
- Browser-based chess engine
- Runs entirely client-side
- No server required
- Based on Stockfish 10

## Local Development

To test locally:

1. Clone the repository
2. Open `index.html` in a modern web browser
3. Or serve with a local server:
   ```bash
   python -m http.server 8000
   # Then open http://localhost:8000
   ```

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Modern browsers with ES6 support required

## Notes

- The Stockfish engine may take a moment to initialize on first load
- Analysis depth of 15-20 provides good balance of speed and accuracy
- Higher depths (25-30) may take considerable time
- The Lichess API returns data from master-level games by default

## Contributing

Feel free to submit issues or pull requests to improve the application!

## License

This project uses open-source libraries and APIs. Please respect their individual licenses.
