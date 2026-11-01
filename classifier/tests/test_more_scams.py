"""Scam types added from public reports (news, police and bank advisories, read 2026-11-01).

These calls were written by the same author who wrote the rules (an AI assistant), from those reports, so they are an
in-sample regression check, NOT a measure of accuracy on real calls. The safe calls include awareness messages and
ordinary calls that share vocabulary with scams (bills, parcels, pensions, invitations, investments).
"""
import pytest

from classifier import classify_transcript

SCAM = {
"trai_en":"Hello, I am calling from TRAI. Your mobile number is linked to illegal activity and will be blocked within two hours. You must give your statement on a WhatsApp video call. Do not disconnect and do not tell anyone, this is confidential.",
"arrest_en2":"This is Mumbai cyber crime branch. A case has been registered against you. How many bank accounts do you have? Do you use UPI? Transfer your money to the RBI safe account for verification, it will be returned after the investigation with a clearance certificate.",
"trai_hi":"मैं ट्राई से बोल रहा हूं। आपके नंबर से अवैध गतिविधि हो रही है और आपका सिम ब्लॉक हो जाएगा। कृपया वीडियो कॉल पर बयान दीजिए और कॉल मत काटिए।",
"apk_en":"Sir your traffic challan is pending. Please download the APK file I sent on WhatsApp and install it to pay the challan.",
"apk_hinglish":"Sir aapka e-challan pending hai, main ek apk file bhej raha hoon, usse install karo aur challan bharo.",
"pension_en":"I am calling from the pension department. Your pension will stop unless you update your life certificate. Please tell me your PPO number and the OTP you will receive.",
"pension_hi":"मैं पेंशन विभाग से बोल रहा हूं। आपकी पेंशन बंद हो जाएगी जब तक आप लाइफ सर्टिफिकेट अपडेट नहीं करते। अपना पीपीओ नंबर और ओटीपी बताइए।",
"job_en":"Hi, we have a part time job. Like YouTube videos and earn 5000 per day. Join our Telegram group. You first send 1000 and you will receive 1300 for the prepaid task.",
"job_hinglish":"Ghar baithe kamao, roz 3000 rupay. Telegram group join karo, pehle prepaid task karo aur commission milega.",
"invest_en":"Join our VIP trading group. Guaranteed returns of 5 percent daily, risk free. Invest today, minimum investment 10000, double your money in a month.",
"invest_hi":"हमारे ट्रेडिंग ग्रुप से जुड़ें, पक्का मुनाफा, पैसे डबल हो जाएंगे। आज ही निवेश करें।",
"loan_en":"Your pre-approved loan of five lakh is approved, no documents required. Please pay the processing fee first, then the loan will be released.",
"loan_hi":"आपका तुरंत लोन अप्रूव हो गया है, बिना डॉक्यूमेंट। पहले प्रोसेसिंग फीस जमा करें फिर लोन मिलेगा।",
"anydesk_en":"This is Microsoft support. Your computer has a virus. Please download AnyDesk and tell me the nine digit code so I can fix it remotely.",
"anydesk_hinglish":"Sir aapke computer mein virus hai, anydesk download karo aur 9 digit code batao.",
"elec_en":"Your electricity bill is not updated and power will be disconnected tonight at 9:30. Call the officer on this number immediately.",
"elec_hinglish":"Aapka bijli ka bill update nahi hai, aaj raat bijli ka connection kat jayega. Turant is number par call karo.",
"sim_hi":"आपका सिम बंद हो जाएगा, केवाईसी अपडेट नहीं है। इस नंबर पर कॉल करें, केवाईसी एग्जीक्यूटिव से बात करें।",
"fedex_en":"This is FedEx. A parcel in your name contains illegal drugs and a passport. It is held at customs. Please pay the customs clearance fee to release it.",
"fedex_hi":"आपके नाम से पार्सल में ड्रग्स मिले हैं, कस्टम ड्यूटी भरनी होगी वरना केस दर्ज होगा।",
"tax_en":"Your income tax refund is approved. To receive the refund, verify your bank details and share the OTP.",
"sextort_en":"I have your private video. Pay me 20000 or I will leak it and viral your video to all your contacts.",
"grandma_en":"Hi Grandma, do you know who this is? I'm in jail and I need bail money. Please don't tell mom. Buy gift cards and read me the codes.",
"bank_press1":"This is customer care executive. We detected unauthorized transaction of Rs 49,000 on your credit card. Press 1 to block it, or tell me the card number and OTP to verify certain transactions.",
"irs_en":"This is the IRS. You owe back taxes and a warrant for your arrest has been issued. Pay today with gift cards or a bitcoin ATM, and do not hang up.",
"mule_en":"Lend your bank account to us for a few days, commission of 10000 per month, we will just use your account for transfers.",
}
SAFE = {
"s1":"Hi, this is your dentist's clinic reminding you about your appointment tomorrow at 4 PM. Please call us if you need to reschedule.",
"s2":"Your electricity bill for October has been paid. Thank you. Your next reading is due on the fifth.",
"s3":"Hello, I'm calling from the school. The parent teacher meeting is on Saturday at ten in the morning.",
"s4":"Your Amazon package will be delivered today between 2 and 6 PM. Please keep your phone handy for the delivery person.",
"s5":"Bank advisory: never share your OTP, PIN or CVV with anyone. Banks never ask for it. Report fraud on 1930.",
"s6":"Hi mom, I reached the station. I will call you in the evening after the meeting. Can you send me the recipe for dal?",
"s7":"We are hiring for a software engineer position. Please send your resume and we will schedule an interview next week.",
"s8":"Your loan EMI of 12000 rupees is due on the fifth. You can pay through the official app or visit the nearest branch.",
"s9":"The doctor said the report is normal. Your tax filing is done and the refund will come to your account in a few weeks, no action is required.",
"s10":"Aapka order kal subah tak deliver ho jayega. Delivery boy aapko call karega.",
"s11":"नमस्ते, मैं स्कूल से बोल रहा हूं। कल बच्चों की छुट्टी रहेगी।",
"s12":"सावधान रहें, कोई भी बैंक आपसे ओटीपी कभी नहीं मांगता। साइबर क्राइम हेल्पलाइन 1930 पर शिकायत करें।",
"s13":"Hey, can you send me the invitation for the wedding? I want to know the venue and time. Let me know if you will come.",
"s14":"My pension came in this month and my life certificate was submitted at the branch last week. Everything is fine.",
"s15":"I invested in a mutual fund through my bank's official app last year, the returns are not guaranteed but it is doing okay.",
"s16":"Your internet connection will be upgraded tomorrow between 10 and 12. No action is needed from your side.",
"s17":"Bhai kal shaam ko cricket khelne chalenge? Main apna naya bat laaunga.",
"s18":"The police officer helped me file a report about my lost wallet at the station. I went there in person and collected the copy.",
}

