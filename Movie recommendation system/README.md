# 🎬 CineMatch AI - Movie Recommendation System

An AI-powered movie recommendation system built with Python, Scikit-learn, and Streamlit. Uses content-based filtering with cosine similarity to recommend movies similar to your favorites.

---

## 🏗️ Project Architecture

```
MovieRecommendation/
│
├── data/                          # Dataset files
│   ├── tmdb_5000_movies.csv       # TMDB movies dataset
│   └── tmdb_5000_credits.csv      # TMDB credits dataset
│
├── model/                         # ML model
│   ├── build_model.py             # Model training pipeline
│   ├── movies.pkl                 # Processed movie data (generated)
│   └── similarity.pkl             # Cosine similarity matrix (generated)
│
├── ui/                            # Frontend (Streamlit)
│   ├── app.py                     # Main application
│   ├── components.py              # Reusable UI components
│   └── styles.py                  # CSS styles (Netflix theme)
│
├── utils/                         # Utility modules
│   ├── recommender.py             # Recommendation engine
│   └── poster.py                  # TMDB poster fetcher
│
├── assets/                        # Static assets
│   └── logo.png                   # App logo
│
├── .streamlit/
│   └── config.toml                # Streamlit configuration
│
├── requirements.txt               # Python dependencies
├── run.py                         # Application entry point
├── run_ui.bat                     # Windows launcher
└── README.md                      # This file
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Internet connection (for initial setup)

### Step 1: Download the Dataset

Download the **TMDB 5000 Movies Dataset** from Kaggle:

🔗 [https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

Place the two CSV files in the `data/` directory:
- `data/tmdb_5000_movies.csv`
- `data/tmdb_5000_credits.csv`

### Step 2: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Build the Model

```bash
python model/build_model.py
```

This will:
- Load and merge the datasets
- Clean and preprocess the data
- Extract features (genres, keywords, cast, crew, overview)
- Build CountVectorizer with 5000 features
- Compute cosine similarity matrix
- Save `movies.pkl` and `similarity.pkl`

---

## 🚀 Running the Application

### Option A: Using the Batch File (Windows)

Simply double-click `run_ui.bat` or run:

```bash
run_ui.bat
```

This will automatically:
1. Create a virtual environment (if needed)
2. Install dependencies
3. Build the model (if needed)
4. Launch the Streamlit app
5. Open your browser

### Option B: Manual Launch

```bash
python run.py
```

### Option C: Direct Streamlit Launch

```bash
streamlit run ui/app.py
```

The app will be available at: **http://localhost:8501**

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Search** | Search movies with autocomplete from 4800+ titles |
| 🤖 **AI Recommendations** | Content-based filtering using cosine similarity |
| 🎴 **Movie Cards** | Rich cards with poster, rating, genres, year, overview |
| 🌙 **Dark Theme** | Netflix-inspired premium dark UI |
| 📱 **Responsive** | Works on desktop, tablet, and mobile |
| ⚡ **Fast** | Cached model loading for instant recommendations |
| 🖼️ **Posters** | TMDB API integration for movie posters (optional) |

---

## 🖼️ Movie Posters (Optional)

To enable movie poster images, set your TMDB API key:

```bash
# Windows
set TMDB_API_KEY=your_api_key_here

# Linux/Mac
export TMDB_API_KEY=your_api_key_here
```

Get a free API key at: [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

> Without an API key, placeholder images will be shown instead.

---

## 🧠 How It Works

1. **Data Processing**: Merges movies and credits datasets
2. **Feature Engineering**: Combines genres, keywords, top 3 cast, director, and overview into a single "tags" field
3. **Vectorization**: Applies `CountVectorizer` (5000 max features, English stop words removed)
4. **Similarity**: Computes pairwise cosine similarity between all movie vectors
5. **Recommendation**: For a selected movie, returns the top 10 most similar movies by cosine score

---

## 📸 Screenshots

> *Screenshots will appear here after running the application.*

| Home Screen | Recommendations |
|-------------|-----------------|
| *Search interface* | *Movie cards grid* |

---

## 🛠️ Tech Stack

- **Python 3.12+** — Core language
- **Streamlit** — Web UI framework
- **Pandas** — Data manipulation
- **Scikit-learn** — ML (CountVectorizer, cosine similarity)
- **NumPy** — Numerical computations
- **Joblib** — Model serialization
- **Requests** — TMDB API calls

---

## 📝 License

This project is for educational purposes. The TMDB dataset is provided by [The Movie Database](https://www.themoviedb.org/).

---

<p align="center">Built with ❤️ using Python, Streamlit & Scikit-learn</p>
