"""Additional scam types and wording, layered on top of rules.py (imported by classifier.py).

Written from publicly described Indian scam patterns (RBI / I4C / cyber-police advisories): fake job and
"task" offers, investment and trading groups, instant-loan apps, remote-access "support", electricity and SIM
disconnection threats, courier/customs calls, insurance and tax-refund calls, plus extra wording for the original types.
Phrases are lowercase; Latin phrases match on word boundaries, other scripts as substrings.
"""
from rules import CATEGORIES, CATEGORY_PATTERNS, DAMPENER_PATTERNS, DAMPENERS, SIGNAL_PATTERNS, SIGNALS


def add_phrases(category: str, label: str, phrases: list[tuple[str, int]]) -> None:
    cat = CATEGORIES.setdefault(category, {"label": label, "phrases": []})
    cat["phrases"].extend(phrases)


# ---------------------------------------------------------------------------------------------------------------
# New categories: English, Hinglish, Devanagari Hindi
# ---------------------------------------------------------------------------------------------------------------
add_phrases("job_task_scam", "Fake job / task scam", [
    ("part time job", 20), ("part-time job", 20), ("work from home", 18), ("earn per day", 25), ("daily income", 20),
    ("like youtube videos", 35), ("like and subscribe", 15), ("rate hotels", 25), ("complete tasks", 20),
    ("telegram group", 25), ("whatsapp group", 12), ("join our telegram", 30), ("commission on every task", 30),
    ("registration deposit", 25), ("recharge your wallet", 30), ("task wallet", 30), ("hr department", 8),
    ("ghar baithe", 15), ("ghar baithe kamao", 30), ("part time kaam", 20), ("roz kamao", 25), ("daily kamai", 25),
    ("task complete karo", 25), ("telegram par judo", 30), ("telegram group join", 30),
    ("पार्ट टाइम जॉब", 20), ("घर बैठे कमाएं", 30), ("घर बैठे कमाओ", 30), ("रोज़ कमाएं", 25), ("रोज कमाएं", 25),
    ("टेलीग्राम ग्रुप", 25), ("टास्क पूरा", 25), ("वीडियो लाइक", 30), ("वर्क फ्रॉम होम", 18),
])
add_phrases("investment_scam", "Investment / trading scam", [
    ("guaranteed returns", 35), ("guaranteed profit", 35), ("double your money", 40), ("triple your money", 40),
    ("100% profit", 35), ("risk free", 20), ("risk-free", 20), ("stock tips", 20), ("trading group", 25),
    ("vip group", 25), ("vip trading", 30), ("crypto investment", 30), ("bitcoin", 12), ("usdt", 20), ("ipo allotment", 25),
    ("insider tip", 30), ("fixed returns", 25), ("monthly returns", 20), ("invest today", 20), ("minimum investment", 20),
    ("pakka munafa", 35), ("guaranteed munafa", 35), ("paisa double", 40), ("paise double", 40), ("double paisa", 40),
    ("share market tips", 25), ("trading ka group", 25), ("crypto mein invest", 30), ("invest karo", 20), ("nivesh karo", 20),
    ("गारंटीड रिटर्न", 35), ("पक्का मुनाफा", 35), ("पैसे डबल", 40), ("पैसा डबल", 40), ("दोगुना पैसा", 40),
    ("शेयर मार्केट टिप्स", 25), ("ट्रेडिंग ग्रुप", 25), ("निवेश करें", 18), ("निवेश करो", 20), ("क्रिप्टो", 15),
])
add_phrases("loan_app_scam", "Fake loan offer", [
    ("instant loan", 25), ("pre-approved loan", 30), ("pre approved loan", 30), ("loan approved", 20),
    ("loan without documents", 30), ("no documents required", 25), ("no cibil", 25), ("zero interest loan", 25),
    ("processing fee for loan", 35), ("insurance fee for loan", 35), ("loan sanction", 15), ("low interest loan", 18),
    ("loan mil jayega", 30), ("turant loan", 30), ("bina document", 25), ("bina cibil", 25), ("loan approve ho gaya", 30),
    ("processing fee pehle", 35), ("loan ke liye fees", 30),
    ("तुरंत लोन", 30), ("इंस्टेंट लोन", 30), ("लोन अप्रूव", 25), ("बिना डॉक्यूमेंट", 25), ("बिना सिबिल", 25),
    ("लोन पास हो गया", 30), ("प्रोसेसिंग फीस पहले", 35),
])
add_phrases("remote_access_scam", "Remote-access / tech-support scam", [
    ("anydesk", 40), ("teamviewer", 40), ("team viewer", 40), ("quicksupport", 40), ("quick support", 30), ("rustdesk", 40),
    ("screen share", 25), ("share your screen", 35), ("remote access", 35), ("install the app", 15),
    ("microsoft support", 35), ("technical support", 12), ("your computer has a virus", 40), ("virus detected", 30),
    ("your device is hacked", 35), ("your account is hacked", 25), ("download the app i send", 30),
    ("एनीडेस्क", 40), ("टीमव्यूअर", 40), ("टीम व्यूअर", 40), ("क्विक सपोर्ट", 35), ("स्क्रीन शेयर", 25),
    ("ऐप डाउनलोड करें", 20), ("ऐप डाउनलोड कीजिए", 20), ("एप डाउनलोड करो", 20), ("कंप्यूटर में वायरस", 40),
    ("app download karo", 22), ("screen share karo", 35), ("anydesk download", 45),
])
add_phrases("utility_disconnection_scam", "Fake utility / SIM disconnection", [
    ("electricity bill", 12), ("bijli ka bill", 12), ("power will be disconnected", 40), ("electricity will be disconnected", 40),
    ("connection will be cut", 35), ("connection will be disconnected", 35), ("disconnected tonight", 40),
    ("bill is pending", 18), ("bill not updated", 25), ("update your bill", 25), ("meter reading", 8),
    ("sim will be deactivated", 40), ("sim will be disconnected", 40), ("sim card will be blocked", 40), ("mobile number will be blocked", 40),
    ("trai", 12), ("5g upgrade", 25), ("number will be deactivated", 40), ("gas connection will", 30),
    ("bijli kat jayegi", 40), ("bijli ka connection kat", 40), ("aaj raat bijli", 40), ("connection kat jayega", 35),
    ("sim band ho jayega", 40), ("sim block ho jayega", 40), ("number band ho jayega", 40), ("bill update nahi", 25),
    ("बिजली कट", 35), ("बिजली का कनेक्शन कट", 40), ("आज रात बिजली", 40), ("कनेक्शन कट जाएगा", 35),
    ("सिम बंद हो जाएगा", 40), ("सिम ब्लॉक हो जाएगा", 40), ("नंबर बंद हो जाएगा", 40), ("बिल अपडेट नहीं", 25),
    ("ट्राई", 12), ("बिजली का बिल", 12),
])
add_phrases("courier_customs_scam", "Courier / customs parcel scam", [
    ("fedex", 20), ("dhl", 15), ("blue dart", 15), ("customs duty", 30), ("customs clearance fee", 40), ("parcel is held", 35),
    ("parcel has been seized", 40), ("parcel in your name", 30), ("your parcel contains", 35), ("package contains", 25),
    ("delivery failed", 12), ("redelivery fee", 35), ("pay the clearance", 35), ("parcel stuck", 25), ("held at customs", 40),
    ("aapke naam se parcel", 35), ("aapke naam ka parcel", 35), ("parcel mein drugs", 45), ("parcel mein illegal", 45),
    ("customs duty bharni", 35), ("parcel rok", 30), ("parcel pakda gaya", 40),
    ("आपके नाम से पार्सल", 35), ("आपके नाम का पार्सल", 35), ("पार्सल में ड्रग्स", 45), ("कस्टम ड्यूटी", 30),
    ("पार्सल रोका", 30), ("पार्सल पकड़ा", 40), ("फेडेक्स", 20),
])
add_phrases("insurance_tax_scam", "Fake insurance / tax-refund call", [
    ("income tax refund", 35), ("tax refund", 25), ("refund approved", 25), ("gst refund", 30), ("policy has matured", 35),
    ("policy bonus", 25), ("maturity amount", 30), ("claim your bonus", 35), ("lic policy", 12), ("policy will lapse", 25),
    ("insurance claim", 8), ("surrender your policy", 25), ("irdai", 20), ("policy expire ho", 25),
    ("income tax refund aaya", 40), ("tax refund aapke", 35), ("policy ka bonus", 30), ("policy mature ho gayi", 40),
    ("maturity ka paisa", 30), ("policy lapse ho", 25), ("एलआईसी पॉलिसी", 12), ("इनकम टैक्स रिफंड", 35),
    ("पॉलिसी मैच्योर", 40), ("पॉलिसी का बोनस", 30), ("पॉलिसी लैप्स", 25), ("मैच्योरिटी का पैसा", 30),
])
add_phrases("romance_sextortion_scam", "Romance / blackmail scam", [
    ("video call and record", 40), ("your private video", 40), ("leak your photos", 45), ("viral your video", 45),
    ("pay or i will upload", 45), ("send me your photos", 25), ("i will post your", 25), ("your nude", 45), ("intimate video", 45),
    ("tumhari video viral", 45), ("video viral kar dunga", 45), ("photos viral", 40), ("tumhari private video", 40),
    ("तुम्हारी वीडियो वायरल", 45), ("वीडियो वायरल कर दूंगा", 45), ("वायरल कर दूंगा", 40), ("तुम्हारी प्राइवेट वीडियो", 40),
])