EXPECTED = {'trai_en': 'fake_authority', 'arrest_en2': 'fake_authority', 'trai_hi': 'fake_authority', 'apk_en': 'remote_access_scam', 'apk_hinglish': 'remote_access_scam', 'pension_en': 'insurance_tax_scam', 'pension_hi': 'insurance_tax_scam', 'job_en': 'job_task_scam', 'job_hinglish': 'job_task_scam', 'invest_en': 'investment_scam', 'invest_hi': 'investment_scam', 'loan_en': 'loan_app_scam', 'loan_hi': 'loan_app_scam', 'anydesk_en': 'remote_access_scam', 'anydesk_hinglish': 'remote_access_scam', 'elec_en': 'utility_disconnection_scam', 'elec_hinglish': 'utility_disconnection_scam', 'sim_hi': 'fake_kyc_update', 'fedex_en': 'courier_customs_scam', 'fedex_hi': 'courier_customs_scam', 'tax_en': 'insurance_tax_scam', 'sextort_en': 'romance_sextortion_scam', 'grandma_en': 'relative_impersonation', 'bank_press1': 'fake_bank_officer', 'irs_en': 'insurance_tax_scam', 'mule_en': 'money_mule_scam'}
# --- Third pass: shapes found by scoring the independent BothBosu/scam-dialogue corpus (own paraphrases, not its text) ---
SCAM.update({
    "refund_bank_ack": "Hello, this is the refund department of an online store. You were overcharged by two hundred dollars and we want to refund it. To process the refund I need your bank account number and routing number.",
    "support_infected": "Hi, I'm calling from Windows technical support. Your computer has been infected with malware. I will need to remote into your computer to fix it, please download this software.",
})
EXPECTED.update({"refund_bank_ack": "fake_refund_scam", "support_infected": "remote_access_scam"})
SAFE.update({
    "promo_price_tax": "Hi, I'm calling about the new laptop you ordered. It is five hundred ninety nine dollars plus tax and will arrive by 5 pm today. Please confirm you will be home.",
    "promo_never_ask": "We are offering a limited time discount on our software. We would never ask you to provide your bank account or social security number over the phone. Call us back whenever you like.",
})



@pytest.mark.parametrize("key", sorted(SCAM))
def test_new_scam_types_detected(key):
    r = classify_transcript(SCAM[key])
    assert r["risk_score"] >= 60, r
    assert r["category"] == EXPECTED[key], r


@pytest.mark.parametrize("key", sorted(SAFE))
def test_ordinary_calls_not_flagged(key):
    r = classify_transcript(SAFE[key])
    assert r["risk_score"] < 30, r

