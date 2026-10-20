"""Rule-based scam patterns. Each category: weight (base risk) and phrases (lowercase)."""

CATEGORIES = {
    "fake_kyc_update": {
        "label": "Fake KYC update",
        "weight": 35,
        "phrases": ["kyc", "update your kyc", "account will be blocked", "account will be suspended",
                    "pan card", "aadhaar", "verify your account", "kyc expired"],
    },
    "upi_refund_fraud": {
        "label": "UPI refund fraud",
        "weight": 40,
        "phrases": ["upi pin", "refund", "scan the qr", "collect request", "accept the request",
                    "google pay", "phonepe", "paytm", "wrong transfer"],
    },
    "lottery_scam": {
        "label": "Lottery / prize scam",
        "weight": 40,
        "phrases": ["lottery", "you have won", "lucky draw", "prize money", "claim your prize",
                    "processing fee", "congratulations"],
    },
    "fake_bank_officer": {
        "label": "Fake bank officer",
        "weight": 40,
        "phrases": ["bank manager", "calling from bank", "card blocked", "debit card", "credit card",
                    "otp", "cvv", "share the otp", "card number"],
    },
    "relative_impersonation": {
        "label": "Relative impersonation",
        "weight": 35,
        "phrases": ["it's me", "i am in trouble", "accident", "hospital", "send money urgently",
                    "don't tell anyone", "new number", "your nephew", "your son"],
    },
}

URGENCY_PHRASES = ["immediately", "urgent", "right now", "within 24 hours", "last warning", "arrest"]