# ---------------------------------------------------------------------------------------------------------------
# Extra wording for the original categories (English, Hinglish, Hindi)
# ---------------------------------------------------------------------------------------------------------------
add_phrases("fake_kyc_update", "Fake KYC update", [
    ("kyc verification", 20), ("complete your kyc", 28), ("kyc is pending", 28), ("kyc pending", 28), ("re-kyc", 25), ("ekyc", 20),
    ("e-kyc", 20), ("kyc ke liye", 20), ("kyc complete karo", 30), ("kyc pending hai", 30), ("wallet kyc", 25),
    ("paytm kyc", 30), ("account deactivate", 25), ("account deactivated", 25), ("net banking blocked", 30),
    ("net banking band", 30), ("mobile banking band", 30), ("pan aadhaar link", 25), ("pan link", 18),
    ("आपका केवाईसी पेंडिंग", 30), ("केवाईसी पूरा", 25), ("केवाईसी करवाना", 25), ("खाता डीएक्टिवेट", 25), ("नेट बैंकिंग बंद", 30),
])
add_phrases("upi_refund_fraud", "UPI refund fraud", [
    ("cashback", 8), ("cashback of", 15), ("reward points", 12), ("redeem your points", 25), ("redeem points", 25),
    ("money has been debited", 15), ("received by mistake", 25), ("sent to your account by mistake", 35), ("return the amount", 20),
    ("amount was credited by mistake", 35), ("paytm cashback", 20), ("accept the collect", 35), ("approve the collect", 35),
    ("cashback mila", 20), ("reward points expire", 30), ("points redeem karo", 25), ("galti se aapke account mein", 35),
    ("paise wapas kar do", 25), ("rupay wapas", 20), ("रिवॉर्ड पॉइंट", 12), ("पॉइंट्स रिडीम", 25), ("कैशबैक", 8),
    ("गलती से आपके अकाउंट में", 35), ("पैसे लौटा दीजिए", 25), ("पैसे लौटा दो", 25),
])
add_phrases("fake_bank_officer", "Fake bank officer", [
    ("credit card limit", 12), ("increase your limit", 25), ("limit increase", 25), ("limit badhane", 25), ("card limit badh", 25),
    ("annual fee waiver", 25), ("fee waiver", 18), ("lifetime free card", 25), ("card activation", 18), ("card upgrade", 20),
    ("reward points expiring", 30), ("block your card", 25), ("unauthorized transaction", 25), ("unauthorised transaction", 25),
    ("verify the last four digits", 30), ("last four digits", 18), ("card ke piche", 25), ("back of your card", 30), ("three digit", 20),
    ("लिमिट बढ़ाने", 25), ("लिमिट बढ़ाना", 25), ("कार्ड के पीछे", 25), ("कार्ड अपग्रेड", 20), ("अनधिकृत लेन-देन", 25),
    ("अनधिकृत लेनदेन", 25), ("लाइफटाइम फ्री कार्ड", 25),
])
add_phrases("relative_impersonation", "Relative impersonation", [
    ("i lost my phone", 20), ("this is my new number", 30), ("save this number", 20), ("save my new number", 30), ("old number is not working", 30),
    ("i am arrested", 35), ("lawyer fee", 25), ("bail", 20), ("i need money urgently", 35), ("need money for hospital", 35),
    ("don't tell papa", 30), ("don't tell mummy", 30), ("mummy ko mat batana", 30), ("papa ko mat batana", 30),
    ("mera purana number band", 30), ("ye mera naya number", 30), ("number save kar lo", 20), ("paise bhej do abhi", 30),
    ("मेरा पुराना नंबर बंद", 30), ("ये मेरा नया नंबर", 30), ("नंबर सेव कर लो", 20), ("मम्मी को मत बताना", 30),
    ("पापा को मत बताना", 30), ("मुझे अभी पैसे चाहिए", 30),
])
add_phrases("fake_authority", "Government or police impersonation", [
    ("video call", 6), ("skype", 20), ("you are under digital", 40), ("mumbai crime branch", 30), ("cyber cell", 18), ("ed officer", 25),
    ("enforcement directorate", 30), ("supreme court order", 25), ("fir has been registered", 35), ("fir registered", 30),
    ("case has been registered against you", 40), ("freeze your account", 30), ("clear your name", 35), ("verify your innocence", 40),
    ("do not tell your family", 35), ("don't tell your family", 35), ("kisi ko mat batana", 15), ("tumhare khilaf fir", 40),
    ("aapke khilaf fir", 40), ("aapke khilaf case", 35), ("aapke naam par warrant", 40), ("jaanch poori hone tak", 30),
    ("आपके खिलाफ एफआईआर", 40), ("आपके खिलाफ केस", 35), ("आपके नाम पर वारंट", 40), ("जांच पूरी होने तक", 30), ("ईडी अधिकारी", 25),
    ("प्रवर्तन निदेशालय", 30), ("साइबर सेल", 18), ("वीडियो कॉल पर रहें", 35), ("परिवार को मत बताना", 35),
])
add_phrases("lottery_scam", "Lottery / prize scam", [
    ("you are the lucky winner", 35), ("lucky winner", 25), ("free gift", 20), ("gift voucher", 18), ("amazon voucher", 20),
    ("won a car", 40), ("won a bike", 40), ("won an iphone", 40), ("won 25 lakh", 40), ("gst charges to release", 40),
    ("pay to receive", 30), ("tax to release", 35), ("lucky customer", 25), ("jio lucky", 30), ("whatsapp lottery", 35),
    ("aapne gaadi jeeti", 40), ("aapko gift mila", 25), ("gift voucher mila", 25), ("lakh ka inaam", 35), ("inaam ki raashi", 30),
    ("आपने गाड़ी जीती", 40), ("आपको गिफ्ट मिला", 25), ("लाख का इनाम", 35), ("इनाम की राशि", 30), ("लकी विनर", 25),
])

