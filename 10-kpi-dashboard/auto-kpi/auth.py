"""
OAuth 2.0 authentication for GA4 + Google Sheets.
Requires a Desktop app credential (client_secrets.json with "installed" key).

First run: opens browser → user authorizes → saves token.json
All future runs (including cron): uses refresh token silently, no browser.
"""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

TOKEN_FILE   = "token.json"
SECRETS_FILE = "client_secrets.json"


def get_credentials() -> Credentials:
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if creds and creds.valid:
        return creds

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _save(creds)
            return creds
        except Exception as e:
            print(f"⚠️  Token refresh failed ({e}), re-authorizing…")
            creds = None

    if not os.path.exists(SECRETS_FILE):
        raise FileNotFoundError(
            f"\n❌ '{SECRETS_FILE}' not found.\n"
            "Create a Desktop app credential in Google Cloud Console:\n"
            "  APIs & Services → Credentials → + Create Credentials\n"
            "  → OAuth 2.0 Client ID → Desktop app → Download JSON\n"
            f"  → Save as '{SECRETS_FILE}' in this folder\n"
        )

    import json
    with open(SECRETS_FILE) as f:
        data = json.load(f)

    if "web" in data and "installed" not in data:
        raise ValueError(
            "\n❌ Wrong credential type: your client_secrets.json is a Web app credential.\n"
            "Please create a Desktop app credential instead:\n"
            "  Google Cloud Console → APIs & Services → Credentials\n"
            "  → + Create Credentials → OAuth 2.0 Client ID → Desktop app\n"
        )

    print("\n🔐 Opening browser for one-time Google authorization…")
    flow = InstalledAppFlow.from_client_secrets_file(SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    _save(creds)
    print(f"✅ Authorized. Token saved to {TOKEN_FILE} — future runs will be silent.\n")
    return creds


def _save(creds: Credentials):
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())


if __name__ == "__main__":
    get_credentials()
    print("Authorization complete. Run: python3 main.py")
