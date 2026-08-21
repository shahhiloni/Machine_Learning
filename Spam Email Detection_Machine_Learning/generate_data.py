"""
generate_data.py
-----------------
Generates a synthetic but realistic dataset of SPAM and HAM (normal) messages
using sentence templates. This gives us a decent-sized dataset (600+ rows)
without needing an internet download.

Run this first -> creates data/spam_dataset.csv
"""

import random
import csv
import os

random.seed(42)

# ---------------------------------------------------------
# SPAM message templates (common patterns real spam uses)
# ---------------------------------------------------------
spam_templates = [
    "Congratulations! You have won a {prize} worth ${amount}. Click here {link} to claim now!",
    "URGENT: Your account will be suspended. Verify your details immediately at {link}",
    "You have been selected for a FREE {prize}! Reply YES to claim your prize now.",
    "Limited time offer! Get {percent}% off on all products. Shop now {link}",
    "Dear customer, you have won ${amount} in our lucky draw. Claim before it expires!",
    "WINNER!! As a valued network customer you have been selected to receive a {prize}!",
    "Your loan of ${amount} has been approved. No credit check needed. Apply now {link}",
    "Congratulations, you've been chosen for a free {prize} cruise! Call now to claim.",
    "Act now! Your {prize} is waiting. Click {link} before offer expires today.",
    "You have 1 new voicemail regarding your unclaimed ${amount} refund. Call now.",
    "Hot singles in your area want to chat with you! Click {link} now",
    "Get rich quick! Earn ${amount} per day working from home. No experience needed.",
    "FINAL NOTICE: Your payment of ${amount} is overdue. Pay now to avoid penalty {link}",
    "Claim your FREE {prize} today, no purchase necessary! Limited stock, hurry up.",
    "You've been pre-approved for a credit card with ${amount} limit. Apply instantly.",
    "This is not a scam! You really did win a {prize}. Text WIN to 12345 to claim.",
    "Lowest prices guaranteed on {prize}! Buy 1 get 1 free, offer ends tonight {link}",
    "Your Amazon account has an issue with order. Verify now to avoid cancellation {link}",
    "Make ${amount} a week doing simple online surveys. Sign up free today!",
    "Alert: Suspicious login detected. Confirm your identity now or account will be locked {link}",
]

prizes = ["iPhone 16", "vacation package", "gift card", "laptop", "smartwatch",
          "cash prize", "Amazon voucher", "PlayStation 5", "spa weekend", "car"]
links = ["www.claim-prize-now.com", "bit.ly/xyz123", "www.free-gift-offer.net",
         "www.verify-account-now.com", "tinyurl.com/winbig"]
amounts = ["500", "1000", "2500", "10000", "750", "5000", "200", "15000"]
percents = ["50", "70", "80", "90", "60", "40"]

# ---------------------------------------------------------
# HAM (normal, legitimate) message templates
# ---------------------------------------------------------
ham_templates = [
    "Hey, are we still meeting for lunch tomorrow at {time}?",
    "Can you send me the report before the {day} meeting?",
    "Thanks for your help yesterday, really appreciate it!",
    "Don't forget to pick up milk on your way home.",
    "The project deadline has been moved to next {day}.",
    "Happy birthday! Hope you have a wonderful day.",
    "Let's catch up over coffee this {day}, are you free?",
    "I attached the notes from today's class, let me know if anything is unclear.",
    "Can we reschedule our call to {time} instead?",
    "Just checking in, how is the assignment coming along?",
    "The meeting has been confirmed for {time} in conference room B.",
    "Please review the attached document and share your feedback by {day}.",
    "Mom said dinner will be ready by {time}, come home soon.",
    "Great job on the presentation today, the client loved it.",
    "Reminder: your dentist appointment is scheduled for {day} at {time}.",
    "Can you help me move some furniture this weekend?",
    "I'll be a few minutes late, traffic is heavy today.",
    "The exam syllabus has been updated, please check the portal.",
    "Let's finalize the budget numbers before {day}'s review.",
    "Thanks for sending the invoice, I'll process the payment by {day}.",
]

times = ["10 AM", "2 PM", "6 PM", "noon", "9:30 AM", "5 PM"]
days = ["Monday", "Friday", "Wednesday", "next week", "tomorrow", "Thursday"]


def fill(template):
    return template.format(
        prize=random.choice(prizes),
        link=random.choice(links),
        amount=random.choice(amounts),
        percent=random.choice(percents),
        time=random.choice(times),
        day=random.choice(days),
    )


def generate_dataset(n_per_class=300):
    rows = []
    for _ in range(n_per_class):
        rows.append((fill(random.choice(spam_templates)), "spam"))
    for _ in range(n_per_class):
        rows.append((fill(random.choice(ham_templates)), "ham"))
    random.shuffle(rows)
    return rows


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    rows = generate_dataset(300)
    with open("data/spam_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "message"])
        for message, label in rows:
            writer.writerow([label, message])
    print(f"Dataset created: data/spam_dataset.csv ({len(rows)} messages)")