# ---------------------------------------------------------------------------------------------------------------
# Request-shape patterns for the new categories (English / Hinglish / Hindi)
# ---------------------------------------------------------------------------------------------------------------
_NEW_PATTERNS = {
    "job_task_scam": [
        (r"(?:earn|kamao|kamaye|कमाएं|कमाओ|कमाइए).{0,25}(?:per day|daily|every day|roz|रोज|प्रतिदिन|₹|rs\.? ?\d+|\d+ ?(?:rupees|रुपये|rupay))", 28),
        (r"(?:like|rate|review|subscribe|लाइक|रेट).{0,25}(?:videos?|hotels?|products?|वीडियो|होटल).{0,40}(?:earn|paid|paise|commission|कमा|पैसे|income)", 35),
        (r"(?:deposit|invest|recharge|रिचार्ज|जमा).{0,25}(?:to start|to unlock|first task|pehle|पहले|शुरू).{0,25}(?:task|work|earning|कमाई|टास्क)", 35),
        (r"(?:no experience|bina experience|बिना अनुभव).{0,30}(?:needed|required|chahiye|चाहिए|job|जॉब)", 20),
        (r"(?:hr|recruiter|manager).{0,30}(?:telegram|whatsapp|टेलीग्राम|व्हाट्सएप)", 25),
    ],
    "investment_scam": [
        (r"(?:invest|nivesh|निवेश).{0,30}(?:and|aur|और|then|get|milega|मिलेगा).{0,25}(?:double|triple|guaranteed|daily|weekly|doguna|दोगुना|डबल|रिटर्न|return|profit|munafa|मुनाफा)", 40),
        (r"(?:\d+ ?%|percent|प्रतिशत).{0,20}(?:returns?|profit|interest|munafa|मुनाफा|रिटर्न).{0,20}(?:daily|weekly|monthly|guaranteed|every|roz|हर)", 35),
        (r"(?:join|add).{0,25}(?:trading|stock|crypto|investment|vip).{0,15}(?:group|channel|ग्रुप)", 30),
        (r"(?:ipo|allotment|app|platform).{0,30}(?:download|install|register|डाउनलोड|रजिस्टर).{0,30}(?:invest|deposit|trade|निवेश)", 30),
    ],
    "loan_app_scam": [
        (r"(?:loan|लोन).{0,30}(?:approved|sanctioned|pass|mil|मिल|अप्रूव).{0,30}(?:fee|charge|deposit|insurance|pay|फीस|शुल्क|जमा)", 40),
        (r"(?:pay|deposit|send|bhejo|jama|भेजो|जमा).{0,25}(?:fee|charge|insurance|gst|फीस).{0,25}(?:loan|release|disburse|लोन)", 40),
        (r"(?:loan|लोन).{0,25}(?:without|bina|बिना).{0,15}(?:document|cibil|salary|documents|डॉक्यूमेंट|सिबिल)", 30),
    ],
    "remote_access_scam": [
        (r"(?:download|install|open|डाउनलोड|इंस्टॉल).{0,25}(?:anydesk|teamviewer|quicksupport|rustdesk|remote|एनीडेस्क|टीमव्यूअर)", 40),
        (r"(?:tell|give|share|read|batao|bataiye|बताइए|बताओ).{0,25}(?:nine|9|ten|10|\d)[ -]?(?:digit|अंक).{0,15}(?:code|id|कोड|आईडी)", 40),
        (r"(?:allow|give|grant).{0,20}(?:access|permission|control).{0,25}(?:phone|computer|screen|device)", 30),
        (r"(?:fix|remove|clean|solve).{0,20}(?:virus|hack|problem|issue).{0,30}(?:remotely|through the app|app)", 25),
    ],
    "utility_disconnection_scam": [
        (r"(?:electricity|power|bijli|बिजली|sim|सिम|gas|connection|कनेक्शन).{0,40}(?:will be|ho jayega|jayega|जाएगा|हो जाएगा|disconnected|cut|blocked|deactivated|kat|कट).{0,25}(?:tonight|today|9|nine|within|aaj|आज|raat|रात|hours|ghante|घंटे)", 40),
        (r"(?:call|contact|message|sms).{0,15}(?:this number|the officer|our officer|immediately|turant|तुरंत).{0,30}(?:bill|connection|sim|बिल|कनेक्शन)", 25),
        (r"(?:bill|बिल).{0,30}(?:not updated|pending|update nahi|अपडेट नहीं|बकाया).{0,40}(?:disconnect|cut|kat|कट|band|बंद)", 35),
    ],
    "courier_customs_scam": [
        (r"(?:parcel|package|courier|पार्सल|कूरियर).{0,40}(?:customs|mumbai|airport|police|narcotics|cbi|कस्टम|एयरपोर्ट|पुलिस)", 30),
        (r"(?:pay|deposit|bharni|bharo|भरनी|भरो).{0,25}(?:duty|clearance|fee|charges|शुल्क|ड्यूटी).{0,25}(?:release|parcel|clear|पार्सल|छुड़ाने)", 40),
        (r"(?:your|aapke|आपके).{0,15}(?:name|naam|नाम).{0,25}(?:parcel|package|courier|पार्सल).{0,40}(?:drugs|passport|fake|illegal|suspicious|ड्रग्स|पासपोर्ट|नकली)", 40),
    ],
    "insurance_tax_scam": [
        (r"(?:refund|bonus|maturity|मैच्योरिटी|रिफंड|बोनस).{0,30}(?:approved|credited|ready|pending|release|aapke|आपके|क्रेडिट).{0,30}(?:pay|fee|verify|details|otp|बैंक|bank|खाता)", 30),
        (r"(?:to receive|to release|to claim|pane ke liye|पाने के लिए).{0,25}(?:refund|bonus|amount|maturity|रिफंड).{0,25}(?:pay|deposit|fee|jama|जमा|फीस)", 40),
    ],
    "romance_sextortion_scam": [
        (r"(?:video|photos?|pics?|screenshot|वीडियो|फोटो).{0,30}(?:viral|leak|upload|post|share with|वायरल|लीक|भेज दूंगा).{0,40}(?:unless|if you don|pay|paise|पैसे|नहीं दिए|वरना)", 45),
        (r"(?:pay|send|bhej|भेज).{0,25}(?:or|otherwise|warna|वरना).{0,30}(?:viral|leak|upload|post|वायरल|लीक)", 45),
    ],
    "fake_authority": [
        (r"(?:fir|case|warrant|एफआईआर|केस|वारंट).{0,30}(?:registered|filed|against you|your name|darj|दर्ज|आपके|तुम्हारे).{0,40}(?:pay|transfer|settle|verify|clear|account|जमा|पैसे|खाते|ट्रांसफर)", 40),
        (r"(?:don't|do not|mat|न|मत).{0,12}(?:tell|inform|batana|बताना|बताओ).{0,20}(?:family|parents|lawyer|anyone|ghar|परिवार|वकील|किसी)", 20),
        (r"(?:stay|remain|rahiye|rahna|रहिए|रहना).{0,15}(?:on (?:the )?(?:video )?call|on the line|line par|कॉल पर|लाइन पर)", 25),
    ],
    "fake_bank_officer": [
        (r"(?:credit card|card).{0,30}(?:limit|upgrade|fee waiver|reward|rewards|लिमिट).{0,40}(?:otp|cvv|card number|expiry|कार्ड नंबर|ओटीपी|सीवीवी|verify)", 40),
        (r"(?:last|first)[ -]?(?:four|4|six|6).{0,15}digits?.{0,25}(?:card|debit|credit|कार्ड)", 25),
    ],
}
for _cat, _pats in _NEW_PATTERNS.items():  # extend, never replace: the originals are tuned
    CATEGORY_PATTERNS.setdefault(_cat, []).extend(_pats)

