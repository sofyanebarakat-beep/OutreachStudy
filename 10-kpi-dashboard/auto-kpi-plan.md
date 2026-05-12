# Outreach Study — Automated KPI Analysis System
## Project Plan

---

## 1. Project Objective

Build a fully automated daily reporting system that:
- Pulls real data from Google Analytics 4 (two properties: outreachstudy.eu + apply.outreachstudy.eu)
- Calculates all key KPIs including lead funnel, traffic, conversions
- Sends the data to OpenAI GPT-4 for performance analysis and recommendations
- Saves everything (raw data + AI analysis) into a Google Sheet
- Tracks monthly progress toward the **300 leads/month** business target
- Runs automatically every day with zero manual action

**No email reports. No manual exports. No dashboards to refresh.**

---

## 2. System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DAILY CRON (08:00)                   │
└──────────────────────────┬──────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │        main.py          │
              │    (Orchestrator)       │
              └────────────┬────────────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │ ga4_client  │ │openai_client│ │sheets_client│
    │             │ │             │ │             │
    │ GA4 Data API│ │  GPT-4o     │ │ Sheets API  │
    │  (2 sites)  │ │  Analysis   │ │  (6 tabs)   │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           │
                  ┌────────▼────────┐
                  │  Google Sheet   │
                  │  "OS KPI Hub"   │
                  └─────────────────┘
