"""
generate_data.py
-----------------
Generates a synthetic but medically-realistic Heart Disease dataset,
modeled after the well-known UCI Cleveland Heart Disease dataset structure.

Features used (standard in real heart-disease ML datasets):
    age       : age in years
    sex       : 1 = male, 0 = female
    cp        : chest pain type (0-3)
    trestbps  : resting blood pressure (mm Hg)
    chol      : serum cholesterol (mg/dl)
    fbs       : fasting blood sugar > 120 mg/dl (1 = true, 0 = false)
    restecg   : resting ECG results (0-2)
    thalach   : maximum heart rate achieved
    exang     : exercise induced angina (1 = yes, 0 = no)
    oldpeak   : ST depression induced by exercise relative to rest
    slope     : slope of the peak exercise ST segment (0-2)
    ca        : number of major vessels colored by fluoroscopy (0-3)
    thal      : thalassemia (1 = normal, 2 = fixed defect, 3 = reversible defect)
    target    : 1 = has heart disease, 0 = no heart disease

Run this first -> creates data/heart_dataset.csv
"""

import random
import csv
import os

random.seed(42)


def generate_patient(has_disease):
    """
    Generate one synthetic patient record.
    Patients with heart disease are given feature distributions that
    skew toward known risk patterns (higher age, higher cholesterol,
    lower max heart rate, more chest pain / angina, etc.)
    This mimics real-world correlations without using real patient data.

    NOTE: The disease/no-disease ranges below OVERLAP on purpose (instead
    of being cleanly separated). Real medical data is noisy - a healthy
    person can have high cholesterol, and a sick person can have a normal
    heart rate. This overlap means the model will NOT get 100% accuracy,
    which is realistic and better for teaching.
    """
    if has_disease:
        age = random.randint(40, 77)
        sex = random.choices([1, 0], weights=[0.62, 0.38])[0]
        cp = random.choices([0, 1, 2, 3], weights=[0.4, 0.25, 0.2, 0.15])[0]
        trestbps = random.randint(110, 180)
        chol = random.randint(190, 400)
        fbs = random.choices([0, 1], weights=[0.7, 0.3])[0]
        restecg = random.choices([0, 1, 2], weights=[0.45, 0.45, 0.1])[0]
        thalach = random.randint(95, 175)
        exang = random.choices([0, 1], weights=[0.5, 0.5])[0]
        oldpeak = round(random.uniform(0.3, 4.0), 1)
        slope = random.choices([0, 1, 2], weights=[0.4, 0.35, 0.25])[0]
        ca = random.choices([0, 1, 2, 3], weights=[0.35, 0.3, 0.2, 0.15])[0]
        thal = random.choices([1, 2, 3], weights=[0.3, 0.3, 0.4])[0]
    else:
        age = random.randint(29, 70)
        sex = random.choices([1, 0], weights=[0.48, 0.52])[0]
        cp = random.choices([0, 1, 2, 3], weights=[0.2, 0.28, 0.32, 0.2])[0]
        trestbps = random.randint(100, 155)
        chol = random.randint(160, 300)
        fbs = random.choices([0, 1], weights=[0.8, 0.2])[0]
        restecg = random.choices([0, 1, 2], weights=[0.55, 0.4, 0.05])[0]
        thalach = random.randint(120, 202)
        exang = random.choices([0, 1], weights=[0.78, 0.22])[0]
        oldpeak = round(random.uniform(0.0, 2.2), 1)
        slope = random.choices([0, 1, 2], weights=[0.2, 0.35, 0.45])[0]
        ca = random.choices([0, 1, 2, 3], weights=[0.6, 0.25, 0.1, 0.05])[0]
        thal = random.choices([1, 2, 3], weights=[0.48, 0.32, 0.2])[0]

    return {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal,
        "target": 1 if has_disease else 0,
    }


def generate_dataset(n_per_class=300):
    rows = []
    for _ in range(n_per_class):
        rows.append(generate_patient(has_disease=True))
    for _ in range(n_per_class):
        rows.append(generate_patient(has_disease=False))
    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    rows = generate_dataset(1500)
    fieldnames = list(rows[0].keys())
    with open("data/heart_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Dataset created: data/heart_dataset.csv ({len(rows)} patient records)")
