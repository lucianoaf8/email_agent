#!/usr/bin/env python3
"""
Gmail Fetch Proof-of-Concept
Usage:
  python3 scripts/demo_fetch.py
Make sure the environment variables (GMAIL_ACCOUNT, IMAP_SERVER, IMAP_PORT, and OAuth2 credentials.json in auth/) are set.
"""
import os
import sys
import json
import imaplib

# Ensure project root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth.gmail_auth import get_gmail_oauth2_credentials
from google.auth.transport.requests import Request
from fetcher import fetch_emails
from utils.config import GMAIL_ACCOUNT, IMAP_SERVER, IMAP_PORT

import argparse

parser = argparse.ArgumentParser(description="Demo fetch and classify Gmail emails")
parser.add_argument("--mailbox", default="INBOX", help="Mailbox to fetch from")
parser.add_argument("--since-date", dest="since_date", help="Date to fetch (DD-Mon-YYYY), defaults to yesterday")
args = parser.parse_args()


def login_via_oauth2(creds, user, host, port):
    """
    Given Google OAuth2 credentials, authenticate to IMAP using XOAUTH2.
    """
    # Refresh token if needed
    if not creds.valid:
        creds.refresh(Request())
    auth_str = f"user={user}\x01auth=Bearer {creds.token}\x01\x01"
    imap = imaplib.IMAP4_SSL(host, port)
    imap.authenticate('XOAUTH2', lambda x: auth_str.encode())
    return imap


def main():
    # Acquire OAuth2 credentials
    creds = get_gmail_oauth2_credentials()
    # Connect and authenticate to Gmail IMAP
    imap_conn = login_via_oauth2(creds, GMAIL_ACCOUNT, IMAP_SERVER, IMAP_PORT)
    # Fetch emails based on args
    emails = fetch_emails(imap_conn, mailbox=args.mailbox, since_date=args.since_date)
    # Classify emails
    from processor.classifier import classify_email, explain_classification
    categorized = {"important": [], "junk": [], "other": []}
    for e in emails:
        label = classify_email(e)
        reason = explain_classification(e)
        e["classification"] = label
        e["reason"] = reason
        categorized[label].append(e)

    # Print summary
    total = len(emails)
    imp = len(categorized["important"])
    junk = len(categorized["junk"])
    other = len(categorized["other"])
    print(f"Fetched {total} emails: {imp} important, {junk} junk, {other} other.")
    print("\nDetails:")
    for label in ["important", "junk", "other"]:
        print(f"\n== {label.upper()} ({len(categorized[label])}) ==")
        for e in categorized[label]:
            print(f"- {e['subject']} from {e['from']} [{e['reason']}]")
    # Also output full JSON
    print("\nFull JSON output:")
    print(json.dumps(emails, indent=2))


if __name__ == '__main__':
    main()