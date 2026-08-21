"""
heart_disease_classifier.py
----------------------------
A complete Machine Learning project:
HEART DISEASE PREDICTION

Pipeline:
1. Load patient data (data/heart_dataset.csv)
2. Split features (X) and target (y)
3. Scale numeric features
4. Train a Random Forest classifier
5. Evaluate (accuracy, precision, recall, confusion matrix, feature importance)
6. Predict for a new patient

Run:
    python3 generate_data.py               # creates the dataset (only once)
    python3 heart_disease_classifier.py    # trains + evaluates + demo prediction
"""

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)

FEATURE_NAMES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal",
]

# Full, student-friendly labels for plots (instead of short codes)
FEATURE_LABELS = {
    "age": "Age",
    "sex": "Sex",
    "cp": "Chest Pain Type",
    "trestbps": "Resting Blood Pressure",
    "chol": "Cholesterol Level",
    "fbs": "Fasting Blood Sugar",
    "restecg": "Resting ECG Result",
    "thalach": "Maximum Heart Rate Achieved",
    "exang": "Exercise-Induced Angina",
    "oldpeak": "ST Depression (Exercise)",
    "slope": "Slope of ST Segment",
    "ca": "Number of Major Vessels Blocked",
    "thal": "Thalassemia Type",
}


def main():
    # ============================================================
    # STEP 1: LOAD DATA
    # ============================================================
    df = pd.read_csv("data/heart_dataset.csv")
    print(f"Loaded {len(df)} patient records")
    print(df["target"].value_counts().rename({1: "disease", 0: "no disease"}), "\n")

    X = df[FEATURE_NAMES]
    y = df["target"]

    # ============================================================
    # STEP 2: TRAIN / TEST SPLIT
    # ============================================================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training samples: {len(X_train)} | Testing samples: {len(X_test)}\n")

    # ============================================================
    # STEP 3: FEATURE SCALING
    # Random Forest doesn't strictly need scaling, but we scale here
    # so the pipeline generalizes well if you swap in Logistic
    # Regression or SVM later.
    # ============================================================
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ============================================================
    # STEP 4: TRAIN THE MODEL (Random Forest)
    # Random Forest = many decision trees voting together.
    # It handles mixed numeric/categorical medical features well
    # and gives us feature importance for free.
    # ============================================================
    model = RandomForestClassifier(
        n_estimators=200, max_depth=6, random_state=42
    )
    model.fit(X_train_scaled, y_train)

    # ============================================================
    # STEP 5: EVALUATE THE MODEL
    # ============================================================
    y_pred = model.predict(X_test_scaled)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("=" * 50)
    print("MODEL PERFORMANCE")
    print("=" * 50)
    print(f"Accuracy : {accuracy:.2%}")
    print(f"Precision: {precision:.2%}  (of predicted 'disease', how much was correct)")
    print(f"Recall   : {recall:.2%}  (of actual disease cases, how much was caught)")
    print(f"F1 Score : {f1:.2%}")
    print("=" * 50, "\n")

    # Confusion matrix (visual)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["No Disease", "Disease"]
    )
    fig, ax = plt.subplots(figsize=(8, 6.5))
    disp.plot(cmap="Purples", ax=ax, colorbar=True, values_format="d")
    for text in disp.text_.ravel():
        text.set_fontsize(20)
    ax.set_title("Heart Disease Classifier - Confusion Matrix", fontsize=16, pad=15)
    ax.set_xlabel("Predicted Label", fontsize=13)
    ax.set_ylabel("True Label", fontsize=13)
    ax.tick_params(labelsize=12)
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=200)
    print("Saved confusion_matrix.png")

    # ============================================================
    # STEP 6: FEATURE IMPORTANCE
    # Shows which medical factors mattered most to the model.
    # ============================================================
    importances = model.feature_importances_
    readable_names = [FEATURE_LABELS[f] for f in FEATURE_NAMES]
    imp_series = pd.Series(importances, index=readable_names).sort_values()

    fig, ax = plt.subplots(figsize=(11, 8))
    bars = ax.barh(imp_series.index, imp_series.values, color="#7c3aed")
    ax.set_title("Feature Importance - What Drives the Prediction?", fontsize=17, pad=15)
    ax.set_xlabel("Importance Score", fontsize=13)
    ax.tick_params(labelsize=12)
    # Add value labels next to each bar for clarity when presenting
    for bar, value in zip(bars, imp_series.values):
        ax.text(value + 0.003, bar.get_y() + bar.get_height() / 2,
                 f"{value:.1%}", va="center", fontsize=11)
    plt.tight_layout()
    plt.savefig("feature_importance.png", dpi=200)
    print("Saved feature_importance.png\n")

    # ============================================================
    # STEP 7: PREDICT FOR NEW / SAMPLE PATIENTS
    # ============================================================
    sample_patients = pd.DataFrame([
        # A higher-risk profile
        {"age": 62, "sex": 1, "cp": 3, "trestbps": 152, "chol": 290, "fbs": 1,
         "restecg": 1, "thalach": 118, "exang": 1, "oldpeak": 2.6,
         "slope": 1, "ca": 2, "thal": 3},
        # A lower-risk profile
        {"age": 34, "sex": 0, "cp": 1, "trestbps": 112, "chol": 190, "fbs": 0,
         "restecg": 0, "thalach": 178, "exang": 0, "oldpeak": 0.4,
         "slope": 2, "ca": 0, "thal": 1},
    ])

    sample_scaled = scaler.transform(sample_patients[FEATURE_NAMES])
    predictions = model.predict(sample_scaled)
    probs = model.predict_proba(sample_scaled)

    print("=" * 50)
    print("PREDICTIONS FOR NEW PATIENTS")
    print("=" * 50)
    for i, (pred, prob) in enumerate(zip(predictions, probs)):
        risk_prob = prob[1]
        label = "HIGH RISK (disease predicted)" if pred == 1 else "LOW RISK (no disease predicted)"
        print(f"Patient {i+1}: {label}  ->  {risk_prob:.0%} probability of heart disease")

    return model, scaler


def predict_patient(model, scaler, patient_dict):
    """Utility: predict for a single custom patient dict."""
    df = pd.DataFrame([patient_dict])[FEATURE_NAMES]
    scaled = scaler.transform(df)
    pred = model.predict(scaled)[0]
    prob = model.predict_proba(scaled)[0][1]
    return pred, prob


if __name__ == "__main__":
    main()
