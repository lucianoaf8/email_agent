"""
processor package
"""
from .summarizer import summarize_emails_with_llm as summarize_emails
from .classifier import classify_email as classify_emails, explain_classification