SIGNAL_PATTERNS["credential"] += [
    (r"(?:nine|9|ten|10)[ -]?(?:digit|अंक).{0,15}(?:code|id|कोड|आईडी)", 30),
    (r"(?:aadhaar|aadhar|pan|आधार|पैन).{0,20}(?:number|नंबर|card|कार्ड).{0,20}(?:batao|bataiye|bata|share|send|bhejo|बताइए|बताओ|भेजो)", 30),
    (r"(?:selfie|photo|फोटो|सेल्फी).{0,20}(?:with|holding|and|aur).{0,20}(?:aadhaar|aadhar|pan|id|आधार)", 25),
]
SIGNAL_PATTERNS["payment_request"] += [
    (r"(?:pay|deposit|pay the|send the|bharo|bharni|भरो|भरनी).{0,15}(?:processing|registration|clearance|security|refundable|refundable security|handling|gst|insurance|customs).{0,10}(?:fee|fees|charge|charges|deposit|duty|शुल्क|फीस)", 30),
    (r"(?:refundable|वापस मिलने वाला|वापस होने वाला).{0,15}(?:deposit|amount|security|डिपॉजिट|राशि)", 25),
    (r"(?:buy|purchase|kharido|खरीदो|खरीदें).{0,15}(?:gift cards?|google play|itunes|vouchers?|गिफ्ट कार्ड|वाउचर)", 40),
    (r"(?:send|share|bhejo|बताओ|बताइए).{0,20}(?:gift card|voucher|redeem code|गिफ्ट कार्ड|कोड)", 30),
]
SIGNAL_PATTERNS["threat"] += [
    (r"(?:will be|ho jayega|jayega|जाएगा).{0,8}(?:disconnected|deactivated|cut|terminated|seized|confiscated|कट|बंद)", 18),
    (r"(?:legal|कानूनी|police|पुलिस|court|कोर्ट).{0,15}(?:action|notice|case|कार्रवाई|नोटिस).{0,20}(?:against you|aapke|आपके|will be|होगी|होगा)", 20),
    (r"(?:viral|leak|expose|वायरल|लीक).{0,15}(?:video|photos?|pictures|वीडियो|फोटो)", 30),
]
SIGNAL_PATTERNS["urgency"] += [
    (r"(?:within|next|in|के अंदर|अगले)\s*(?:the next )?(?:\d+|one|two|three|एक|दो|तीन|आधे)\s*(?:hours?|minutes?|mins?|घंटे|मिनट)", 12),
    (r"(?:offer|deal|link|ऑफर|लिंक).{0,15}(?:expires?|valid only|ends|एक्सपायर|सिर्फ)", 10),
    (r"(?:last chance|limited (?:time|slots|seats)|आखिरी मौका|सीमित)", 10),
]
SIGNAL_PATTERNS["secrecy"] += [
    (r"(?:do not|don'?t|never|मत|न).{0,10}(?:tell|inform|share|bank|branch|batana|बताना).{0,25}(?:bank|branch|staff|employees|बैंक|ब्रांच)", 20),
    (r"(?:confidential|गोपनीय|secret).{0,20}(?:matter|case|investigation|मामला|जांच)", 18),
]

