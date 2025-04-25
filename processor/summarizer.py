import os
from typing import List, Dict
import openai

# Add this if you're planning to use dotenv for secrets (recommended)
from dotenv import load_dotenv
load_dotenv()

# Read OpenAI API Key from environment or config
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable not set!"
openai.api_key = OPENAI_API_KEY

def format_emails_for_summary(emails: List[Dict]) -> str:
    """
    Formats a list of emails ready for LLM prompt.
    """
    lines = []
    for idx, email_obj in enumerate(emails, 1):
        from_ = email_obj.get("from", "")
        subject = email_obj.get("subject", "")
        snippet = email_obj.get("snippet", "")
        lines.append(f"{idx}. From: {from_}\n   Subject: {subject}\n   Snippet: {snippet}")
    return "\n".join(lines)

def summarize_emails_with_llm(emails: List[Dict], mailbox: str = "Mailbox") -> str:
    """
    Takes a list of email dicts, generates a prompt, and returns a concise summary via GPT API.
    Returns summary string.
    """
    if not emails:
        return f"No emails received in {mailbox} yesterday."

    input_text = format_emails_for_summary(emails)
    prompt = (
        f"Summarize the main points of the following {len(emails)} emails from mailbox: {mailbox} "
        "so that a busy user can get the gist in a few sentences. Only mention notable topics, requests, or actions. "
        "Do NOT include spam or promotional messages if obvious. Here are the emails:\n\n"
        f"{input_text}\n\nSummary:"
    )

    # Using the GPT-3.5-turbo model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Or gpt-4o etc.
        messages=[
            {"role": "system", "content": "You are an expert assistant for summarizing email digests."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.5,
        n=1,
        stop=None,
    )
    return response.choices[0].message['content'].strip()

# Optionally: A simple CLI for testing this module - run as script
if __name__ == "__main__":
    # Example emails
    emails = [
        {"from": "boss@company.com", "subject": "Monday Report Needed", "snippet": "Hi, please send the Monday sales report."},
        {"from": "no-reply@promo.com", "subject": "Special Offer!", "snippet": "Act now to receive free shipping..."},
        {"from": "alice@client.com", "subject": "Meeting Reschedule", "snippet": "Can we move our call to Tuesday?"},
    ]
    print(summarize_emails_with_llm(emails, "Test Mailbox"))
