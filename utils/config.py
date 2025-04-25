# utils/config.py
import os
import json
from dotenv import load_dotenv
load_dotenv()

# Gmail/IMAP settings
GMAIL_ACCOUNT = os.getenv("GMAIL_ACCOUNT")
IMAP_SERVER = os.getenv("IMAP_SERVER")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))

# Other IMAP accounts: JSON list of {username, password, imap_server}
OTHER_ACCOUNTS = []
raw_accounts = os.getenv("OTHER_ACCOUNTS_JSON")
if raw_accounts:
    try:
        OTHER_ACCOUNTS = json.loads(raw_accounts)
    except json.JSONDecodeError:
        OTHER_ACCOUNTS = []

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# SMTP settings (for later modules)
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
REPORT_RECIPIENT = os.getenv("REPORT_RECIPIENT", SMTP_USER)