# Extra "this is a genuine warning" context so the wider rules do not flag awareness messages.
DAMPENERS += [
    ("never ask for your otp", 40), ("will never ask", 35), ("never asks for", 35), ("beware of", 20), ("be aware of", 20),
    ("report fraud", 25), ("cyber crime helpline", 25), ("1930", 20), ("sanchar saathi", 25), ("this is a scam", 25),
    ("कभी नहीं मांगते", 35), ("कभी भी नहीं मांगता", 35), ("सावधान रहें", 20), ("साइबर क्राइम हेल्पलाइन", 25), ("धोखाधड़ी की शिकायत", 25),
    ("kabhi nahi maangta", 35), ("kabhi nahi maangte", 35), ("savdhan rahein", 20),
]
DAMPENER_PATTERNS += [
    (r"(?:i|maine|मैंने).{0,15}(?:paid|pay kiya|bhar diya|भर दिया|checked|dekha|देखा).{0,25}(?:bill|बिल)", 20),
    (r"(?:this is a|ye ek|यह एक).{0,10}(?:reminder|appointment|confirmation|रिमाइंडर|अपॉइंटमेंट).{0,25}(?:dentist|doctor|clinic|class|school|डॉक्टर|क्लिनिक)", 25),
]


# ---------------------------------------------------------------------------------------------------------------
# Second pass, from public reports of how these calls actually run (news and advisories read 2026-11-01):
# digital-arrest call sequences (TRAI claim -> "number linked to illegal activity" -> statement over a WhatsApp/Skype video
# call -> Aadhaar details -> "how many bank accounts / do you use UPI" -> transfer to a "safe account", with a promised
# refund and clearance certificate); APK-file lures (wedding card, e-challan, "life certificate"); pensioner and
# KYC-executive calls; prepaid-task job scams ("send 1000, get 1300"); mule recruitment; and the US-style
# government, tech-support, gift-card and grandparent scripts that also reach Indian numbers.
# ---------------------------------------------------------------------------------------------------------------
add_phrases("fake_authority", "Government or police impersonation", [
    ("linked to illegal activity", 40), ("used for illegal activities", 40), ("number will be blocked within", 35),
    ("mobile number is linked", 30), ("whatsapp video call", 12), ("give your statement", 25), ("record your statement", 25),
    ("how many bank accounts", 40), ("do you use upi", 30), ("do you use net banking", 30), ("senior officer will", 25),
    ("until the verification is complete", 35), ("will be returned after verification", 40), ("clearance certificate", 35),
    ("funds will be returned", 35), ("your money will be refunded after", 40), ("headquarters", 8), ("your aadhaar is linked to", 35),
    ("your aadhaar has been used", 35), ("aadhaar number to verify", 25), ("mumbai police", 15), ("delhi police", 12),
    ("cyber crime branch", 25), ("trai officer", 30), ("trai se bol", 35), ("mobile number illegal", 35),
    ("aapke number se illegal", 40), ("aapka number band kar diya jayega", 40), ("kitne bank account hain", 40),
    ("upi use karte hain", 25), ("paise rbi ke account mein", 40), ("jaanch ke baad wapas", 40),
    ("आपका नंबर अवैध गतिविधि", 40), ("आपके नंबर से अवैध", 40), ("ट्राई से बोल", 35), ("कितने बैंक अकाउंट", 40),
    ("यूपीआई इस्तेमाल करते", 25), ("जांच के बाद वापस", 40), ("आरबीआई के खाते में", 40), ("वीडियो कॉल पर बयान", 30),
    ("आपका आधार नंबर अवैध", 35), ("आपके आधार से", 15), ("आपका सिम अवैध", 40),
])
add_phrases("remote_access_scam", "Remote-access / tech-support scam", [
    ("apk file", 35), (".apk", 35), ("download the apk", 45), ("install this apk", 45), ("install the file", 25),
    ("e-challan", 18), ("echallan", 18), ("traffic challan", 15), ("pending challan", 25), ("rto challan", 25),
    ("wedding invitation", 12), ("shaadi ka card", 12), ("invitation card app", 30), ("apk bheji", 40), ("apk file bhej", 40),
    ("apk download karo", 45), ("file install karo", 30), ("link se app install", 35),
    ("एपीके फाइल", 40), ("एपीके डाउनलोड", 45), ("चालान", 12), ("ई-चालान", 18), ("फाइल इंस्टॉल करें", 30), ("फाइल इंस्टॉल करो", 30),
    ("शादी का कार्ड", 12), ("इनविटेशन ऐप", 30),
])
add_phrases("insurance_tax_scam", "Fake insurance / tax-refund call", [
    ("jeevan pramaan", 30), ("jeevan praman", 30), ("life certificate", 25), ("pension department", 25), ("ppo number", 35),
    ("date of retirement", 18), ("pension will stop", 40), ("pension band ho", 40), ("pension rok", 35), ("life certificate update", 40),
    ("पेंशन बंद हो", 40), ("पेंशन रुक", 35), ("लाइफ सर्टिफिकेट", 25), ("जीवन प्रमाण", 30), ("पीपीओ नंबर", 35), ("पेंशन विभाग", 25),
    ("social security number", 30), ("social security has been suspended", 45), ("your social security", 25), ("medicare card", 25),
    ("irs", 12), ("internal revenue", 25), ("back taxes", 35), ("tax lien", 35), ("owe back taxes", 40),
])
add_phrases("job_task_scam", "Fake job / task scam", [
    ("prepaid task", 45), ("prepaid tasks", 45), ("advance task", 30), ("merchant task", 35), ("send 1000", 25), ("you will receive 1300", 45),
    ("earn commission", 20), ("submit the screenshot", 25), ("screenshot of the task", 30), ("unlock the next task", 40), ("withdraw your earnings", 30),
    ("your salary will be", 8), ("hiring for", 8), ("simple online tasks", 35), ("no interview", 25), ("work from mobile", 20),
    ("prepaid task karo", 45), ("pehle paise bhejo", 35), ("screenshot bhejo", 25), ("agla task unlock", 40), ("commission milega", 25),
    ("प्रीपेड टास्क", 45), ("अगला टास्क", 25), ("स्क्रीनशॉट भेजो", 25), ("कमीशन मिलेगा", 25), ("बिना इंटरव्यू", 25), ("मोबाइल से कमाएं", 22),
])
add_phrases("money_mule_scam", "Money-mule recruitment", [
    ("rent your bank account", 40), ("lend your bank account", 45), ("lend your account", 40), ("use your account for", 25),
    ("commission for your account", 40), ("commission of", 12), ("use your account for transfers", 35), ("receive money in your account", 30),
    ("account rent par", 40), ("apna account do", 35), ("account kiraye par", 40), ("apna account kiraye", 40),
    ("अकाउंट किराए पर", 40), ("अपना अकाउंट दो", 35), ("अपना खाता किराए", 40),
])
add_phrases("relative_impersonation", "Relative impersonation", [
    ("gift card", 20), ("gift cards", 20), ("google play card", 30), ("itunes card", 30), ("bitcoin atm", 20), ("wire the money", 25),
    ("do you know who this is", 40), ("guess who", 30), ("i'm in jail", 40), ("i need bail", 45), ("bail money", 40), ("don't tell mom", 30),
    ("don't tell my parents", 35), ("please don't tell anyone", 30),
])
add_phrases("remote_access_scam", "Remote-access / tech-support scam", [
    ("lost iphone", 18), ("your lost iphone", 30), ("iphone has been found", 40),
])
add_phrases("fake_kyc_update", "Fake KYC update", [
    ("kyc executive", 35), ("call this number to update", 40), ("kyc documents are incomplete", 35), ("kyc documents are pending", 35),
    ("sim kyc", 25), ("jio kyc", 25), ("airtel kyc", 25), ("bsnl kyc", 25), ("kyc suspension", 30), ("kyc expired", 30),
    ("pan will be deactivated", 40), ("pan card will be blocked", 40), ("aadhaar will be deactivated", 40), ("aadhaar will be blocked", 40),
    ("pan inoperative", 35), ("pan aadhaar not linked", 35), ("kyc executive se baat", 35), ("is number par call karo", 30),
    ("पैन निष्क्रिय", 35), ("पैन ब्लॉक हो", 40), ("आधार ब्लॉक हो", 40), ("केवाईसी एग्जीक्यूटिव", 35), ("इस नंबर पर कॉल करें", 30),
])
add_phrases("fake_bank_officer", "Fake bank officer", [
    ("verify certain transactions", 40), ("verify some transactions", 40), ("verify a transaction", 30), ("did you make a transaction", 30),
    ("transaction of rs", 15), ("transaction of ₹", 15), ("press 1", 22), ("press one", 22), ("press 9", 22), ("toll free number", 8),
    ("customer care executive", 25), ("customer care number", 15), ("customer care", 8), ("aapke account se transaction", 30),
    ("transaction confirm karne", 30), ("1 dabaiye", 25), ("1 dabayen", 25), ("एक दबाएं", 25), ("1 दबाएं", 25), ("1 दबाइए", 25),
    ("आपके खाते से ट्रांजैक्शन", 30), ("ट्रांजैक्शन कन्फर्म", 30), ("कस्टमर केयर एग्जीक्यूटिव", 25),
])

