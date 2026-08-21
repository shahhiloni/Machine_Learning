"""
app.py - Main application for CineMatch AI.
"""

import sys
import logging
from pathlib import Path

import streamlit as st

# ── Add project root to path ───────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.recommender import MovieRecommender
from utils.poster import fetch_poster_url
from ui.styles import get_custom_css
from ui.components import (
    render_hero,
    render_search_section,
    render_source_movie,
    render_section_header,
    render_movie_card,
    render_error,
    render_no_model_error,
    render_footer,
)

# ── Logging ─────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Page Configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch — AI Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_resource(show_spinner=False)
def load_recommender() -> MovieRecommender:
    """Load and cache the recommendation engine."""
    recommender = MovieRecommender()
    recommender.load_model()
    return recommender


def main() -> None:
    """Main application entry point."""
    # Inject custom CSS (must be first)
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # Render hero
    render_hero()

    # Load model
    recommender = load_recommender()

    if not recommender.is_loaded:
        render_no_model_error()
        render_footer()
        return

    # Search section
    movie_titles = recommender.get_movie_titles()
    selected_movie = render_search_section(movie_titles)

    # Persist selection across reruns
    if selected_movie:
        st.session_state["selected_movie"] = selected_movie

    if st.session_state.get("selected_movie"):
        movie_name = st.session_state["selected_movie"]

        # Source movie details
        details = recommender.get_movie_details(movie_name)
        if details:
            render_source_movie(details)

        # Get recommendations
        recommendations = recommender.recommend(movie_name, top_n=10)

        if recommendations is None or recommendations.empty:
            render_error(
                f"No recommendations found for <strong>{movie_name}</strong>. "
                "Please try a different movie."
            )
        else:
            render_section_header(
                "Top 10 Recommendations",
                f"Movies similar to {movie_name}",
            )

            # Render in 5-column grid with staggered animations
            card_idx = 0
            for row_start in range(0, len(recommendations), 5):
                row_end = min(row_start + 5, len(recommendations))
                cols = st.columns(5)

                for i, col in enumerate(cols):
                    idx = row_start + i
                    if idx >= row_end:
                        break

                    movie = recommendations.iloc[idx]
                    poster_url = fetch_poster_url(
                        int(movie.get("movie_id", 0)),
                        movie["title"],
                    )

                    with col:
                        render_movie_card(
                            title=movie["title"],
                            poster_url=poster_url,
                            genres=movie.get("genres", "Unknown"),
                            year=int(movie.get("release_year", 0)),
                            rating=float(movie.get("vote_average", 0)),
                            overview=movie.get("overview", ""),
                            similarity=float(movie.get("similarity_score", 0)),
                            index=card_idx,
                        )
                    card_idx += 1

    render_footer()


if __name__ == "__main__":
    main()
