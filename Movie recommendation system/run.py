"""
run.py - Entry point for the CineMatch AI application.

Handles model building (if needed) and launches the Streamlit UI.
"""

import subprocess
import sys
import logging
from pathlib import Path

# ── Logging ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Paths ───────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
DATA_DIR = BASE_DIR / "data"
UI_APP = BASE_DIR / "ui" / "app.py"

MOVIES_PKL = MODEL_DIR / "movies.pkl"
SIMILARITY_PKL = MODEL_DIR / "similarity.pkl"
MOVIES_CSV = DATA_DIR / "tmdb_5000_movies.csv"
CREDITS_CSV = DATA_DIR / "tmdb_5000_credits.csv"


def check_datasets() -> bool:
    """Check if the required dataset files exist."""
    if not MOVIES_CSV.exists() or not CREDITS_CSV.exists():
        logger.error("=" * 60)
        logger.error("  DATASET FILES NOT FOUND!")
        logger.error("=" * 60)
        logger.error("")
        logger.error("  Please download the TMDB 5000 Movies Dataset:")
        logger.error("  https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata")
        logger.error("")
        logger.error(f"  Place the files in: {DATA_DIR}")
        logger.error("    - tmdb_5000_movies.csv")
        logger.error("    - tmdb_5000_credits.csv")
        logger.error("")
        logger.error("=" * 60)
        return False
    return True


def build_model_if_needed() -> bool:
    """Build the ML model if pickle files don't exist."""
    if MOVIES_PKL.exists() and SIMILARITY_PKL.exists():
        logger.info("Model files found. Skipping build.")
        return True

    logger.info("Model files not found. Building model...")

    if not check_datasets():
        return False

    try:
        # Import and run model builder
        from model.build_model import build
        build()
        return True
    except Exception as e:
        logger.error(f"Failed to build model: {e}")
        return False


def launch_streamlit() -> None:
    """Launch the Streamlit application."""
    logger.info("=" * 60)
    logger.info("  🎬 Launching CineMatch AI...")
    logger.info("=" * 60)
    logger.info("")
    logger.info("  The app will open in your browser automatically.")
    logger.info("  If not, navigate to: http://localhost:8501")
    logger.info("")
    logger.info("  Press Ctrl+C to stop the server.")
    logger.info("=" * 60)

    try:
        subprocess.run(
            [
                sys.executable, "-m", "streamlit", "run",
                str(UI_APP),
                "--server.headless=false",
                "--browser.gatherUsageStats=false",
                "--theme.base=dark",
                "--theme.primaryColor=#e94560",
                "--theme.backgroundColor=#0a0a0f",
                "--theme.secondaryBackgroundColor=#12121a",
                "--theme.textColor=#f0f0f5",
            ],
            cwd=str(BASE_DIR),
        )
    except KeyboardInterrupt:
        logger.info("\nServer stopped.")
    except FileNotFoundError:
        logger.error(
            "Streamlit not found. Install it: pip install streamlit"
        )
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    logger.info("🎬 CineMatch AI - Movie Recommendation System")
    logger.info("")

    # Step 1: Build model if needed
    model_ready = build_model_if_needed()

    if not model_ready:
        logger.warning(
            "Model not available. The app will start but "
            "recommendations won't work until the model is built."
        )

    # Step 2: Launch Streamlit UI
    launch_streamlit()


if __name__ == "__main__":
    main()
