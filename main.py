# main.py
from auth.gmail_auth.py import authenticate_gmail
from auth.imap_login.py import authenticate_imap
from fetcher.fetch_emails.py import fetch_emails
from processor.summarizer.py import summarize_emails
from processor.classifier.py import classify_emails
from sender.send_summary.py import send_summary_email
from utils.config.py import GMAIL_ACCOUNT, IMAP_SERVER, OTHER_ACCOUNTS, OPENAI_API_KEY
from utils.helpers.py import get_yesterday_date

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
