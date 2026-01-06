# Chess Opening Explorer

An interactive chess opening explorer with Python API clients and a web-based interface.

## 🌐 Live Web Application

Try the interactive web application: [Chess Opening Explorer](https://jonathan-pearce.github.io/chess_openings/)

The web interface provides:
- Interactive chess board with drag-and-drop moves
- Real-time Lichess opening statistics from millions of games
- Stockfish chess engine analysis with best move recommendations
- Opening name identification and ECO codes
- Visual win/draw/loss statistics

See [WEBSITE.md](WEBSITE.md) for more details about the web application.

## 🐍 Python API Clients

Small example utilities to query the Lichess Opening Explorer API from Python.

Files:
- `lichess_opening_explorer.py`: Python client for the Lichess Opening Explorer API
- `chess_engine_evaluator.py`: Chess position evaluator using Stockfish engine
- `requirements.txt`: runtime dependencies

### Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Install Stockfish (for chess engine analysis):

```bash
./install_stockfish.sh
```

3. Use the Python clients:

```python
from lichess_opening_explorer import LichessOpeningExplorer

# Query opening statistics
explorer = LichessOpeningExplorer()
data = explorer.query(play="e2e4,e7e5")
print(f"Total games: {data['white'] + data['draws'] + data['black']}")
```

### API References
- Lichess Opening Explorer: https://lichess.org/api#tag/opening-explorer
- Python Chess: https://python-chess.readthedocs.io/

## 🚀 GitHub Pages Deployment

The web application is deployed using GitHub Pages. To update:

1. Make changes to `index.html`, `styles.css`, or `app.js`
2. Commit and push to the `main` branch
3. GitHub Actions will automatically deploy the changes

## 📁 Repository Structure

```
.
├── index.html                    # Main web application
├── app.js                        # JavaScript logic for web app
├── styles.css                    # Styling for web app
├── WEBSITE.md                    # Web application documentation
├── lichess_opening_explorer.py   # Python Lichess API client
├── chess_engine_evaluator.py     # Python Stockfish wrapper
├── requirements.txt              # Python dependencies
├── install_stockfish.sh          # Stockfish installation script
└── README.md                     # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs or request features via Issues
- Submit pull requests with improvements
- Share feedback on the web application

## 📄 License

Open source project using public APIs and open-source chess libraries.