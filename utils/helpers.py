# utils/helpers.py
from datetime import datetime, timedelta
import re
from utils.logger import logger

def get_yesterday_date():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%d-%b-%Y')

def validate_email_content(emails):
    """Check for potential credential leaks before processing"""
    SENSITIVE_TERMS = [
        "password", "token", "key", "secret", 
        "credential", "authorization", "bearer"
    ]
    CRED_PATTERNS = [
        r'(?i)(password|token|key|secret|auth)\s*[:=]\s*[\'"]?\S+[\'"]?',
        r'sk-[a-zA-Z0-9]{24,}',
        r'ghp_[a-zA-Z0-9]{36}',
        r'eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}'
    ]
    
    for email in emails:
        content = f"{email.get('subject','')} {email.get('snippet','')}".lower()
        
        # Check for sensitive terms
        for term in SENSITIVE_TERMS:
            if term in content:
                logger.error(f"Sensitive term '{term}' found in email from {email.get('from')}")
                raise ValueError(f"Potential credential leak detected - contains '{term}'")
        
        # Check for credential patterns
        for pattern in CRED_PATTERNS:
            if re.search(pattern, content):
                logger.error(f"Credential pattern matched in email from {email.get('from')}")
                raise ValueError("Potential credential leak detected - matches known pattern")
