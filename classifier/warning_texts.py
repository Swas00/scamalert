# Spoken warnings by language, then category. Languages without a translation fall back to English.
WARNINGS = {
    "en-IN": {
        "fake_kyc_update": "Warning. This looks like a fake KYC update scam. Banks never ask you to update KYC over a phone call. Do not share any details and hang up.",
        "upi_refund_fraud": "Warning. This looks like a UPI refund scam. Never enter your UPI PIN or accept a collect request to receive money. Hang up now.",
        "lottery_scam": "Warning. This looks like a lottery scam. You cannot win a prize you did not enter. Never pay a fee to claim a prize.",
        "fake_bank_officer": "Warning. This caller may be pretending to be a bank officer. Never share your OTP, CVV or card number with anyone.",
        "relative_impersonation": "Warning. This may be someone pretending to be your relative. Call your family member on a known number before sending any money.",
        "fake_authority": "Warning. This looks like a scam by someone pretending to be police or a government officer. There is no such thing as a digital arrest. Hang up, and do not transfer any money.",
        "default": "Warning. This call shows signs of a scam. Do not share personal or financial details.",
    },
    "hi-IN": {
        "fake_kyc_update": "सावधान! यह फर्जी केवाईसी अपडेट का घोटाला लगता है। बैंक कभी फोन पर केवाईसी अपडेट करने को नहीं कहते। कोई जानकारी साझा न करें और फोन काट दें।",
        "upi_refund_fraud": "सावधान! यह यूपीआई रिफंड का घोटाला लगता है। पैसे पाने के लिए कभी अपना यूपीआई पिन न डालें और न ही कोई रिक्वेस्ट स्वीकार करें। अभी फोन काट दें।",
        "lottery_scam": "सावधान! यह लॉटरी का घोटाला लगता है। आप ऐसा इनाम नहीं जीत सकते जिसमें आपने हिस्सा ही नहीं लिया। इनाम के लिए कभी कोई फीस न दें।",
        "fake_bank_officer": "सावधान! यह कॉलर खुद को बैंक अधिकारी बता रहा हो सकता है। अपना ओटीपी, सीवीवी या कार्ड नंबर किसी को न बताएं।",
        "relative_impersonation": "सावधान! यह कोई आपका रिश्तेदार बनकर बात कर रहा हो सकता है। पैसे भेजने से पहले अपने परिवार के सदस्य को उनके पुराने नंबर पर फोन करें।",
        "fake_authority": "सावधान! यह पुलिस या सरकारी अधिकारी बनकर की जा रही ठगी लगती है। डिजिटल अरेस्ट जैसी कोई चीज़ नहीं होती। फोन काट दें और किसी को पैसे न भेजें।",
        "default": "सावधान! इस कॉल में धोखाधड़ी के संकेत हैं। अपनी निजी या वित्तीय जानकारी साझा न करें।",
    },
}


def warning_text(category: str | None, language: str = "en-IN") -> tuple[str, str]:
    """Return (text, language actually used)."""
    lang = language if language in WARNINGS else "en-IN"
    texts = WARNINGS[lang]
    return texts.get(category or "", texts["default"]), lang
