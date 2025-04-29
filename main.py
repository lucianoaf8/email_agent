# main.py
from auth import authenticate_gmail, authenticate_imap, login_imap
from fetcher import fetch_emails
from processor import summarize_emails, classify_emails
from sender import send_summary_email
from utils.config import GMAIL_ACCOUNT, IMAP_SERVER, IMAP_PORT, OTHER_ACCOUNTS
from utils.helpers import get_yesterday_date
from dotenv import load_dotenv
import os
from utils.logger import logger

load_dotenv()
# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def main():
    logger.info("Starting email agent")
    # Fetch emails from Gmail
    gmail_emails = fetch_emails(mailbox="INBOX", since_date=get_yesterday_date())

    # Authenticate and fetch emails from other accounts
    other_emails = []
    for account in OTHER_ACCOUNTS:
        mail = authenticate_imap(account['username'], account['password'], account['imap_server'])
        other_emails.extend(fetch_emails(mail, account['imap_server'], account['username'], get_yesterday_date()))

    # Combine all emails
    all_emails = gmail_emails + other_emails

    # Validate email content for sensitive data
    from utils.helpers import validate_email_content
    validate_email_content(all_emails)

    # Test mode early exit
    from utils.config import TEST_MODE
    if TEST_MODE:
        logger.info(f"TEST MODE ACTIVE - Fetched {len(all_emails)} emails")
        logger.info("Stopping after fetch as per TEST_MODE")
        return {
            "status": "test_complete", 
            "emails_fetched": len(all_emails),
            "first_email": all_emails[0] if all_emails else None
        }

    # Summarize emails
    summaries = summarize_emails(all_emails, OPENAI_API_KEY)

    # Classify emails
    classified_emails = []
    for email in all_emails:
        classification = classify_email(email)
        classified_emails.append({"email": email, "classification": classification})

    # Extract important emails
    important_emails = [email["email"] for email in classified_emails if email["classification"] == "important"]

    # Send summary email
    send_summary_email("Daily Email Report", summaries, {"Gmail": important_emails})

if __name__ == "__main__":
    main()