CATEGORY_PATTERNS["fake_authority"] += [
    (r"(?:number|sim|mobile|नंबर|सिम).{0,30}(?:linked|used|involved|connected|जुड़ा|इस्तेमाल|शामिल).{0,25}(?:illegal|crime|fraud|money laundering|harass|अवैध|अपराध|धोखाधड़ी)", 40),
    (r"(?:will be|ho jayega|जाएगा|होगा).{0,8}blocked.{0,15}(?:within|in|next|के अंदर|ghante|hours?)|(?:within|next).{0,10}(?:2|two|24|\d+) hours.{0,25}(?:block|disconnect|suspend)", 30),
    (r"(?:how many|kitne|कितने).{0,15}(?:bank )?(?:accounts?|खाते|अकाउंट).{0,25}(?:do you have|hain|हैं|aapke|आपके|you have)", 40),
    (r"(?:money|funds|paise|पैसे|रकम).{0,40}(?:returned|refunded|wapas|वापस).{0,25}(?:after|once|baad|बाद).{0,20}(?:verification|investigation|inquiry|jaanch|जांच|सत्यापन)", 40),
    (r"(?:send|share|upload|show|bhejo|dikhao|भेजो|दिखाओ).{0,15}(?:your )?(?:aadhaar|aadhar|id proof|आधार).{0,25}(?:to verify|for verification|verify|सत्यापन|verification)", 25),
    (r"(?:pay|transfer|deposit).{0,20}(?:bail|fine|penalty|settlement|security deposit).{0,20}(?:avoid|to avoid|otherwise|or you)", 40),
]
CATEGORY_PATTERNS["remote_access_scam"] += [
    (r"(?:download|install|open|click).{0,25}(?:the |this )?(?:apk|file|app).{0,40}(?:sent|send|i sent|whatsapp|link|bheji|भेजी|चालान|challan|invitation|कार्ड)", 40),
    (r"(?:challan|चालान).{0,40}(?:apk|download|install|app|डाउनलोड|ऐप)", 40),
]
CATEGORY_PATTERNS["insurance_tax_scam"] += [
    (r"(?:pension|पेंशन).{0,40}(?:will stop|stopped|suspend|band|बंद|रुक).{0,40}(?:unless|until|if|verify|update|otp|जब तक|अपडेट)", 40),
    (r"(?:life certificate|jeevan pram[a]?an|जीवन प्रमाण|लाइफ सर्टिफिकेट).{0,40}(?:otp|link|app|video call|ऐप|लिंक|ओटीपी|वीडियो कॉल)", 40),
    (r"(?:your|aapka|आपका).{0,10}(?:social security|ssn).{0,30}(?:suspend|compromis|blocked|linked to|used)", 45),
]
CATEGORY_PATTERNS["job_task_scam"] += [
    (r"(?:send|pay|deposit|bhejo|भेजो).{0,15}(?:₹|rs\.?|rupees|\$)?\s?\d{3,5}.{0,30}(?:receive|get|milega|मिलेगा|return|back).{0,15}(?:₹|rs\.?|rupees|\$)?\s?\d{3,6}", 45),
    (r"(?:pay|deposit|bhar|भरो).{0,20}(?:first|pehle|पहले).{0,30}(?:then|baad|बाद).{0,20}(?:earn|task|salary|kamao|कमा)", 35),
]
_GIFT = (r"(?:buy|purchase|get|kharid|खरीद).{0,20}(?:gift ?cards?|google play|itunes|steam|apple card|गिफ्ट कार्ड).{0,40}(?:read|send|scratch|share|code|कोड|बताओ|भेजो|number)", 45)
CATEGORY_PATTERNS["relative_impersonation"] += [
    _GIFT,
    (r"(?:hi|hello|hey)\s*(?:grandma|grandpa|nani|nana|dadi|dada|दादी|नानी)", 15),
    (r"(?:i|main|मैं).{0,12}(?:am in|am at|hoon|हूं).{0,15}(?:jail|police station|custody|lockup|जेल|थाने|हवालात).{0,40}(?:bail|lawyer|money|paise|पैसे|वकील|जमानत)", 45),
]
CATEGORY_PATTERNS["fake_authority"].append(_GIFT)
CATEGORY_PATTERNS.setdefault("money_mule_scam", []).append(
    (r"(?:your|aapka|आपका|apna|अपना).{0,15}(?:account|bank account|खाता).{0,25}(?:rent|lend|kiraye|किराए|use|इस्तेमाल).{0,25}(?:commission|per month|paisa|कमीशन|हर महीने)|(?:lend|rent|kiraye).{0,12}(?:your|apna).{0,12}(?:bank )?(?:account|खाता).{0,40}(?:commission|per month|कमीशन)", 40))
