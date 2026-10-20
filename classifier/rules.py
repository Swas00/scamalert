"""Rule data for scam detection.

Phrases are (text, weight) pairs. Weight = how strongly the phrase signals a scam on its own
(roughly 5 = weak/ambiguous, 15 = moderate, 30+ = strong). English, romanized Hindi (Hinglish)
and Devanagari variants live side by side. All Latin phrases are lowercase.
"""

CATEGORIES = {
    "fake_kyc_update": {
        "label": "Fake KYC update",
        "phrases": [
            ("kyc", 12), ("update your kyc", 30), ("kyc expired", 30), ("kyc update", 25),
            ("account will be blocked", 25), ("account will be suspended", 25),
            ("verify your account", 15), ("pan card", 8), ("aadhaar", 8), ("aadhar", 8),
            ("kyc update karna", 30), ("kyc expire", 30), ("account band", 25),
            ("account block ho", 25), ("pan card update", 25), ("aadhaar update", 25),
            ("केवाईसी", 12), ("केवाईसी अपडेट", 30), ("केवाईसी एक्सपायर", 30), ("केवाईसी expire", 30), ("अकाउंट बैंड", 25), ("अकाउंट बंद", 25), ("एक्सपायर हो गया", 15),
            ("खाता बंद", 25), ("खाता ब्लॉक", 25), ("अकाउंट ब्लॉक", 25), ("पैन कार्ड", 8), ("आधार", 6),
        ],
    },
    "upi_refund_fraud": {
        "label": "UPI refund fraud",
        "phrases": [
            ("refund", 8), ("upi pin", 35), ("scan the qr", 30), ("collect request", 30),
            ("accept the request", 25), ("wrong transfer", 20), ("paisa wapas", 15),
            ("google pay", 6), ("phonepe", 6), ("paytm", 6), ("gpay", 6),
            ("upi pin batao", 35), ("qr code scan", 30), ("request accept karo", 30),
            ("galti se paise", 20), ("refund milega", 20), ("paise wapas", 15),
            ("रिफंड", 8), ("यूपीआई पिन", 35), ("क्यूआर कोड", 25), ("गलती से पैसे", 20),
            ("पैसे वापस", 15), ("रिक्वेस्ट एक्सेप्ट", 30),
        ],
    },
    "lottery_scam": {
        "label": "Lottery / prize scam",
        "phrases": [
            ("lottery", 25), ("you have won", 30), ("lucky draw", 25), ("prize money", 25),
            ("claim your prize", 30), ("processing fee", 25), ("congratulations", 6),
            ("kbc", 15), ("inaam", 15), ("aapne jeeta hai", 30), ("lottery lagi", 30),
            ("lucky draw jeeta", 30), ("registration fee", 20), ("inaam jeeta", 30),
            ("लॉटरी", 25), ("इनाम", 15), ("आपने जीता", 30), ("आप जीत गए", 30),
            ("लकी ड्रॉ", 25), ("बधाई हो", 6), ("प्रोसेसिंग फीस", 25),
        ],
    },
    "fake_bank_officer": {
        "label": "Fake bank officer",
        "phrases": [
            ("bank manager", 20), ("calling from bank", 25), ("card blocked", 25),
            ("debit card", 8), ("credit card", 8), ("card number", 25), ("expiry date", 15),
            ("bank se bol raha", 30), ("bank se bol rahi", 30), ("bank manager bol", 30),
            ("card block ho", 25), ("card band", 20), ("card number batao", 35),
            ("बैंक से बोल", 30), ("बैंक मैनेजर", 20), ("कार्ड ब्लॉक", 25),
            ("कार्ड बंद", 20), ("कार्ड नंबर", 25), ("डेबिट कार्ड", 8), ("क्रेडिट कार्ड", 8),
        ],
    },
    "relative_impersonation": {
        "label": "Relative impersonation",
        "phrases": [
            ("it's me", 10), ("i am in trouble", 30), ("accident", 15), ("hospital", 12),
            ("new number", 15), ("your nephew", 20), ("your son", 12), ("your grandson", 20),
            ("pehchana", 15), ("pehchaan", 15), ("mera naya number", 25), ("naya number", 15),
            ("main musibat mein", 30), ("emergency hai", 20), ("hospital mein", 20),
            ("beta bol raha", 20), ("पहचाना", 15), ("नया नंबर", 20), ("मेरा नया नंबर", 25),
            ("मुसीबत में", 30), ("दुर्घटना", 15), ("अस्पताल", 12), ("एक्सीडेंट", 15),
        ],
    },
}

# Cross-category signals. Each group has its own phrases with weights.
SIGNALS = {
    "urgency": [
        ("immediately", 12), ("urgent", 12), ("right now", 12), ("within 24 hours", 15),
        ("last warning", 15), ("hurry", 8), ("jaldi", 10), ("turant", 12), ("abhi ke abhi", 15),
        ("fauran", 12), ("24 ghante", 15), ("तुरंत", 12), ("जल्दी", 10), ("अभी के अभी", 15),
        ("फौरन", 12), ("२४ घंटे", 15), ("24 घंटे", 15),
    ],
    "credential": [
        ("otp", 25), ("cvv", 30), ("upi pin", 30), ("atm pin", 30), ("password", 15),
        ("share the otp", 35), ("otp batao", 35), ("otp bata", 30), ("otp share", 35),
        ("pin batao", 35), ("otp bhejo", 35), ("ओटीपी", 25), ("ओटीपी बताओ", 35),
        ("ओटीपी बताइए", 35), ("सीवीवी", 30), ("पिन बताओ", 35), ("पिन नंबर", 25),
    ],
    "threat": [
        ("arrest", 20), ("legal action", 20), ("police case", 20), ("court", 10),
        ("account will be blocked", 15), ("sim will be blocked", 20), ("giraftar", 20),
        ("police case ho", 20), ("band ho jayega", 18), ("block ho jayega", 18),
        ("jail", 15), ("गिरफ्तार", 20), ("पुलिस केस", 20), ("बंद हो जाएगा", 18),
        ("ब्लॉक हो जाएगा", 18), ("कानूनी कार्रवाई", 20), ("जेल", 15),
    ],
    "secrecy": [
        ("don't tell anyone", 20), ("do not tell anyone", 20), ("keep this secret", 20),
        ("kisi ko mat batana", 25), ("kisi ko na batana", 25), ("kisi ko mat batao", 25),
        ("किसी को मत बताना", 25), ("किसी को न बताना", 25), ("किसी को मत बताओ", 25),
    ],
    "payment_request": [
        ("send money", 20), ("transfer money", 20), ("send money urgently", 30),
        ("paise bhejo", 25), ("paise transfer", 20), ("paisa bhejo", 25), ("money bhejo", 25),
        ("पैसे भेजो", 25), ("पैसे ट्रांसफर", 20), ("पैसा भेजो", 25), ("पैसे भेज दो", 25),
    ],
}

# Combination bonuses: (signal groups that must all be present, bonus points).
COMBOS = [
    (("urgency", "credential"), 25),
    (("threat", "credential"), 20),
    (("threat", "urgency"), 10),
    (("secrecy", "payment_request"), 20),
    (("urgency", "payment_request"), 15),
]

# Phrases that indicate a legitimate warning (e.g. a real bank SMS read aloud); they reduce the score.
DAMPENERS = [
    ("do not share", 30), ("never share", 30), ("don't share", 30), ("is your otp", 15),
    ("kisi ke saath share na", 30), ("share na karein", 30), ("kabhi share na", 30),
    ("किसी के साथ शेयर न", 30), ("शेयर न करें", 30), ("साझा न करें", 30),
]
