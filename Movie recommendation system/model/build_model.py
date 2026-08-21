"""
build_model.py - Builds the movie recommendation model.

Processes the TMDB 5000 Movies Dataset, creates feature vectors
using CountVectorizer, computes cosine similarity matrix, and
saves the processed data for the recommendation engine.
"""

import os
import ast
import logging
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Logging Configuration ───────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── Path Configuration ──────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent.parent
DATA_DIR: Path = BASE_DIR / "data"
MODEL_DIR: Path = BASE_DIR / "model"

MOVIES_CSV: Path = DATA_DIR / "tmdb_5000_movies.csv"
CREDITS_CSV: Path = DATA_DIR / "tmdb_5000_credits.csv"

MOVIES_PKL: Path = MODEL_DIR / "movies.pkl"
SIMILARITY_PKL: Path = MODEL_DIR / "similarity.pkl"
NEIGHBORS_PKL: Path = MODEL_DIR / "neighbors.pkl"


def _parse_json_column(text: str) -> list[str]:
    """Safely parse a JSON-like string column and extract 'name' fields."""
    try:
        data = ast.literal_eval(text)
        return [item["name"].replace(" ", "") for item in data]
    except (ValueError, SyntaxError, KeyError):
        return []


def _extract_top_cast(text: str, top_n: int = 3) -> list[str]:
    """Extract the top N cast members from the cast column."""
    try:
        data = ast.literal_eval(text)
        return [member["name"].replace(" ", "") for member in data[:top_n]]
    except (ValueError, SyntaxError, KeyError):
        return []


def _extract_director(text: str) -> list[str]:
    """Extract the director name from the crew column."""
    try:
        data = ast.literal_eval(text)
        for member in data:
            if member.get("job") == "Director":
                return [member["name"].replace(" ", "")]
        return []
    except (ValueError, SyntaxError, KeyError):
        return []


def load_and_merge_data() -> pd.DataFrame:
    """Load CSV files and merge them on the 'title' column."""
    logger.info("Loading datasets...")

    if not MOVIES_CSV.exists():
        logger.error(f"Movies CSV not found at: {MOVIES_CSV}")
        sys.exit(1)
    if not CREDITS_CSV.exists():
        logger.error(f"Credits CSV not found at: {CREDITS_CSV}")
        sys.exit(1)

    movies = pd.read_csv(MOVIES_CSV)
    credits = pd.read_csv(CREDITS_CSV)

    logger.info(f"Movies dataset shape: {movies.shape}")
    logger.info(f"Credits dataset shape: {credits.shape}")

    # Merge datasets on title
    df = movies.merge(credits, on="title", how="inner")
    logger.info(f"Merged dataset shape: {df.shape}")

    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset by selecting relevant columns and handling missing values."""
    logger.info("Cleaning dataset...")

    # Select relevant columns
    columns_to_keep = [
        "movie_id", "title", "overview", "genres", "keywords",
        "cast", "crew", "vote_average", "release_date", "popularity",
    ]

    # Handle column naming differences
    if "movie_id" not in df.columns and "id" in df.columns:
        df = df.rename(columns={"id": "movie_id"})

    available_cols = [col for col in columns_to_keep if col in df.columns]
    df = df[available_cols].copy()

    # Drop rows with missing overview
    df = df.dropna(subset=["overview"])

    # Fill remaining NaN values
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna("")

    logger.info(f"Cleaned dataset shape: {df.shape}")
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineer the 'tags' feature by combining multiple text columns."""
    logger.info("Engineering features...")

    # Parse JSON columns
    df["genres_list"] = df["genres"].apply(_parse_json_column)
    df["keywords_list"] = df["keywords"].apply(_parse_json_column)
    df["cast_list"] = df["cast"].apply(_extract_top_cast)
    df["director_list"] = df["crew"].apply(_extract_director)

    # Process overview into word list
    df["overview_list"] = df["overview"].apply(lambda x: x.split())

    # Combine all features into tags
    df["tags"] = (
        df["genres_list"]
        + df["keywords_list"]
        + df["cast_list"]
        + df["director_list"]
        + df["overview_list"]
    )

    # Convert tags list to string
    df["tags"] = df["tags"].apply(lambda x: " ".join(x).lower())

    # Extract release year safely
    df["release_year"] = pd.to_datetime(
        df["release_date"], errors="coerce"
    ).dt.year.fillna(0).astype(int)

    # Keep only the columns we need
    final_columns = [
        "movie_id", "title", "tags", "genres_list",
        "vote_average", "release_year", "overview",
    ]
    available_final = [col for col in final_columns if col in df.columns]
    df = df[available_final].copy()

    # Store genres as comma-separated string for display
    if "genres_list" in df.columns:
        df["genres"] = df["genres_list"].apply(
            lambda x: ", ".join([g.replace("Science", "Sci-").replace("Fiction", "Fi") if "Fiction" in g else g for g in x]) if x else "Unknown"
        )
        # Fix genre names back to readable format
        df["genres"] = df["genres"].str.replace("ScienceFiction", "Sci-Fi")
        df.drop(columns=["genres_list"], inplace=True)

    logger.info(f"Feature-engineered dataset shape: {df.shape}")
    logger.info(f"Sample tags: {df['tags'].iloc[0][:200]}...")

    return df