SIGNAL_PATTERNS["credential"] += [
    (r"(?:otp|code|कोड|ओटीपी).{0,25}(?:to verify|for verification|to confirm|verify karne|वेरिफाई|सत्यापन)", 25),
    (r"(?:ppo|pension|पीपीओ|पेंशन).{0,12}(?:number|no\.?|नंबर).{0,20}(?:batao|bataiye|share|tell|give|बताइए|बताओ)", 30),
    (r"(?:date of birth|dob|जन्म ?तिथि|janam ?tithi).{0,25}(?:and|aur|और).{0,20}(?:aadhaar|pan|account|आधार|पैन)", 25),
]
SIGNAL_PATTERNS["secrecy"] += [
    (r"(?:don'?t|do not|never|mat|मत).{0,12}(?:hang up|disconnect|cut the call|leave the (?:room|house)|leave the video|call mat|कॉल मत|कमरा न छोड़)", 25),
    (r"(?:do not|don'?t|mat|मत).{0,10}(?:contact|call|talk to|speak to|baat|बात).{0,15}(?:anyone|family|lawyer|bank|kisi se|किसी से|परिवार|वकील)", 30),
    (r"(?:this is|ye|यह).{0,8}(?:a )?(?:secret|confidential|gopniya|गोपनीय|top secret|national security)", 20),
]
SIGNAL_PATTERNS["threat"] += [
    (r"(?:your|aapka|आपका).{0,15}(?:number|sim|account|aadhaar|pan|नंबर|खाता|आधार|पैन).{0,20}(?:will be|ho jayega|jayega|जाएगा|होगा).{0,12}(?:blocked|deactivated|cancelled|seized|frozen|band|बंद|ब्लॉक)", 25),
    (r"(?:warrant|fir|एफआईआर|वारंट).{0,25}(?:issued|registered|jaari|जारी|दर्ज)", 25),
    (r"(?:otherwise|or else|warna|वरना|nahi to|नहीं तो).{0,25}(?:arrest|jail|case|fine|giraftar|गिरफ्तार|जेल|केस)", 30),
]
SIGNAL_PATTERNS["urgency"] += [
    (r"(?:right now|abhi|अभी|immediately|turant|तुरंत).{0,20}(?:or|warna|वरना|otherwise|nahi to|नहीं तो)", 12),
    (r"(?:before|by|se pehle|से पहले).{0,12}(?:midnight|tonight|5 ?pm|end of (?:the )?day|aaj raat|आज रात|शाम)", 12),
]
SIGNAL_PATTERNS["payment_request"] += [
    (r"(?:safe|secure|rbi|supervised|temporary|सुरक्षित|आरबीआई|अस्थायी).{0,12}(?:account|wallet|upi|खाते|अकाउंट)", 35),
    (r"(?:transfer|send|move|deposit|ट्रांसफर|भेज|जमा).{0,20}(?:all|entire|whole|sab|saara|सारा|सारे|पूरा).{0,20}(?:money|amount|savings|funds|paise|पैसे|रकम|बचत)", 40),
    (r"(?:bitcoin|crypto|usdt|btc|बिटकॉइन|क्रिप्टो).{0,25}(?:atm|wallet|address|deposit|transfer|pay|वॉलेट|जमा)", 35),
    (r"(?:western union|moneygram|wire transfer|zelle|cash ?app|वायर ट्रांसफर)", 30),
]
COMBOS_EXTRA = None  # combos already cover urgency+credential, threat+credential, secrecy+payment, urgency+payment
DAMPENERS += [
    ("report it on 1930", 25), ("call 1930", 25), ("visit the nearest branch", 20), ("official website", 8), ("official app", 8),
    ("never send apk", 30), ("never download apk", 30), ("do not install apk", 30), ("do not click on links", 25), ("don't click on links", 25),
    ("एपीके फाइल कभी", 30), ("लिंक पर क्लिक न करें", 25), ("आधिकारिक वेबसाइट", 8), ("निकटतम शाखा", 20),
]