```

**Data Flow:**
1. `ga4_client.py` → fetches yesterday's data from both GA4 properties
2. `kpi_formulas.py` → calculates all derived KPIs (rates, projections)
3. `openai_client.py` → sends KPI data to GPT-4o, receives analysis
4. `sheets_client.py` → appends raw KPIs + AI analysis to Google Sheet
5. Cron job → runs `main.py` daily at 08:00

---

## 3. Folder Structure

```
10-kpi-dashboard/
├── auto-kpi/
│   ├── main.py              # Daily orchestrator — runs everything
│   ├── ga4_client.py        # GA4 Data API — pulls all metrics
│   ├── openai_client.py     # OpenAI GPT-4 — analysis & recommendations
│   ├── sheets_client.py     # Google Sheets — saves data
│   ├── kpi_formulas.py      # KPI calculations & projections
│   ├── config.py            # All settings, targets, property IDs
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # Your credentials (never commit this)
│   ├── .env.example         # Template to share safely
│   ├── service_account.json # Google Service Account key (never commit)
│   └── README.md            # Setup instructions
├── auto-kpi-plan.md         # This document
├── dashboard.html           # Local GA4 dashboard
├── kpi-framework.md         # KPI reference
└── kpi-tracker.csv          # KPI targets tracker
```

---

## 4. Required APIs

| API | Purpose | Cost |
|-----|---------|------|
| Google Analytics Data API v1 (GA4) | Pull website & apply platform data | Free |
| Google Sheets API v4 | Write KPI data and analysis | Free |
| OpenAI API (GPT-4o) | Analyze KPIs, generate recommendations | ~$0.01–0.05/day |
| Google OAuth2 / Service Account | Authenticate GA4 + Sheets | Free |

**Estimated cost: ~$0.30–1.50/month** (OpenAI only)

---

## 5. Required Credentials

### A. Google Service Account (for GA4 + Sheets)
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → Enable these APIs:
   - **Google Analytics Data API**
   - **Google Sheets API**
3. IAM & Admin → Service Accounts → Create Service Account
4. Create JSON Key → download as `service_account.json`
5. In GA4 Admin → Account Access → Add the service account email with **Viewer** role
6. In Google Sheets → Share the sheet with the service account email (**Editor**)

### B. OpenAI API Key
1. Go to [platform.openai.com](https://platform.openai.com)
2. API Keys → Create new secret key
3. Add to `.env` as `OPENAI_API_KEY`

### C. GA4 Property IDs
- Go to GA4 Admin → Property Settings → Property ID
- You need **two Property IDs** (one per website):
  - `outreachstudy.eu` → `PROPERTY_ID_MAIN`
  - `apply.outreachstudy.eu` → `PROPERTY_ID_APPLY`

### D. Google Sheet ID
- Create a Google Sheet named **"OS KPI Hub"**
- The Sheet ID is in the URL: `docs.google.com/spreadsheets/d/**SHEET_ID**/edit`

### E. Your `.env` file will look like:
```
OPENAI_API_KEY=sk-...
GA4_PROPERTY_MAIN=properties/123456789
GA4_PROPERTY_APPLY=properties/987654321
GOOGLE_SHEET_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms
GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
MONTHLY_LEAD_TARGET=300
```

---

## 6. Required GA4 Events

These events must be firing in GA4 before the system can track them.

### Standard Events (auto-tracked by GA4 plugin)
| Event | Tracked on | Description |
|-------|-----------|-------------|
| `page_view` | Both sites | Every page visit |
| `session_start` | Both sites | New session begins |
| `scroll` | Both sites | 90% scroll depth |
| `click` | Both sites | Outbound link clicks |

### Custom Events (you must set these up)
| Event | Tracked on | Description | How to set up |
|-------|-----------|-------------|---------------|
| `apply_click` | outreachstudy.eu | Click on "Apply Now" CTA | GA4 Event via GTM or plugin |
| `form_start` | apply.outreachstudy.eu | User starts registration form | GTM trigger on form focus |
| `form_submit` | apply.outreachstudy.eu | Form successfully submitted | GTM trigger on form submit |
| `lead_signup` | apply.outreachstudy.eu | Confirmed lead created | GTM trigger on thank-you page |
| `whatsapp_click` | Both sites | Click on WhatsApp button | GTM trigger on WA link click |

### Event Setup Priority
1. `lead_signup` — most critical (this tracks your 300/month target)
2. `form_submit` — needed for conversion rate
3. `apply_click` — needed for CTA performance
4. `whatsapp_click` — needed for WhatsApp funnel
5. `form_start` — needed for form abandonment rate

---

## 7. Google Sheets Structure

The sheet **"OS KPI Hub"** has 6 tabs:

### Tab 1: `Daily_KPIs`
Raw daily data, one row per day per site.

| Column | Description |
|--------|-------------|
| Date | YYYY-MM-DD |
| Site | main / apply |
| Users | Total users |
| Sessions | Total sessions |
| New_Users | First-time visitors |
| Pageviews | Screen page views |
| Engagement_Rate | % engaged sessions |
| Avg_Session_Duration_sec | Seconds |
| Organic_Sessions | From organic search |
| Paid_Sessions | From paid social/search |
| Direct_Sessions | Direct traffic |
| Referral_Sessions | Referral traffic |
| Social_Sessions | Social (organic) |
| apply_click | Event count |
| form_start | Event count |
| form_submit | Event count |
| lead_signup | Event count |
| whatsapp_click | Event count |
| Apply_Click_Rate | apply_click / sessions |
| Form_Completion_Rate | form_submit / form_start |
| Lead_Conv_Rate | lead_signup / users |
| Month_To_Date_Leads | Running total this month |
| Monthly_Target | 300 |
| Target_Progress_Pct | MTD / 300 × 100 |
| Projected_Monthly_Leads | Projected at current pace |
| Days_In_Month | Total days |
| Days_Elapsed | Days so far |
| Required_Daily_Pace | Remaining leads / remaining days |

### Tab 2: `AI_Analysis`
AI-generated analysis, one row per day.

| Column | Description |
|--------|-------------|
| Date | YYYY-MM-DD |
| Performance_Score | 1–10 (GPT rated) |
| Summary | 2-sentence overview |
| Whats_Working | Bullet points |
| Whats_Not_Working | Bullet points |
| Top_Recommendation | Single most important action |
| Lead_Projection_Status | On track / Behind / Ahead |
| Action_Items | Numbered list |
| Full_Analysis | Complete GPT response |

### Tab 3: `Lead_Progress`
Monthly summary for lead tracking.

| Column | Description |
|--------|-------------|
| Month | YYYY-MM |
| Total_Leads | Actual leads that month |
| Target | 300 |
| Pct_Of_Target | Achieved % |
| Avg_Daily_Leads | Leads / days |
| Best_Day | Date with most leads |
| Best_Day_Count | Leads on best day |
| Top_Source | Traffic source that sent most leads |

### Tab 4: `Traffic_Sources`
Daily traffic source breakdown.

| Columns: Date, Site, Channel, Sessions, Users, Engagement_Rate, Avg_Duration |

### Tab 5: `Top_Pages`
Daily top 10 pages.

| Columns: Date, Site, Page_Path, Page_Title, Views, Users, Avg_Duration, Engagement_Rate |

### Tab 6: `Config`
Single-row settings sheet (editable manually).

| Key | Value |
|-----|-------|
| monthly_target | 300 |
| main_site | outreachstudy.eu |
| apply_site | apply.outreachstudy.eu |
| openai_model | gpt-4o |
| analysis_days | 7 |
| report_timezone | Europe/Malta |

---

## 8. KPI Formulas

```python
# Apply Click Rate
apply_click_rate = apply_click_events / sessions * 100

# Form Completion Rate (abandonment inverse)
form_completion_rate = form_submit / form_start * 100

# Lead Conversion Rate (website to lead)
lead_conv_rate = lead_signup / total_users * 100

# WhatsApp Click Rate
wa_click_rate = whatsapp_click / sessions * 100

# Month-to-Date Leads
mtd_leads = SUM(lead_signup) WHERE month = current_month

