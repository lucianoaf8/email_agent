# main.py
from auth import authenticate_gmail, authenticate_imap
from fetcher import fetch_emails
from processor import summarize_emails, classify_emails
from sender import send_summary_email
from utils.config import GMAIL_ACCOUNT, IMAP_SERVER, IMAP_PORT, OTHER_ACCOUNTS
from utils.helpers import get_yesterday_date

def main():
    # Authenticate Gmail account
    gmail_creds = authenticate_gmail()

    # Fetch emails from Gmail 
    gmail_emails = fetch_emails(gmail_creds, IMAP_SERVER, GMAIL_ACCOUNT, get_yesterday_date())

    # Authenticate and fetch emails from other accounts
    other_emails = []
    for account in OTHER_ACCOUNTS:
        mail = authenticate_imap(account['username'], account['password'], account['imap_server'])
        other_emails.extend(fetch_emails(mail, account['imap_server'], account['username'], get_yesterday_date()))

    # Combine all emails
    all_emails = gmail_emails + other_emails

    # Summarize emails
    summaries = summarize_emails(all_emails, OPENAI_API_KEY)

    # Classify emails
    classified_emails = classify_emails(summaries)

    # Send summary email
    send_summary_email(classified_emails, GMAIL_ACCOUNT, OTHER_ACCOUNTS)

if __name__ == "__main__":
    main()
