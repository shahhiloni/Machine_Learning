"""
recommender.py - Core recommendation engine.

Loads precomputed top-N neighbor data (lightweight) and provides
movie search + recommendation functionality.
"""

import logging
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd

# ── Logging ─────────────────────────────────────────────────────────
logger = logging.getLogger(__name__)

# ── Path Configuration ──────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent.parent
MODEL_DIR: Path = BASE_DIR / "model"
MOVIES_PKL: Path = MODEL_DIR / "movies.pkl"
NEIGHBORS_PKL: Path = MODEL_DIR / "neighbors.pkl"


class MovieRecommender:
    """
    Content-based movie recommendation engine.

    Uses precomputed top-N neighbor dict for instant lookups
    instead of loading the full similarity matrix.
    """

    def __init__(self) -> None:
        """Initialize the recommender."""
        self._movies: Optional[pd.DataFrame] = None
        self._neighbors: Optional[dict] = None
        self._is_loaded: bool = False
        self._title_cache: Optional[list[str]] = None

    def load_model(self) -> bool:
        """
        Load the precomputed model artifacts from disk.

        Returns:
            True if model loaded successfully, False otherwise.
        """
        try:
            if not MOVIES_PKL.exists() or not NEIGHBORS_PKL.exists():
                logger.error(
                    "Model files not found. Please run build_model.py first."
                )
                return False

            logger.info("Loading model artifacts...")
            self._movies = joblib.load(MOVIES_PKL)
            self._neighbors = joblib.load(NEIGHBORS_PKL)
            self._is_loaded = True

            # Pre-cache sorted titles for autocomplete
            self._title_cache = sorted(self._movies["title"].tolist())

            logger.info(
                f"Model loaded: {len(self._movies)} movies available."
            )
            return True

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False

    @property
    def is_loaded(self) -> bool:
        """Check if the model is loaded."""
        return self._is_loaded

    def get_movie_titles(self) -> list[str]:
        """Get all available movie titles for autocomplete."""
        if not self._is_loaded or self._title_cache is None:
            return []
        return self._title_cache

    def search_movies(self, query: str, limit: int = 10) -> list[str]:
        """
        Search for movies matching a query string.

        Args:
            query: Search query string.
            limit: Maximum number of results to return.

        Returns:
            List of matching movie titles.
        """
        if not self._is_loaded or self._movies is None:
            return []

        query_lower = query.lower().strip()
        if not query_lower:
            return []

        titles = self._movies["title"].tolist()

        # Exact match first, then starts-with, then contains
        exact: list[str] = []
        starts_with: list[str] = []
        contains: list[str] = []

        for title in titles:
            title_lower = title.lower()
            if title_lower == query_lower:
                exact.append(title)
            elif title_lower.startswith(query_lower):
                starts_with.append(title)
            elif query_lower in title_lower:
                contains.append(title)

        results = exact + sorted(starts_with) + sorted(contains)
        return results[:limit]

    def recommend(
        self, movie_title: str, top_n: int = 10
    ) -> Optional[pd.DataFrame]:
        """
        Get movie recommendations using precomputed neighbors.

        Args:
            movie_title: The title of the movie to find similar movies for.
            top_n: Number of recommendations to return.

        Returns:
            DataFrame with recommended movies, or None if movie not found.
        """
        if not self._is_loaded or self._movies is None or self._neighbors is None:
            logger.error("Model not loaded.")
            return None

        # Find the movie index (case-insensitive)
        title_lower = movie_title.lower().strip()
        matches = self._movies[
            self._movies["title"].str.lower() == title_lower
        ]

        if matches.empty:
            logger.warning(f"Movie not found: '{movie_title}'")
            return None

        # Get index of the matched movie
        movie_idx: int = matches.index[0]

        # Look up precomputed neighbors (instant, no sorting needed)
        neighbor_list = self._neighbors.get(movie_idx, [])
        neighbor_list = neighbor_list[:top_n]

        if not neighbor_list:
            return None

        top_indices = [idx for idx, _ in neighbor_list]
        top_scores = [round(score * 100, 1) for _, score in neighbor_list]

        # Build recommendations DataFrame
        recommendations = self._movies.iloc[top_indices].copy()
        recommendations["similarity_score"] = top_scores

        return recommendations.reset_index(drop=True)

    def get_movie_details(self, movie_title: str) -> Optional[dict]:
        """
        Get detailed information about a specific movie.

        Args:
            movie_title: The title of the movie.

        Returns:
            Dictionary with movie details, or None if not found.
        """
        if not self._is_loaded or self._movies is None:
            return None

        title_lower = movie_title.lower().strip()
        matches = self._movies[
            self._movies["title"].str.lower() == title_lower
        ]

        if matches.empty:
            return None

        movie = matches.iloc[0]
        return {
            "movie_id": int(movie.get("movie_id", 0)),
            "title": movie["title"],
            "overview": movie.get("overview", "No overview available."),
            "genres": movie.get("genres", "Unknown"),
            "vote_average": float(movie.get("vote_average", 0)),
            "release_year": int(movie.get("release_year", 0)),
        }
