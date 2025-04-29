# scripts/test_imap.py
import os
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config import IMAP_SERVER, IMAP_PORT, GMAIL_ACCOUNT
from utils.logger import logger
import imaplib2

def test_imap_connection():
    """Test basic IMAP connection and mailbox operations"""
    load_dotenv()
    
    try:
        # Connect to IMAP server
        logger.info(f"Connecting to {IMAP_SERVER}:{IMAP_PORT}")
        mail = imaplib2.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        logger.info(f"Connected successfully, state: {mail.state}")

        # Login using OAuth2
        from auth.gmail_auth import get_gmail_oauth2_credentials
        creds = get_gmail_oauth2_credentials()
        auth_string = f"user={GMAIL_ACCOUNT}\1auth=Bearer {creds.token}\1\1"
        mail.authenticate('XOAUTH2', lambda x: auth_string)
        logger.info(f"Authenticated successfully, state: {mail.state}")

        # List mailboxes
        logger.info("Listing mailboxes...")
        typ, data = mail.list()
        if typ == 'OK':
            for mailbox in data:
                logger.info(f"Mailbox: {mailbox.decode()}")
        else:
            logger.error("Failed to list mailboxes")

        # Check INBOX status
        logger.info("Checking INBOX status...")
        mail.select("INBOX")
        typ, data = mail.status("INBOX", "(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)")
        if typ == 'OK':
            logger.info(f"INBOX status: {data[0].decode()}")
        else:
            logger.error("Failed to get INBOX status")

        # Logout
        mail.logout()
        logger.info("Logged out successfully")

    except Exception as e:
        logger.error(f"IMAP test failed: {e}")

if __name__ == "__main__":
    test_imap_connection()
