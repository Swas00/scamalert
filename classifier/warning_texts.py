WARNINGS = {
    "fake_kyc_update": "Warning. This looks like a fake KYC update scam. Banks never ask you to update KYC over a phone call. Do not share any details and hang up.",
    "upi_refund_fraud": "Warning. This looks like a UPI refund scam. Never enter your UPI PIN or accept a collect request to receive money. Hang up now.",
    "lottery_scam": "Warning. This looks like a lottery scam. You cannot win a prize you did not enter. Never pay a fee to claim a prize.",
    "fake_bank_officer": "Warning. This caller may be pretending to be a bank officer. Never share your OTP, CVV or card number with anyone.",
    "relative_impersonation": "Warning. This may be someone pretending to be your relative. Call your family member on a known number before sending any money.",
}
DEFAULT = "Warning. This call shows signs of a scam. Do not share personal or financial details."


def warning_text(category: str | None) -> str:
    return WARNINGS.get(category or "", DEFAULT)
