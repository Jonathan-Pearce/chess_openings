"""Simple Lichess Opening-Explorer client for the `player` endpoint.

Usage:
    from lichess_explorer import query_player_openings

    resp = query_player_openings('magnuscarlsen', nb=10)
    print(resp)

This module wraps the Lichess opening-explorer player endpoint documented at
https://lichess.org/api#tag/opening-explorer/get/player
"""
from typing import Optional, List, Dict, Any
import requests


API_URL_PLAYER = "https://lichess.org/api/opening-explorer/player"
API_URL_LICHESS = "https://lichess.org/api/opening-explorer/lichess"


def _normalize_moves(moves: Optional[List[str] | str]) -> Optional[str]:
    if moves is None:
        return None
    if isinstance(moves, str):
        return moves
    return ",".join(moves)


def query_player_openings(
    username: str,
    moves: Optional[List[str] | str] = None,
    nb: Optional[int] = None,
    play_as: Optional[str] = None,  # 'white' | 'black' | 'both'
    speeds: Optional[List[str] | str] = None,
    since: Optional[int] = None,
    until: Optional[int] = None,
    variant: Optional[str] = None,
    token: Optional[str] = None,
    timeout: int = 10,
) -> Dict[str, Any]:
    """Query the Lichess opening-explorer `/player` endpoint.

    Parameters map to the endpoint query parameters. All parameters are optional
    except `username`.

    - `moves`: list or comma-separated string of SAN moves (e.g. 'e4,e5,Nf3')
    - `nb`: number of top moves to return
    - `play_as`: 'white', 'black' or 'both'
    - `speeds`: list or comma-separated string of speeds like 'blitz,rapid'
    - `since` / `until`: timestamps in milliseconds since epoch
    - `variant`: chess variant (e.g. 'standard')
    - `token`: optional Lichess OAuth token (Bearer) if you want higher rate limits

    Returns the parsed JSON response as a Python dict. Raises requests.HTTPError
    on HTTP errors.
    """

    params: Dict[str, str] = {"username": username}
    m = _normalize_moves(moves)
    if m:
        params["moves"] = m
    if nb is not None:
        params["nb"] = str(nb)
    if play_as:
        params["playAs"] = play_as
    if speeds:
        params["speeds"] = _normalize_moves(speeds)
    if since is not None:
        params["since"] = str(since)
    if until is not None:
        params["until"] = str(until)
    if variant:
        params["variant"] = variant

    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(API_URL_PLAYER, params=params, headers=headers, timeout=timeout)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        # Try to include response body for easier debugging
        body = resp.text
        raise requests.HTTPError(f"{resp.status_code} {resp.reason}: {body}")

    return resp.json()


def query_lichess_openings(
    moves: Optional[List[str] | str] = None,
    nb: Optional[int] = None,
    play_as: Optional[str] = None,  # 'white' | 'black' | 'both'
    speeds: Optional[List[str] | str] = None,
    since: Optional[int] = None,
    until: Optional[int] = None,
    variant: Optional[str] = None,
    token: Optional[str] = None,
    timeout: int = 10,
) -> Dict[str, Any]:
    """Query the Lichess opening-explorer `/lichess` endpoint.

    This is the general opening explorer across Lichess games (no username).
    Parameters map to the endpoint query parameters.
    """

    params: Dict[str, str] = {}
    m = _normalize_moves(moves)
    if m:
        params["moves"] = m
    if nb is not None:
        params["nb"] = str(nb)
    if play_as:
        params["playAs"] = play_as
    if speeds:
        params["speeds"] = _normalize_moves(speeds)
    if since is not None:
        params["since"] = str(since)
    if until is not None:
        params["until"] = str(until)
    if variant:
        params["variant"] = variant

    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(API_URL_LICHESS, params=params, headers=headers, timeout=timeout)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        body = resp.text
        raise requests.HTTPError(f"{resp.status_code} {resp.reason}: {body}")

    return resp.json()


if __name__ == "__main__":
    # Simple manual demo when run directly
    import os
    import argparse

    parser = argparse.ArgumentParser(description="Query Lichess opening-explorer player")
    parser.add_argument("username", help="Lichess username to query")
    parser.add_argument("--nb", type=int, help="Number of moves to return")
    parser.add_argument("--moves", help="Comma-separated SAN moves or quoted list")
    parser.add_argument("--play-as", choices=["white", "black", "both"], help="Which side to play as")
    parser.add_argument("--token", help="Lichess OAuth token (optional). Can also be set via LICHESS_TOKEN env var")
    args = parser.parse_args()

    token = args.token or os.environ.get("LICHESS_TOKEN")
    result = query_player_openings(
        args.username, moves=args.moves, nb=args.nb, play_as=args.play_as, token=token
    )
    import json

    print(json.dumps(result, indent=2))
