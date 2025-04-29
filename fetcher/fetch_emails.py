import email
import imaplib2
import re
import json
import os
import datetime
from utils.helpers import get_yesterday_date
from utils.logger import logger
from utils.config import IMAP_SERVER, IMAP_PORT, GMAIL_ACCOUNT

def save_emails_to_data(emails):
    """Save fetched emails to data folder as JSON."""
    if not os.path.exists('data'):
        os.makedirs('data')
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/emails_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(emails, f, indent=2)
    logger.info(f"Saved {len(emails)} emails to {filename}")

def fetch_emails(imap_conn=None, mailbox="INBOX", since_date=None):
    """
    Fetch emails from `mailbox` on the given `since_date` (format DD-Mon-YYYY).
    Returns list of dicts with keys: uid, date, from, subject, snippet.
    """
    logger.info(f"Starting fetch_emails from {mailbox} since {since_date}")
    
    # Create new connection if none provided
    if imap_conn is None:
        from auth.gmail_auth import get_gmail_oauth2_credentials
        creds = get_gmail_oauth2_credentials()
        import imaplib2
        imap_conn = imaplib2.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        auth_string = f"user={GMAIL_ACCOUNT}\1auth=Bearer {creds.token}\1\1"
        imap_conn.authenticate('XOAUTH2', lambda x: auth_string)
    
    date_str = since_date if since_date else get_yesterday_date()
    # Select the mailbox/folder
    try:
        logger.debug(f"IMAP connection state before select: {imap_conn.state}")
        typ, data = imap_conn.select(mailbox)
        if typ != 'OK':
            raise Exception(f"Failed to select mailbox {mailbox}: {data[0].decode()}")
        logger.debug(f"Selected mailbox: {mailbox}, state: {imap_conn.state}")
        
        # Use UID search for consistent identifiers
        search_criteria = f'(ON "{date_str}")'
        logger.debug(f"Using search criteria: {search_criteria}")
        typ, data = imap_conn.uid('SEARCH', None, search_criteria)
        logger.debug(f"Search response type: {typ}, data: {data}")
        uids = data[0].split() if data and data[0] else []
        
        # Fallback to ALL emails if none found for date
        if not uids:
            logger.info("No emails found for date, trying ALL emails")
            typ, data = imap_conn.uid('SEARCH', None, 'ALL')
            uids = data[0].split() if data and data[0] else []
            logger.debug(f"ALL search found {len(uids)} emails")
        emails = []
        # Limit to 5 emails for testing
        for uid in uids[:5]:
            # Fetch full message by UID
            try:
                typ, msg_data = imap_conn.uid('FETCH', uid, '(RFC822)')
                raw = msg_data[0][1]
                msg = email.message_from_bytes(raw)
                sender = email.utils.parseaddr(msg.get("From"))[1]
                subject = msg.get("Subject")
                date_hdr = msg.get("Date")
                # Extract plain-text body snippet
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        ctype = part.get_content_type()
                        cdispo = str(part.get("Content-Disposition"))
                        if ctype == "text/plain" and "attachment" not in cdispo:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")
                # Remove any strings that look like API keys or passwords
                body = re.sub(r"(sk-|ghp_|ey[A-Za-z0-9_-]+).*", "[REDACTED]", body)
                snippet = body[:200].replace('\n', ' ').replace('\r', '')
                emails.append({
                    "uid": uid.decode(),
                    "date": date_hdr,
                    "from": sender,
                    "subject": subject,
                    "snippet": snippet
                })
            except Exception as e:
                logger.error(f"Failed to fetch email with UID {uid}: {e}")
        logger.info(f"Finished fetching {len(emails)} emails from {mailbox}")
        if emails:
            save_emails_to_data(emails)
        return emails
    except Exception as e:
        logger.error(f"Failed to select mailbox {mailbox}: {e}")
        return []
