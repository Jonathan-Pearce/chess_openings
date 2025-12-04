"""
Query the Lichess Opening Explorer API
API Documentation: https://lichess.org/api#tag/opening-explorer/get/lichess
"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urlencode


class LichessOpeningExplorer:
    """Client for querying the Lichess Opening Explorer API."""
    
    BASE_URL = "https://explorer.lichess.ovh/lichess"
    
    def __init__(self):
        """Initialize the Lichess Opening Explorer client."""
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json'
        })
    
    def query(
        self,
        fen: Optional[str] = None,
        play: Optional[str] = None,
        variant: str = "standard",
        speeds: Optional[list] = None,
        ratings: Optional[list] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        moves: int = 12,
        top_games: int = 15,
        recent_games: int = 8,
        history: bool = False
    ) -> Dict[str, Any]:
        """
        Query the Lichess opening explorer database.
        
        Args:
            fen: FEN of the position to explore (default: starting position)
            play: Comma-separated sequence of legal moves in UCI notation (alternative to fen)
            variant: Variant (standard, crazyhouse, chess960, etc.)
            speeds: List of game speeds to filter (ultraBullet, bullet, blitz, rapid, classical, correspondence)
            ratings: List of rating groups (0, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2500)
            since: Include only games from this month (YYYY-MM format)
            until: Include only games until this month (YYYY-MM format)
            moves: Number of most common moves to display (default: 12)
            top_games: Number of top games to display (default: 15, max: 15)
            recent_games: Number of recent games to display (default: 8, max: 8)
            history: Include position popularity history (default: False)
        
        Returns:
            Dictionary containing the API response with opening statistics
        """
        params = {
            'variant': variant,
            'moves': moves,
            'topGames': top_games,
            'recentGames': recent_games
        }
        
        if fen:
            params['fen'] = fen
        if play:
            params['play'] = play
        if speeds:
            params['speeds'] = ','.join(speeds)
        if ratings:
            params['ratings'] = ','.join(map(str, ratings))
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        if history:
            params['history'] = 'true'
        
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        return response.json()
    
    def get_position_stats(self, fen: str, **kwargs) -> Dict[str, Any]:
        """
        Get statistics for a specific position.
        
        Args:
            fen: FEN string of the position
            **kwargs: Additional parameters to pass to query()
        
        Returns:
            Dictionary containing position statistics
        """
        return self.query(fen=fen, **kwargs)
    
    def get_moves_sequence_stats(self, moves: str, **kwargs) -> Dict[str, Any]:
        """
        Get statistics for a sequence of moves.
        
        Args:
            moves: Comma-separated sequence of legal moves in UCI notation (e.g., "e2e4,e7e5")
            **kwargs: Additional parameters to pass to query()
        
        Returns:
            Dictionary containing position statistics
        """
        return self.query(play=moves, **kwargs)


def main():
    """Example usage of the Lichess Opening Explorer API."""
    explorer = LichessOpeningExplorer()
    
    # Example 1: Query the starting position
    print("=== Starting Position ===")
    result = explorer.query()
    print(f"Total games: {result.get('white', 0) + result.get('draws', 0) + result.get('black', 0)}")
    print(f"White wins: {result.get('white', 0)}")
    print(f"Draws: {result.get('draws', 0)}")
    print(f"Black wins: {result.get('black', 0)}")
    print("\nMost popular moves:")
    for move in result.get('moves', [])[:5]:
        print(f"  {move['uci']} ({move['san']}): {move.get('white', 0) + move.get('draws', 0) + move.get('black', 0)} games")
    
    # Example 2: Query after 1.e4
    print("\n=== After 1.e4 ===")
    result = explorer.get_moves_sequence_stats("e2e4")
    print(f"Total games: {result.get('white', 0) + result.get('draws', 0) + result.get('black', 0)}")
    print("\nMost popular replies:")
    for move in result.get('moves', [])[:5]:
        print(f"  {move['uci']} ({move['san']}): {move.get('white', 0) + move.get('draws', 0) + move.get('black', 0)} games")
    
    # Example 3: Query with filters (blitz games, ratings 2000+)
    print("\n=== Starting Position (Blitz, 2000+ rating) ===")
    result = explorer.query(speeds=['blitz'], ratings=[2000, 2200, 2500])
    print(f"Total games: {result.get('white', 0) + result.get('draws', 0) + result.get('black', 0)}")
    print("\nMost popular moves:")
    for move in result.get('moves', [])[:5]:
        print(f"  {move['uci']} ({move['san']}): {move.get('white', 0) + move.get('draws', 0) + move.get('black', 0)} games")


if __name__ == "__main__":
    main()
