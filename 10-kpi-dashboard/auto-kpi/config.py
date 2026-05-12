import os
from dotenv import load_dotenv

load_dotenv()

# GA4 Properties
GA4_PROPERTY_MAIN  = os.getenv("GA4_PROPERTY_MAIN", "properties/123456789")
GA4_PROPERTY_APPLY = os.getenv("GA4_PROPERTY_APPLY", "properties/987654321")

# Google Sheets
GOOGLE_SHEET_ID      = os.getenv("GOOGLE_SHEET_ID", "")
CLIENT_SECRETS_FILE  = os.getenv("CLIENT_SECRETS_FILE", "client_secrets.json")
TOKEN_FILE           = os.getenv("TOKEN_FILE", "token.json")

# OpenAI
OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL     = os.getenv("OPENAI_MODEL", "gpt-4o")

# Business targets
MONTHLY_LEAD_TARGET = int(os.getenv("MONTHLY_LEAD_TARGET", "300"))
REPORT_TIMEZONE     = os.getenv("REPORT_TIMEZONE", "Europe/Malta")

# Sheet tab names
TAB_DAILY_KPIS     = "Daily_KPIs"
TAB_AI_ANALYSIS    = "AI_Analysis"
TAB_LEAD_PROGRESS  = "Lead_Progress"
TAB_TRAFFIC        = "Traffic_Sources"
TAB_PAGES          = "Top_Pages"
TAB_CONFIG         = "Config"

# Custom GA4 events to track
CUSTOM_EVENTS = [
    "apply_click",
    "lead_signup",
]

# Target markets for country flagging
TARGET_COUNTRIES = ["Ghana", "Nigeria", "Morocco", "Uganda", "Kenya"]

def validate():
    errors = []
    if not OPENAI_API_KEY:       errors.append("OPENAI_API_KEY is missing")
    if not GOOGLE_SHEET_ID:      errors.append("GOOGLE_SHEET_ID is missing")
    if "123456789" in GA4_PROPERTY_MAIN:  errors.append("GA4_PROPERTY_MAIN not set")
    if "987654321" in GA4_PROPERTY_APPLY: errors.append("GA4_PROPERTY_APPLY not set")
    import os
    if not os.path.exists(CLIENT_SECRETS_FILE) and not os.path.exists(TOKEN_FILE):
        errors.append(f"Neither '{CLIENT_SECRETS_FILE}' nor '{TOKEN_FILE}' found — run: python3 auth.py")
    return errors
