import email
import imaplib
from utils.helpers import get_yesterday_date

def fetch_emails(imap_conn, mailbox="INBOX", since_date=None):
    """
    Fetch emails from `mailbox` on the given `since_date` (format DD-Mon-YYYY).
    Returns list of dicts with keys: uid, date, from, subject, snippet.
    """
    date_str = since_date if since_date else get_yesterday_date()
    # Select the mailbox/folder
    imap_conn.select(mailbox)
    # Use UID search for consistent identifiers
    typ, data = imap_conn.uid('SEARCH', None, f'(ON "{date_str}")')
    uids = data[0].split() if data and data[0] else []
    emails = []
    for uid in uids:
        # Fetch full message by UID
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
        snippet = body[:200].replace('\n', ' ').replace('\r', '')
        emails.append({
            "uid": uid.decode(),
            "date": date_hdr,
            "from": sender,
            "subject": subject,
            "snippet": snippet
        })
    return emails