# Target Progress
target_progress = mtd_leads / 300 * 100

# Projected Monthly Leads
days_elapsed = current_day_of_month
days_in_month = total_days_in_month
projected = (mtd_leads / days_elapsed) * days_in_month

# Required Daily Pace
days_remaining = days_in_month - days_elapsed
leads_remaining = 300 - mtd_leads
required_daily_pace = leads_remaining / days_remaining

# Engagement Rate (from GA4 directly)
# GA4 definition: sessions lasting >10s OR 2+ pages OR conversion event
```

---

## 9. Implementation Steps

### Phase 1 — Setup (Day 1)
- [ ] Create Google Cloud project
- [ ] Enable Google Analytics Data API + Google Sheets API
- [ ] Create Service Account + download JSON key
- [ ] Create Google Sheet "OS KPI Hub" with 6 tabs
- [ ] Share Sheet with service account email
- [ ] Add service account to GA4 (Viewer)
- [ ] Get OpenAI API key
- [ ] Create `.env` file with all credentials
- [ ] Install Python dependencies: `pip install -r requirements.txt`

### Phase 2 — Build & Test (Day 2–3)
- [ ] Test GA4 connection: run `python ga4_client.py`
- [ ] Verify all custom events are firing in GA4 Real-time
- [ ] Test Sheets write: run `python sheets_client.py`
- [ ] Test OpenAI analysis: run `python openai_client.py`
- [ ] Run full pipeline: `python main.py`
- [ ] Verify data appears correctly in all 6 Sheet tabs

### Phase 3 — Automate (Day 4)
- [ ] Set up cron job (Mac/Linux) or Task Scheduler (Windows)
- [ ] Run at 08:00 daily (yesterday's data is complete by then)
- [ ] Monitor first 3 automated runs
- [ ] Adjust OpenAI prompt if analysis quality needs improvement

### Phase 4 — GA4 Event Setup (Parallel)
- [ ] Set up `lead_signup` event (highest priority)
- [ ] Set up `apply_click` event
- [ ] Set up `form_start` + `form_submit` events
- [ ] Set up `whatsapp_click` event
- [ ] Verify all events in GA4 DebugView

---

## 10. Testing Plan

### Unit Tests
```bash
# Test 1: GA4 connection
python -c "from ga4_client import GA4Client; c = GA4Client(); print(c.test_connection())"

# Test 2: Sheets connection
python -c "from sheets_client import SheetsClient; c = SheetsClient(); print(c.test_connection())"

# Test 3: OpenAI connection
python -c "from openai_client import OpenAIClient; c = OpenAIClient(); print(c.test_connection())"

# Test 4: Full pipeline (dry run — no Sheet write)
python main.py --dry-run

# Test 5: Full pipeline (real run)
python main.py
```

### Data Validation Checks
- Sessions > 0 (site is getting traffic)
- lead_signup >= 0 (no negative leads)
- All rates between 0–100%
- Projected leads is a positive number
- AI analysis is non-empty string

### Edge Cases
- No traffic on a given day (weekend/holiday) → write zeros, skip analysis
- GA4 event not firing → log warning, write 0, continue
- OpenAI rate limit → retry after 30 seconds, max 3 retries
- Sheets quota exceeded → retry after 60 seconds

---

## 11. Daily Automation Plan

### Cron Schedule (Mac/Linux)
```bash
# Edit crontab:
crontab -e

# Add this line (runs at 08:00 every day):
0 8 * * * cd /Users/sof/Documents/Projects/OutreachStudy/OutreachStudy/10-kpi-dashboard/auto-kpi && /usr/bin/python3 main.py >> logs/kpi_$(date +\%Y\%m\%d).log 2>&1
```

### What Runs Each Day at 08:00
```
08:00 → main.py starts
08:00 → Pull yesterday's data from GA4 (outreachstudy.eu)
08:01 → Pull yesterday's data from GA4 (apply.outreachstudy.eu)
08:02 → Calculate all KPI formulas
08:02 → Calculate month-to-date lead progress
08:03 → Send KPI data to OpenAI GPT-4o
08:03 → Receive AI analysis (10–20 seconds)
08:04 → Write raw KPIs to Daily_KPIs tab
08:04 → Write AI analysis to AI_Analysis tab
08:04 → Update Lead_Progress tab (monthly summary)
08:05 → Write traffic sources to Traffic_Sources tab
08:05 → Write top pages to Top_Pages tab
08:05 → Done. Log saved.
```

### What You Do Each Morning
```
08:05 → Open Google Sheet "OS KPI Hub"
08:06 → Check AI_Analysis tab → read Top_Recommendation
08:07 → Check Lead_Progress → are you on track for 300?
08:08 → Act on the recommendation (adjust ads, fix page, etc.)
Total time: 3 minutes
```
