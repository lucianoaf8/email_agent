import os
import pickle
import logging
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from utils.logger import logger

# Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s"
# )
# logger = logging.getLogger("gmail_auth")

SCOPES = ["https://mail.google.com/"]  # Full mail access

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "token.pickle")
CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")


def get_gmail_oauth2_credentials(interactive_if_missing=True):
    """
    Returns Google OAuth2 credentials for Gmail.
    Handles token refresh, saving/loading, and first-time authentication.
    If interactive authentication is needed and interactive_if_missing=False, raise Exception.
    """
    logger.info("Starting get_gmail_oauth2_credentials")
    creds = None

    # Load token if it exists
    if os.path.exists(TOKEN_PATH):
        try:
            with open(TOKEN_PATH, "rb") as token_file:
                creds = pickle.load(token_file)
            logger.info("Loaded existing credentials from token.pickle")
        except Exception as e:
            logger.error(f"Failed to load credentials: {e}")
            creds = None

    # Refresh or obtain new credentials as needed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                logger.info("Refreshed credentials successfully.")
            except RefreshError as e:
                logger.warning(f"Failed to refresh token: {e}")
                creds = None
        if not creds or not creds.valid:
            if not os.path.exists(CREDENTIALS_PATH):
                logger.critical(f"Missing credentials.json at {CREDENTIALS_PATH}")
                raise FileNotFoundError(
                    f"Missing credentials.json at {CREDENTIALS_PATH}. "
                    "Download it from Google Cloud Console and place it here."
                )
            if not interactive_if_missing:
                logger.critical(
                    "Interactive authentication required, but interactive_if_missing=False."
                )
                raise RuntimeError(
                    "User consent required but not permitted in current automation context."
                )
            try:
                # Try browser flow
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                try:
                    creds = flow.run_local_server(port=0)
                    logger.info("Obtained new credentials via browser consent.")
                except Exception as flow_ex:
                    logger.warning("Browser flow failed. Attempting console fallback.")
                    creds = flow.run_console()
                    logger.info("Obtained new credentials via console flow.")
            except Exception as e:
                logger.error(f"Authentication failed: {e}")
                raise
        # Save credentials back to file after successful refresh or obtain
        try:
            with open(TOKEN_PATH, "wb") as token_file:
                pickle.dump(creds, token_file)
            logger.info("Saved new credentials to token.pickle.")
        except Exception as e:
            logger.error(f"Could not save credentials: {e}")
    logger.info("Finished get_gmail_oauth2_credentials")
    return creds


if __name__ == "__main__":
    try:
        creds = get_gmail_oauth2_credentials()
        logger.info("Credentials are ready for use.")
    except Exception as e:
        logger.error(f"Exiting with error: {e}")
