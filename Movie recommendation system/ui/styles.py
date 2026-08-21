"""
styles.py - Premium CSS that completely masks Streamlit's identity.
Every default Streamlit element is overridden or hidden.
"""


def get_custom_css() -> str:
    """Return the complete custom CSS for the application."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@400;500;600;700;800&display=swap');

    :root {
        --bg-primary: #06060b;
        --bg-secondary: #0e0e16;
        --bg-tertiary: #14141f;
        --bg-card: rgba(18, 18, 28, 0.7);
        --bg-glass: rgba(14, 14, 22, 0.75);
        --accent: #e94560;
        --accent-dim: rgba(233, 69, 96, 0.12);
        --accent-glow: rgba(233, 69, 96, 0.25);
        --blue: #0f3460;
        --blue-light: #64b5f6;
        --text-1: #eeeef3;
        --text-2: #9191a8;
        --text-3: #5a5a72;
        --border: rgba(255,255,255,0.05);
        --border-hover: rgba(233,69,96,0.25);
        --font: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        --font-d: 'Outfit', sans-serif;
    }

    /* ===== NUKE ALL STREAMLIT DEFAULTS ===== */
    #MainMenu, footer, .stDeployButton,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stHeader"],
    .reportview-container .main footer,
    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"],
    div[data-testid="stStatusWidget"],
    button[kind="header"],
    .css-1rs6os, .css-17ziqus,
    [data-testid="manage-app-button"],
    div[data-testid="stSidebarCollapsedControl"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        pointer-events: none !important;
    }

    .stApp > header {
        display: none !important;
        height: 0 !important;
    }

    /* ===== BASE ===== */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg-primary) !important;
        font-family: var(--font) !important;
        color: var(--text-1) !important;
    }

    .stApp {
        background: var(--bg-primary) !important;
        background-image:
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(233,69,96,0.06) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 60%, rgba(15,52,96,0.04) 0%, transparent 50%) !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }

    .block-container {
        max-width: 1280px !important;
        padding: 0 2rem 4rem !important;
        margin-top: 0 !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: #2a2a3a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

    /* ===== SELECTBOX FULL OVERRIDE ===== */
    .stSelectbox label {
        font-family: var(--font) !important;
        color: var(--text-2) !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.04em !important;
        text-transform: uppercase !important;
        margin-bottom: 0.5rem !important;
    }

    .stSelectbox [data-baseweb="select"] {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        font-family: var(--font) !important;
        transition: all 0.25s ease !important;
    }

    .stSelectbox [data-baseweb="select"]:hover,
    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent-glow), 0 4px 20px rgba(0,0,0,0.3) !important;
    }

    .stSelectbox [data-baseweb="select"] > div {
        background: transparent !important;
        color: var(--text-1) !important;
        padding: 6px 8px !important;
        font-size: 0.95rem !important;
    }

    /* Dropdown menu */
    [data-baseweb="popover"] {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        box-shadow: 0 16px 48px rgba(0,0,0,0.6) !important;
        backdrop-filter: blur(20px) !important;
    }

    [data-baseweb="popover"] ul {
        background: transparent !important;
    }

    [data-baseweb="popover"] li {
        color: var(--text-1) !important;
        font-family: var(--font) !important;
        font-size: 0.9rem !important;
        padding: 10px 16px !important;
        transition: background 0.15s ease !important;
    }

    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] li[aria-selected="true"] {
        background: var(--accent-dim) !important;
        color: var(--accent) !important;
    }

    /* Search input inside selectbox */
    [data-baseweb="select"] input {
        color: var(--text-1) !important;
        font-family: var(--font) !important;
        caret-color: var(--accent) !important;
    }

    /* ===== BUTTON FULL OVERRIDE ===== */
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #c23152 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.85rem 2.5rem !important;
        font-family: var(--font) !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.03em;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px var(--accent-glow) !important;
        position: relative;
        overflow: hidden;
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 30px rgba(233,69,96,0.4) !important;
        background: linear-gradient(135deg, #f05672 0%, #d4405f 100%) !important;
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.99) !important;
    }

    .stButton > button:focus {
        box-shadow: 0 4px 15px var(--accent-glow) !important;
        outline: none !important;
    }

    /* ===== SPINNER OVERRIDE ===== */
    .stSpinner > div {
        border-top-color: var(--accent) !important;
    }

    /* ===== COLUMN GAPS ===== */
    [data-testid="stHorizontalBlock"] {
        gap: 1rem !important;
    }

    /* ===== HERO ===== */
    .hero-wrap {
        text-align: center;
        padding: 3.5rem 1rem 1rem;
        position: relative;
        overflow: visible;
    }

    .hero-glow {
        position: absolute;
        top: -80px;
        left: 50%;
        transform: translateX(-50%);
        width: 500px;
        height: 500px;
        background: radial-gradient(circle, rgba(233,69,96,0.07) 0%, transparent 65%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--accent-dim);
        border: 1px solid rgba(233,69,96,0.18);
        color: var(--accent);
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: var(--font);
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        animation: fadeDown 0.6s ease-out;
    }

    .hero-title {
        font-family: var(--font-d);
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #e94560 50%, #ff8fa3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 0.6rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
        animation: fadeDown 0.6s ease-out 0.1s both;
    }

    .hero-sub {
        font-size: 1.05rem;
        color: var(--text-2);
        font-weight: 300;
        letter-spacing: 0.02em;
        max-width: 480px;
        margin: 0 auto;
        line-height: 1.6;
        animation: fadeDown 0.6s ease-out 0.2s both;
    }

    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ===== SEARCH PANEL ===== */
    .search-panel {
        background: var(--bg-glass);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 1.8rem 2rem;
        margin: 2rem auto;
        max-width: 640px;
        box-shadow: 0 8px 40px rgba(0,0,0,0.35);
        animation: fadeUp 0.5s ease-out 0.3s both;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ===== SOURCE MOVIE BANNER ===== */
    .source-banner {
        background: linear-gradient(135deg, rgba(233,69,96,0.06) 0%, rgba(15,52,96,0.06) 100%);
        border: 1px solid rgba(233,69,96,0.1);
        border-radius: 16px;
        padding: 1.5rem 1.8rem;
        margin: 1.5rem 0 2rem;
        position: relative;
        overflow: hidden;
        animation: fadeUp 0.4s ease-out;
    }

    .source-banner::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--blue), var(--accent));
    }

    .source-title {
        font-family: var(--font-d);
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text-1);
        margin-bottom: 0.4rem;
    }

    .source-meta {
        display: flex;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 0.5rem;
    }

    .source-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        font-size: 0.8rem;
        color: var(--text-2);
        font-weight: 500;
    }

    .source-chip .val { color: var(--text-1); }

    .source-overview {
        font-size: 0.85rem;
        color: var(--text-3);
        line-height: 1.6;
        margin-top: 0.5rem;
    }

    /* ===== SECTION HEADING ===== */
    .sec-head {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 2.5rem 0 0.5rem;
        animation: fadeUp 0.4s ease-out;
    }

    .sec-head-bar {
        width: 3px;
        height: 28px;
        background: var(--accent);
        border-radius: 2px;
        flex-shrink: 0;
    }

    .sec-head-text {
        font-family: var(--font-d);
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-1);
    }

    .sec-sub {
        color: var(--text-3);
        font-size: 0.85rem;
        margin: 0.2rem 0 1.5rem 15px;
    }

    /* ===== MOVIE CARD ===== */
    .m-card {
        background: var(--bg-card);
        backdrop-filter: blur(10px);
        border: 1px solid var(--border);
        border-radius: 14px;
        overflow: hidden;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        cursor: default;
        animation: cardIn 0.5s ease-out both;
    }

    .m-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: var(--border-hover);
        box-shadow: 0 12px 40px rgba(233,69,96,0.12), 0 4px 20px rgba(0,0,0,0.4);
    }

    @keyframes cardIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Poster area */
    .m-poster {
        position: relative;
        overflow: hidden;
        aspect-ratio: 2/3;
        background: var(--bg-tertiary);
    }

    .m-poster img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .m-card:hover .m-poster img { transform: scale(1.06); }

    .m-poster-grad {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 35%;
        background: linear-gradient(to top, var(--bg-primary) 0%, transparent 100%);
        pointer-events: none;
        z-index: 1;
    }

    .m-badge {
        position: absolute;
        top: 10px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 700;
        font-family: var(--font);
        backdrop-filter: blur(8px);
        letter-spacing: 0.02em;
    }

    .m-badge-rating {
        right: 10px;
        background: rgba(233,69,96,0.85);
        color: #fff;
    }

    .m-badge-match {
        left: 10px;
        background: rgba(15,52,96,0.85);
        color: var(--blue-light);
    }

    /* Card info */
    .m-info {
        padding: 0.8rem 1rem 1.1rem;
    }

    .m-name {
        font-family: var(--font-d);
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-1);
        margin-bottom: 0.35rem;
        line-height: 1.25;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .m-meta {
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
        margin-bottom: 0.4rem;
    }

    .m-year {
        font-size: 0.73rem;
        color: var(--text-3);
        font-weight: 500;
    }

    .m-dot {
        width: 3px; height: 3px;
        background: var(--text-3);
        border-radius: 50%;
        flex-shrink: 0;
    }

    .m-genre {
        display: inline-block;
        background: var(--accent-dim);
        color: var(--accent);
        padding: 1px 7px;
        border-radius: 6px;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }

    .m-desc {
        font-size: 0.75rem;
        color: var(--text-3);
        line-height: 1.5;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    /* ===== SVG POSTER PLACEHOLDER ===== */
    .poster-placeholder {
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: linear-gradient(160deg, #12121f 0%, #0a0a14 50%, #14101a 100%);
        color: var(--text-3);
        gap: 8px;
        position: relative;
        z-index: 2;
    }

    .poster-placeholder svg { opacity: 0.4; }

    .poster-placeholder span {
        font-family: var(--font-d);
        font-size: 0.7rem;
        font-weight: 600;
        text-align: center;
        padding: 0 0.5rem;
        opacity: 0.5;
        line-height: 1.3;
    }

    /* ===== ERROR STATE ===== */
    .err-box {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(233,69,96,0.03);
        border: 1px solid rgba(233,69,96,0.08);
        border-radius: 16px;
        margin: 2rem auto;
        max-width: 480px;
        animation: fadeUp 0.4s ease-out;
    }

    .err-icon { font-size: 2.5rem; margin-bottom: 0.8rem; opacity: 0.7; }

    .err-msg {
        color: var(--text-2);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* ===== FOOTER ===== */
    .app-footer {
        text-align: center;
        padding: 3rem 1rem 1.5rem;
        color: var(--text-3);
        font-size: 0.75rem;
        border-top: 1px solid var(--border);
        margin-top: 4rem;
        letter-spacing: 0.02em;
    }

    .app-footer a {
        color: var(--accent);
        text-decoration: none;
    }

    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title { font-size: 2.4rem; }
        .search-panel { padding: 1.2rem; margin: 1rem; border-radius: 16px; }
        .block-container { padding: 0 0.8rem 3rem !important; }
    }

    /* ===== ANIMATION DELAYS FOR CARD STAGGER ===== */
    .delay-1 { animation-delay: 0.05s; }
    .delay-2 { animation-delay: 0.10s; }
    .delay-3 { animation-delay: 0.15s; }
    .delay-4 { animation-delay: 0.20s; }
    .delay-5 { animation-delay: 0.25s; }
    .delay-6 { animation-delay: 0.30s; }
    .delay-7 { animation-delay: 0.35s; }
    .delay-8 { animation-delay: 0.40s; }
    .delay-9 { animation-delay: 0.45s; }
    .delay-10 { animation-delay: 0.50s; }

    /* Kill any remaining Streamlit branding */
    a[href*="streamlit.io"] { display: none !important; }
    iframe[title="streamlit_analytics"] { display: none !important; }
    </style>
    """
