"""
spam_classifier.py
-------------------
A complete, beginner-friendly Machine Learning project:
SPAM EMAIL / SMS CLASSIFIER

Pipeline:
1. Load data (data/spam_dataset.csv)
2. Clean & preprocess text
3. Convert text -> numeric features using TF-IDF
4. Train a Naive Bayes classifier
5. Evaluate (accuracy, precision, recall, confusion matrix)
6. Predict on new custom messages

Run:
    python3 generate_data.py       # creates the dataset (only once)
    python3 spam_classifier.py     # trains + evaluates + demo predictions
"""

import re
import string
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)


# ============================================================
# STEP 1: TEXT CLEANING FUNCTION
# ============================================================
def clean_text(text):
    """
    Basic text preprocessing:
    - lowercase everything
    - remove punctuation
    - remove extra whitespace
    """
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def main():
    # ============================================================
    # STEP 2: LOAD DATA
    # ============================================================
    df = pd.read_csv("data/spam_dataset.csv")
    print(f"Loaded {len(df)} messages")
    print(df["label"].value_counts(), "\n")

    df["clean_message"] = df["message"].apply(clean_text)

    # ============================================================
    # STEP 3: TRAIN / TEST SPLIT
    # ============================================================
    X = df["clean_message"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)} | Testing samples: {len(X_test)}\n")

    # ============================================================
    # STEP 4: TEXT -> NUMBERS (TF-IDF VECTORIZATION)
    # TF-IDF = Term Frequency - Inverse Document Frequency
    # It scores each word by how important/unique it is to a message.
    # ============================================================
    vectorizer = TfidfVectorizer(stop_words="english", max_features=3000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # ============================================================
    # STEP 5: TRAIN THE MODEL (Multinomial Naive Bayes)
    # Naive Bayes is fast, simple, and works very well for text
    # classification tasks like spam detection.
    # ============================================================
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    # ============================================================
    # STEP 6: EVALUATE THE MODEL
    # ============================================================
    y_pred = model.predict(X_test_vec)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, pos_label="spam")
    recall = recall_score(y_test, y_pred, pos_label="spam")
    f1 = f1_score(y_test, y_pred, pos_label="spam")

    print("=" * 50)
    print("MODEL PERFORMANCE")
    print("=" * 50)
    print(f"Accuracy : {accuracy:.2%}")
    print(f"Precision: {precision:.2%}  (of predicted spam, how much was correct)")
    print(f"Recall   : {recall:.2%}  (of actual spam, how much was caught)")
    print(f"F1 Score : {f1:.2%}")
    print("=" * 50, "\n")

    # Confusion matrix (visual)
    cm = confusion_matrix(y_test, y_pred, labels=["ham", "spam"])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["ham", "spam"])
    disp.plot(cmap="Purples")
    plt.title("Spam Classifier - Confusion Matrix")
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=150)
    print("Saved confusion_matrix.png\n")

    # ============================================================
    # STEP 7: TEST ON NEW / CUSTOM MESSAGES
    # ============================================================
    sample_messages = [
        "Congratulations! You won a free iPhone, click here to claim now!",
        "Hey, are you free for a call at 5 PM today?",
        "URGENT: verify your bank account now to avoid suspension",
        "Can you send me the notes from yesterday's class?",
        "Earn $5000 a week from home, no experience required!",
    ]

    print("=" * 50)
    print("PREDICTIONS ON NEW MESSAGES")
    print("=" * 50)
    cleaned = [clean_text(m) for m in sample_messages]
    vec = vectorizer.transform(cleaned)
    predictions = model.predict(vec)
    probs = model.predict_proba(vec)

    for msg, pred, prob in zip(sample_messages, predictions, probs):
        spam_prob = prob[list(model.classes_).index("spam")]
        print(f"[{pred.upper():5}] ({spam_prob:.0%} spam confidence)  -> {msg}")

    return model, vectorizer


def predict_message(model, vectorizer, message):
    """Utility: predict a single custom message."""
    cleaned = clean_text(message)
    vec = vectorizer.transform([cleaned])
    pred = model.predict(vec)[0]
    prob = model.predict_proba(vec)[0]
    spam_prob = prob[list(model.classes_).index("spam")]
    return pred, spam_prob


if __name__ == "__main__":
    main()
