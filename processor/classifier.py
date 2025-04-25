# processor/classifier.py

import re

# === Edit these lists as you review your mailbox and preferences ===

PROMOTION_KEYWORDS = [
    "welcome", "invited", "just scheduled", "goodbye", "hello", "deal", "promo", "discount", "sale",
    "offer", "last call", "now free", "free", "upgrade", "rate", "activate",
    "scheduled", "virtual", "gathering", "summit", "workshop",
    "webinar", "newsletter", "digest", "curated", "tutorial", "platform", "feature", "discover",
    "launch", "build", "introducing", "pro trial", "trial starts", "trial receipt", "trial ends", "recap", "program",
    "demo", "event", "conference", "skills", "level up", "get better results", "training", "learn", "how to",
    "access your", "your experience", "quick insights", "eye-candy", "marketing playbook", "quick shoulder warm",
    "explore", "refill", "adventure begins", "let's get your", "shopify ceo",
    "celebrate", "enjoy", "try", "pro", "mandatory", "your first", "download", "fast ai chat", "beat", "llama",
    "chatbot", "screenless phone", "wild idea", "wonky hands", "midjourney", "altman x", "ai search",
    "microsoft launches", "controversial feature", "march's hottest", "hottest", "datadriven", "AI tools",
    "our ai", "playbook", "canva adds", "becomes easier", "might need id", "shopify ceo",
    "google i/o", "join us online", "register", "network", "skills network",
]
PROMOTION_SENDERS = [
    "linkedin", "promo", "meetup", "labs", "openrouter", "aicamp", "topaz", "docsbot", "botpress",
    "futurepedia", "future blueprint", "runpod", "vast", "crew", "latenode", "mindstream", "botpenguin", "tangerine",
    "notebooklm", "rasa", "novita", "ai/ml api team", "plutoai", "make", "dust", "community", "reid", "credit score increa",
    "google developer", "uopeople", "fing limited", "sagar sharma", "rahul"
]

IMPORTANT_KEYWORDS = [
    "important", "update", "critical", "alert", "action needed", "recovery code", "two-factor", "password", "reset",
    "data accessed", "account", "backed up file", "failed", "successful", "support", "receipt", "download",
    "transaction", "payment", "unsuccessful", "fatura vence", "pagamento confirmado", "balance low", "inscrição",
    "membership", "renewal", "renew", "license", "trial receipt", "trial ends", "program membership", "accredited",
    "informações", "acordo", "vencimento", "prescription", "refill", "declaração", "atendimento", "copilot", "[luki]",
    "conta pra gente", "added to your account", "accessed from new ip", "password reset", "refill your prescription",
    "score increased", "download your two-factor", "welcome to your pro", "msonlineservicesteam",
]
IMPORTANT_SENDERS = [
    "github", "nubank", "serasa", "idrive", "simplefin", "atendimento", "fing", "msonlineservicesteam",
    "uopeople advising", "vast.ai", "dust team", "plutoai", "anvil support", "credit score increa",
    "google developer", "rahul"
]


def classify_email(email_obj):
    """Classifies an email_obj as 'important', 'junk', or 'other' based on sender/subject keywords."""
    subj = (email_obj.get("subject") or "").lower()
    sender = (email_obj.get("from") or "").lower()

    # Promotion/Junk rules (subject or sender)
    if any(word in subj for word in PROMOTION_KEYWORDS):
        return "junk"
    if any(s in sender for s in PROMOTION_SENDERS):
        return "junk"

    # Important rules (subject or sender)
    if any(word in subj for word in IMPORTANT_KEYWORDS):
        return "important"
    if any(s in sender for s in IMPORTANT_SENDERS):
        return "important"

    return "other"

# Optional: let user see why something was classified a certain way
def explain_classification(email_obj):
    subj = (email_obj.get("subject") or "").lower()
    sender = (email_obj.get("from") or "").lower()
    for word in PROMOTION_KEYWORDS:
        if word in subj:
            return f"junk (matched promotion keyword: {word})"
    for s in PROMOTION_SENDERS:
        if s in sender:
            return f"junk (matched promotion sender: {s})"
    for word in IMPORTANT_KEYWORDS:
        if word in subj:
            return f"important (matched important keyword: {word})"
    for s in IMPORTANT_SENDERS:
        if s in sender:
            return f"important (matched important sender: {s})"
    return "other (no keyword/sender match)"

# Example usage/test
if __name__ == "__main__":
    email_samples = [
        {"from": "PlutoAI Team <no-reply@plutoai.com>", "subject": "How's Your PlutoAI Experience So Far?", "snippet": "..."},
        {"from": "Nubank <transacoes@nubank.com.br>", "subject": "Lembrete: Sua fatura vence amanhã", "snippet": "..."},
        {"from": "XYZ Person <xyz@random.com>", "subject": "Let's catch up this weekend", "snippet": "..."},
        {"from": "GitHub <noreply@github.com>", "subject": "Please download your two-factor recovery codes", "snippet": "..."},
        {"from": "Newsletter <newsletter@aiupdates.com>", "subject": "March's Hottest AI Tools", "snippet": "..."}
    ]

    for email in email_samples:
        label = classify_email(email)
        reason = explain_classification(email)
        print(f"Subject: {email['subject']}\n  >> Classified as: {label}\n  >> Reason: {reason}\n")

