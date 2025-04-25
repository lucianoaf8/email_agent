import datetime
import email
import imaplib
from ..auth import gmail_auth, imap_login

def get_yesterday_date():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    return yesterday.strftime("%d-%b-%Y")  # IMAP date format

def fetch_yesterday_emails(mailbox, imap_connection):
    date = get_yesterday_date()
    imap_connection.select(mailbox)
    # Search for yesterday's emails
    typ, data = imap_connection.search(None, f'(ON "{date}")')
    email_ids = data[0].split()
    emails = []
    for e_id in email_ids:
        typ, raw = imap_connection.fetch(e_id, "(RFC822)")
        msg = email.message_from_bytes(raw[0][1])
        sender = email.utils.parseaddr(msg.get("From"))[1]
        subject = msg.get("Subject")
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
            "from": sender,
            "subject": subject,
            "snippet": snippet
        })
    return emails
