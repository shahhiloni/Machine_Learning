"""
components.py - Premium UI components with SVG poster fallbacks
and staggered card animations. Zero Streamlit look.
"""

import streamlit as st
from typing import Optional


# ── SVG film-icon placeholder (inline, no external dependency) ──────
_FILM_SVG = (
    '<svg width="40" height="40" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
    'stroke-linejoin="round">'
    '<rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"/>'
    '<line x1="7" y1="2" x2="7" y2="22"/>'
    '<line x1="17" y1="2" x2="17" y2="22"/>'
    '<line x1="2" y1="12" x2="22" y2="12"/>'
    '<line x1="2" y1="7" x2="7" y2="7"/>'
    '<line x1="2" y1="17" x2="7" y2="17"/>'
    '<line x1="17" y1="17" x2="22" y2="17"/>'
    '<line x1="17" y1="7" x2="22" y2="7"/>'
    '</svg>'
)


def render_hero() -> None:
    """Render the hero/header section."""
    st.markdown(
        f"""
        <div class="hero-wrap">
            <div class="hero-glow"></div>
            <div class="hero-badge">
                <span>✦</span> AI-POWERED RECOMMENDATIONS
            </div>
            <h1 class="hero-title">CineMatch</h1>
            <p class="hero-sub">
                Discover movies you'll love — powered by machine learning
                and 4,800+ titles from TMDB.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_search_section(movie_titles: list[str]) -> Optional[str]:
    """Render the search panel with styled selectbox and button."""
    st.markdown('<div class="search-panel">', unsafe_allow_html=True)

    selected = st.selectbox(
        "SEARCH MOVIES",
        options=[""] + movie_titles,
        format_func=lambda x: "Start typing a movie name…" if x == "" else x,
        key="movie_search",
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        clicked = st.button(
            "Get Recommendations",
            key="recommend_btn",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if clicked and selected:
        return selected
    return None


def render_source_movie(details: dict) -> None:
    """Render the selected movie banner."""
    year = details["release_year"] if details["release_year"] > 0 else "—"
    rating = details["vote_average"]
    overview = details["overview"]
    if len(overview) > 220:
        overview = overview[:220] + "…"

    st.markdown(
        f"""
        <div class="source-banner">
            <div class="source-title">{details['title']}</div>
            <div class="source-meta">
                <span class="source-chip">⭐ <span class="val">{rating}/10</span></span>
                <span class="source-chip">📅 <span class="val">{year}</span></span>
                <span class="source-chip">🎭 <span class="val">{details['genres']}</span></span>
            </div>
            <div class="source-overview">{overview}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str = "") -> None:
    """Render a styled section header."""
    st.markdown(
        f"""
        <div class="sec-head">
            <div class="sec-head-bar"></div>
            <div class="sec-head-text">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(
            f'<div class="sec-sub">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def _poster_html(poster_url: str, title: str) -> str:
    """Return poster img tag or SVG placeholder if URL is a placeholder."""
    is_placeholder = (
        not poster_url
        or "placeholder.com" in poster_url
        or poster_url.startswith("data:")
    )

    if is_placeholder:
        short = title[:24] + "…" if len(title) > 24 else title
        return (
            f'<div class="poster-placeholder">'
            f'{_FILM_SVG}'
            f'<span>{short}</span>'
            f'</div>'
        )
    return (
        f'<img src="{poster_url}" alt="{title}" loading="lazy" '
        f'onerror="this.parentElement.innerHTML='
        f"'<div class=poster-placeholder>{_FILM_SVG}"
        f"<span>{title[:20]}</span></div>'\">"
    )


def render_movie_card(
    title: str,
    poster_url: str,
    genres: str,
    year: int,
    rating: float,
    overview: str,
    similarity: float = 0.0,
    index: int = 0,
) -> None:
    """Render a single movie card with staggered animation."""
    # Genre tags (max 2)
    genre_list = [g.strip() for g in genres.split(",") if g.strip() and g.strip() != "Unknown"][:2]
    genre_html = "".join(f'<span class="m-genre">{g}</span>' for g in genre_list)

    year_str = str(year) if year > 0 else "—"
    desc = overview[:130] + "…" if len(overview) > 130 else overview

    match_badge = ""
    if similarity > 0:
        match_badge = f'<div class="m-badge m-badge-match">{similarity}% match</div>'

    poster = _poster_html(poster_url, title)
    delay_cls = f"delay-{min(index + 1, 10)}"

    st.markdown(
        f"""
        <div class="m-card {delay_cls}">
            <div class="m-poster">
                {poster}
                <div class="m-poster-grad"></div>
                <div class="m-badge m-badge-rating">⭐ {rating:.1f}</div>
                {match_badge}
            </div>
            <div class="m-info">
                <div class="m-name">{title}</div>
                <div class="m-meta">
                    <span class="m-year">{year_str}</span>
                    <span class="m-dot"></span>
                    {genre_html}
                </div>
                <div class="m-desc">{desc}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_error(message: str) -> None:
    """Render an error state."""
    st.markdown(
        f"""
        <div class="err-box">
            <div class="err-icon">🎬</div>
            <div class="err-msg">{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_no_model_error() -> None:
    """Render the missing model error."""
    st.markdown(
        """
        <div class="err-box">
            <div class="err-icon">⚙️</div>
            <div class="err-msg">
                <strong>Model not built yet</strong><br><br>
                Download the TMDB 5000 dataset, place CSVs in <code>data/</code>,
                then run:<br><br>
                <code style="color:#e94560">python model/build_model.py</code>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the footer."""
    st.markdown(
        """
        <div class="app-footer">
            CineMatch &mdash; Content-based recommendation engine<br>
            Powered by TMDB 5000 Movies Dataset &bull; Built with Python &amp; Scikit-learn
        </div>
        """,
        unsafe_allow_html=True,
    )
