import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load secrets from environment
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))   # Use 465 for SSL, 587 for TLS (starttls)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
REPORT_RECIPIENT = os.getenv("REPORT_RECIPIENT", SMTP_USER)

def craft_summary_mail(subject, summary_text, important_emails_by_mailbox):
    """
    Compose a nicely formatted HTML summary report.
    `important_emails_by_mailbox` is a dict: {
        'Gmail': [{'from':..., 'subject':..., 'snippet':...}, ...], 
        'Other IMAP': [...]
    }
    """
    html = ["<h2>Daily Email Summary</h2>", f"<p>{summary_text}</p>"]
    for box, emails in important_emails_by_mailbox.items():
        html.append(f"<h3>{box} - Important Emails</h3>")
        if emails:
            html.append("<ul>")
            for e in emails:
                html.append(f"<li><strong>{e['subject']}</strong> from <em>{e['from']}</em><br><small>{e['snippet']}</small></li>")
            html.append("</ul>")
        else:
            html.append("<p>No important emails listed for this account.</p>")
    return "\n".join(html)

def send_summary_email(subject, summary_text, important_emails_by_mailbox,
                      sender=SMTP_USER, recipient=REPORT_RECIPIENT):
    """
    Send the daily summary email.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    html_content = craft_summary_mail(subject, summary_text, important_emails_by_mailbox)
    msg.attach(MIMEText(html_content, "html"))

    if SMTP_PORT == 465:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    else:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
    # Login and send
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()

if __name__ == "__main__":
    # Example usage
    mock_summary = "You received 12 emails. 7 were promotional. There are 3 requiring your attention."
    # Example mailbox dict
    mock_important = {
        "Gmail": [
            {"from": "GitHub <noreply@github.com>", "subject": "Download recovery codes", "snippet": "Please download and store your two-factor codes..."},
            {"from": "Nubank <foo@nubank.com>", "subject": "Sua fatura vence amanhã", "snippet": "Lembrete: o pagamento vence em..."}
        ],
        "Work": [
            {"from": "Boss <boss@company.com>", "subject": "Status Update Needed", "snippet": "Where is that report?"},
        ]
    }
    send_summary_email("Daily Email Report", mock_summary, mock_important)
    print("Sent (if SMTP settings are correct)")

