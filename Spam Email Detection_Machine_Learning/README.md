# 📧 Spam Email/SMS Classifier — Machine Learning Project

A complete beginner-to-intermediate ML project that classifies messages as
**SPAM** or **HAM** (normal), built with Python and scikit-learn.

---

## 📁 Project Files

| File | Purpose |
|---|---|
| `generate_data.py` | Creates a 600-message synthetic dataset (`data/spam_dataset.csv`) |
| `spam_classifier.py` | Cleans text, trains the model, evaluates it, predicts new messages |
| `data/spam_dataset.csv` | The dataset (300 spam + 300 ham messages) |
| `confusion_matrix.png` | Visual result of how well the model performed |

---

## ▶️ How to Run

```bash
pip install pandas scikit-learn matplotlib

python3 generate_data.py      # Step 1: create the dataset
python3 spam_classifier.py    # Step 2: train, evaluate, and test the model
```

---

## 🧠 How It Works (Concept Breakdown)

### 1. The Problem
Given a message (email/SMS), predict whether it is **spam** (unwanted/scam)
or **ham** (a normal, legitimate message). This is a **binary text
classification** problem — one of the most common real-world ML tasks
(used by Gmail, WhatsApp, banking apps, etc.).

### 2. Text Preprocessing (`clean_text`)
Machine Learning models can't understand raw sentences directly, so we first:
- Convert everything to **lowercase** (so "FREE" and "free" are treated the same)
- Remove **punctuation**
- Remove extra spaces

### 3. Feature Extraction — TF-IDF
Computers only understand numbers, not words. We use **TF-IDF**
(Term Frequency – Inverse Document Frequency) to convert each message into
a vector of numbers:
- **Term Frequency**: how often a word appears in a message
- **Inverse Document Frequency**: how rare/unique that word is across all messages

Words like "free", "winner", "click", "urgent" get **high importance**
because they appear a lot in spam but rarely in normal messages.

### 4. The Model — Multinomial Naive Bayes
We use **Naive Bayes**, a probability-based algorithm that is:
- Very fast to train
- Works exceptionally well for text classification
- Based on **Bayes' Theorem**: it calculates the probability a message is
  spam given the words it contains, using word-frequency patterns learned
  from the training data.

### 5. Train/Test Split
We split data into:
- **80% training data** — the model learns patterns from this
- **20% testing data** — used to check if the model generalizes well to
  messages it has never seen before

### 6. Evaluation Metrics
| Metric | Meaning |
|---|---|
| **Accuracy** | % of all messages correctly classified |
| **Precision** | Of messages predicted "spam", how many really were spam? (avoids false alarms) |
| **Recall** | Of all real spam messages, how many did we catch? (avoids missed spam) |
| **F1 Score** | Balance between precision and recall |
| **Confusion Matrix** | Table showing correct vs incorrect predictions per class |

### 7. Predicting New Messages
The script ends by testing the trained model on 5 brand-new messages it
never saw during training — showing the predicted label and the model's
confidence (%).

---

## 📊 Sample Output

```
Accuracy : 100.00%
Precision: 100.00%
Recall   : 100.00%
F1 Score : 100.00%

[SPAM] (99% spam confidence)  -> Congratulations! You won a free iPhone...
[HAM ] (11% spam confidence)  -> Hey, are you free for a call at 5 PM today?
```

> Note: Accuracy is very high here because the dataset is synthetic and
> templated (patterns are clear-cut). On a **real-world dataset**
> (e.g., the classic "SMS Spam Collection" dataset), expect **95–98%**
> accuracy — still excellent, but more realistic.

---

## 🚀 Ideas to Extend This Project (great for teaching / portfolio)

1. **Use a real dataset** — e.g., the UCI "SMS Spam Collection" or Kaggle's
   Enron spam dataset instead of synthetic data.
2. **Try other models** — Logistic Regression, SVM, or Random Forest — and
   compare accuracy.
3. **Add more features** — message length, number of exclamation marks,
   presence of links/numbers.
4. **Deploy it** — wrap the model in a simple Flask/Streamlit web app where
   users can paste a message and get an instant prediction.
5. **Use deep learning** — try an LSTM or a pretrained transformer
   (e.g., BERT) for higher accuracy on real-world messy data.

---

## 🎓 Key Takeaway for Students
This project demonstrates the **full ML pipeline** used in real
applications: **raw data → cleaning → feature engineering → model
training → evaluation → prediction** — the same workflow used in
production spam filters, fraud detection, and sentiment analysis systems.