def build_similarity_matrix(df: pd.DataFrame) -> np.ndarray:
    """Build the cosine similarity matrix using CountVectorizer."""
    logger.info("Building similarity matrix...")

    # Create count vectors
    vectorizer = CountVectorizer(
        max_features=5000,
        stop_words="english",
    )
    vectors = vectorizer.fit_transform(df["tags"])

    logger.info(f"Vocabulary size: {len(vectorizer.vocabulary_)}")
    logger.info(f"Vector matrix shape: {vectors.shape}")

    # Compute cosine similarity
    similarity = cosine_similarity(vectors)
    logger.info(f"Similarity matrix shape: {similarity.shape}")

    return similarity


def save_model(df: pd.DataFrame, similarity: np.ndarray) -> None:
    """Save processed data and precomputed top-N neighbors (lightweight)."""
    logger.info("Saving model artifacts...")

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    # Reset index for clean storage
    df = df.reset_index(drop=True)

    # Precompute top-20 neighbors per movie (avoids loading the full matrix)
    top_n = 20
    logger.info(f"Precomputing top-{top_n} neighbors for {len(df)} movies...")
    neighbors: dict[int, list[tuple[int, float]]] = {}
    for i in range(len(df)):
        # Get similarity scores, exclude self
        scores = list(enumerate(similarity[i]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        # Store top-N (skip index 0 = self) as (index, score) tuples
        neighbors[i] = [(idx, round(float(s), 4)) for idx, s in scores[1:top_n + 1]]

    joblib.dump(df, MOVIES_PKL)
    joblib.dump(neighbors, NEIGHBORS_PKL)

    # Report file sizes
    movies_size = MOVIES_PKL.stat().st_size / (1024 * 1024)
    neighbors_size = NEIGHBORS_PKL.stat().st_size / (1024 * 1024)

    logger.info(f"Saved movies.pkl ({movies_size:.1f} MB)")
    logger.info(f"Saved neighbors.pkl ({neighbors_size:.1f} MB)")
    logger.info(f"  (Replaced 176 MB similarity.pkl with {neighbors_size:.1f} MB neighbors.pkl)")


def build() -> None:
    """Main pipeline to build the recommendation model."""
    logger.info("=" * 60)
    logger.info("  MOVIE RECOMMENDATION MODEL BUILDER")
    logger.info("=" * 60)

    # Step 1: Load and merge data
    df = load_and_merge_data()

    # Step 2: Clean dataset
    df = clean_dataset(df)

    # Step 3: Engineer features
    df = engineer_features(df)

    # Step 4: Build similarity matrix
    similarity = build_similarity_matrix(df)

    # Step 5: Save model artifacts
    save_model(df, similarity)

    logger.info("=" * 60)
    logger.info("  MODEL BUILD COMPLETE!")
    logger.info(f"  Total movies processed: {len(df)}")
    logger.info("=" * 60)


if __name__ == "__main__":
    build()
