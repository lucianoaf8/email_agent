import logging
import os
import re

def redact_sensitive(text):
    """Redact sensitive information from log messages."""
    if not text:
        return text
    # Redact API keys and tokens
    text = re.sub(r'(sk-|ghp_|ey[A-Za-z0-9_-]+).*', '[REDACTED]', text)
    return text

class RedactingFormatter(logging.Formatter):
    def format(self, record):
        original = super().format(record)
        return redact_sensitive(original)

def setup_logger():
    """Sets up a logger that saves to a file and prints to the console."""
    log_file = os.path.join(os.getcwd(), "logs", "email_agent.log")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    formatter = RedactingFormatter('%(asctime)s [%(levelname)s] %(message)s')
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger

logger = setup_logger()
