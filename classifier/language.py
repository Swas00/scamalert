import re

# Unicode block -> Gnani language code. Devanagari maps to Hindi (Marathi shares the script).
SCRIPTS = [
    (r"[ऀ-ॿ]", "hi-IN"), (r"[஀-௿]", "ta-IN"), (r"[ఀ-౿]", "te-IN"),
    (r"[ಀ-೿]", "kn-IN"), (r"[ഀ-ൿ]", "ml-IN"), (r"[ঀ-৿]", "bn-IN"),
    (r"[઀-૿]", "gu-IN"), (r"[਀-੿]", "pa-IN"),
]

# Common romanized-Hindi words; two or more distinct hits in Latin text => Hinglish.
HINGLISH_MARKERS = {
    "hai", "hain", "hu", "hoon", "aap", "aapka", "aapke", "aapne", "mera", "meri", "main", "mein",
    "karo", "karna", "kar", "batao", "bata", "bhejo", "bol", "raha", "rahi", "ho", "jayega", "gaya",
    "nahi", "nahin", "paise", "paisa", "abhi", "turant", "jaldi", "warna", "kya", "ka", "ki", "ke",
    "sir", "bhai", "haan", "kab", "tak", "chahiye", "mil", "milte", "theek", "kuch", "koi", "tum", "tumhara", "kal", "aur", "se", "ko", "naya", "musibat", "badhai", "inaam",
}
HINGLISH_MIN_HITS = 3


def detect_language(text: str) -> str:
    counts = [(len(re.findall(rx, text)), code) for rx, code in SCRIPTS]
    n, code = max(counts)
    if n > 0 and n >= sum(c for c, _ in counts) / 2:
        return code
    words = set(re.findall(r"[a-z']+", text.lower()))
    return "hi-IN" if len(words & HINGLISH_MARKERS) >= HINGLISH_MIN_HITS else "en-IN"
