# Lichess Opening-Explorer Client

Small example utilities to query the Lichess Opening Explorer `player` endpoint.

Files:
- `lichess_explorer.py`: a minimal Python client function `query_player_openings`.
- `example.py`: small CLI example that prints top moves.
- `requirements.txt`: runtime dependency.

Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the example:

```bash
python example.py --nb 10
```

If you have a Lichess OAuth token (optional), export it to increase rate limits:

```bash
export LICHESS_TOKEN=your_token_here
python example.py --nb 10
```

Notes
- The client uses `requests` and returns a parsed JSON dict from the API.
- Parameters map directly to the documented query parameters; see `lichess_explorer.py` for details.

API reference
- https://lichess.org/api#tag/opening-explorer
# chess_openings