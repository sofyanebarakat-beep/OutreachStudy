# OutreachStudy — Automated KPI System

GA4 → OpenAI → Google Sheets pipeline. Runs daily at 08:00.

## Quick Start

### 1. Install dependencies
```bash
cd 10-kpi-dashboard/auto-kpi
pip install -r requirements.txt
```

### 2. Add credentials
```bash
cp .env.example .env
# Edit .env with your real values
```

Place your `service_account.json` in this folder.

### 3. Test connections
```bash
python ga4_client.py
python sheets_client.py
python openai_client.py
```

### 4. Run once (dry run — no Sheets write)
```bash
python main.py --dry-run
```

### 5. Run for real
```bash
python main.py
```

### 6. Automate with cron
```bash
crontab -e
# Add:
0 8 * * * cd /path/to/auto-kpi && python3 main.py >> logs/kpi.log 2>&1
```

## Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Run for yesterday |
| `python main.py --dry-run` | Run without writing to Sheets |
| `python main.py --skip-ai` | Skip OpenAI (saves API cost) |
| `python main.py --date 2026-05-10` | Run for a specific date |

## Required credentials in .env

| Variable | Description |
|----------|-------------|
| `GA4_PROPERTY_MAIN` | GA4 Property for outreachstudy.eu |
| `GA4_PROPERTY_APPLY` | GA4 Property for apply.outreachstudy.eu |
| `GOOGLE_SHEET_ID` | ID from the Google Sheet URL |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | Path to service_account.json |
| `OPENAI_API_KEY` | OpenAI secret key |
| `MONTHLY_LEAD_TARGET` | Default: 300 |
