"""
poster.py - Movie poster fetcher using TMDB API.
"""

import logging
import os
from typing import Optional
from functools import lru_cache

import requests

logger = logging.getLogger(__name__)

TMDB_API_KEY: str = os.environ.get("TMDB_API_KEY", "")
TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE: str = "https://image.tmdb.org/t/p/w500"
PLACEHOLDER_POSTER: str = "https://via.placeholder.com/500x750/1a1a2e/e94560?text=No+Poster"


@lru_cache(maxsize=512)
def fetch_poster_url(movie_id: int, movie_title: str = "") -> str:
    """Fetch poster URL from TMDB API with caching and fallback."""
    if not TMDB_API_KEY:
        return _generate_placeholder(movie_title)
    try:
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        params = {"api_key": TMDB_API_KEY, "language": "en-US"}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"{TMDB_IMAGE_BASE}{poster_path}"
        return _generate_placeholder(movie_title)
    except Exception as e:
        logger.warning(f"TMDB API error for movie ID {movie_id}: {e}")
        return _generate_placeholder(movie_title)


def _generate_placeholder(title: str = "") -> str:
    """Generate a placeholder poster URL."""
    if title:
        clean_title = title.replace(" ", "+")[:30]
        return f"https://via.placeholder.com/500x750/1a1a2e/e94560?text={clean_title}"
    return PLACEHOLDER_POSTER


def fetch_posters_batch(movie_ids: list[int], movie_titles: list[str]) -> list[str]:
    """Fetch poster URLs for multiple movies."""
    return [fetch_poster_url(mid, t) for mid, t in zip(movie_ids, movie_titles)]
