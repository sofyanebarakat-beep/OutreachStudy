"""
Google Sheets client.
Writes KPI data and AI analysis into the "OS KPI Hub" spreadsheet.
"""

import gspread
from datetime import date
from auth import get_credentials
import config

# Column headers for each tab
DAILY_KPIS_HEADERS = [
    "Date",
    "main_users", "main_sessions", "main_new_users", "main_pageviews",
    "main_engagement_rate", "main_avg_duration_sec", "main_engaged_sessions",
    "main_organic", "main_paid", "main_direct", "main_referral", "main_social",
    "apply_users", "apply_sessions", "apply_engagement_rate", "apply_avg_duration_sec",
    "apply_click", "lead_signup",
    "apply_click_rate", "lead_conv_rate", "website_lead_conv_rate",
    "mtd_leads", "monthly_target", "target_progress_pct",
    "projected_monthly_leads", "days_elapsed", "days_in_month",
    "days_remaining", "required_daily_pace", "projection_status",
]

AI_ANALYSIS_HEADERS = [
    "Date", "performance_score", "summary", "whats_working",
    "whats_not_working", "top_recommendation", "lead_projection_status",
    "action_items", "full_analysis",
]

TRAFFIC_HEADERS = ["Date", "Site", "Channel", "Sessions", "Users"]
PAGES_HEADERS   = ["Date", "Site", "Path", "Title", "Views", "Users", "Avg_Duration_sec", "Engagement_Rate"]


class SheetsClient:
    def __init__(self):
        creds = get_credentials()
        gc = gspread.authorize(creds)
        self.sheet = gc.open_by_key(config.GOOGLE_SHEET_ID)

    def test_connection(self) -> str:
        try:
            self.sheet.title
            return f"Sheets connection OK: '{self.sheet.title}'"
        except Exception as e:
            return f"Sheets connection FAILED: {e}"

    def _get_or_create_tab(self, name: str, headers: list) -> gspread.Worksheet:
        try:
            ws = self.sheet.worksheet(name)
        except gspread.WorksheetNotFound:
            ws = self.sheet.add_worksheet(title=name, rows=1000, cols=len(headers))
            ws.append_row(headers)
            # Format header row bold
            ws.format("1:1", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.27, "green": 0.18, "blue": 0.98}})
        return ws

    def _row_exists(self, ws: gspread.Worksheet, date_str: str) -> bool:
        try:
            col_a = ws.col_values(1)
            return date_str in col_a
        except Exception:
            return False

    # ──────────────────────────────────────────
    # SETUP — create all tabs if missing
    # ──────────────────────────────────────────
    def setup_tabs(self):
        self._get_or_create_tab(config.TAB_DAILY_KPIS,    DAILY_KPIS_HEADERS)
        self._get_or_create_tab(config.TAB_AI_ANALYSIS,   AI_ANALYSIS_HEADERS)
        self._get_or_create_tab(config.TAB_TRAFFIC,        TRAFFIC_HEADERS)
        self._get_or_create_tab(config.TAB_PAGES,          PAGES_HEADERS)
        print("  Sheets: all tabs ready")

    # ──────────────────────────────────────────
    # DAILY KPIs
    # ──────────────────────────────────────────
    def write_daily_kpis(self, kpis: dict):
        ws = self._get_or_create_tab(config.TAB_DAILY_KPIS, DAILY_KPIS_HEADERS)
        if self._row_exists(ws, kpis["date"]):
            print(f"  Daily KPIs: row for {kpis['date']} already exists, skipping.")
            return
        row = [kpis.get(h, "") for h in DAILY_KPIS_HEADERS]
        ws.append_row(row, value_input_option="USER_ENTERED")
        print(f"  Daily KPIs: written for {kpis['date']}")

    # ──────────────────────────────────────────
    # AI ANALYSIS
    # ──────────────────────────────────────────
    def write_ai_analysis(self, date_str: str, analysis: dict):
        ws = self._get_or_create_tab(config.TAB_AI_ANALYSIS, AI_ANALYSIS_HEADERS)
        if self._row_exists(ws, date_str):
            print(f"  AI Analysis: row for {date_str} already exists, skipping.")
            return
        row = [
            date_str,
            analysis.get("performance_score", ""),
            analysis.get("summary", ""),
            "\n".join(analysis.get("whats_working", [])),
            "\n".join(analysis.get("whats_not_working", [])),
            analysis.get("top_recommendation", ""),
            analysis.get("lead_projection_status", ""),
            "\n".join(analysis.get("action_items", [])),
            analysis.get("full_analysis", ""),
        ]
        ws.append_row(row, value_input_option="USER_ENTERED")
        print(f"  AI Analysis: written for {date_str}")

    # ──────────────────────────────────────────
    # TRAFFIC SOURCES
    # ──────────────────────────────────────────
    def write_traffic_sources(self, date_str: str, raw: dict):
        ws = self._get_or_create_tab(config.TAB_TRAFFIC, TRAFFIC_HEADERS)
        rows_to_add = []
        for site_key, site_label in [("main", "outreachstudy.eu"), ("apply", "apply.outreachstudy.eu")]:
            for ch_row in raw[site_key]["traffic"].get("rows", []):
                rows_to_add.append([
                    date_str, site_label,
                    ch_row["channel"], ch_row["sessions"], ch_row["users"]
                ])
        if rows_to_add:
            ws.append_rows(rows_to_add, value_input_option="USER_ENTERED")
        print(f"  Traffic Sources: {len(rows_to_add)} rows written")

    # ──────────────────────────────────────────
    # TOP PAGES
    # ──────────────────────────────────────────
    def write_top_pages(self, date_str: str, raw: dict):
        ws = self._get_or_create_tab(config.TAB_PAGES, PAGES_HEADERS)
        rows_to_add = []
        for site_key, site_label in [("main", "outreachstudy.eu"), ("apply", "apply.outreachstudy.eu")]:
            for p in raw[site_key].get("pages", []):
                rows_to_add.append([
                    date_str, site_label,
                    p["path"], p["title"], p["views"], p["users"],
                    p["avg_duration_sec"], p["engagement_rate"]
                ])
        if rows_to_add:
            ws.append_rows(rows_to_add, value_input_option="USER_ENTERED")
        print(f"  Top Pages: {len(rows_to_add)} rows written")

    # ──────────────────────────────────────────
    # UPDATE LEAD PROGRESS (monthly summary)
    # ──────────────────────────────────────────
    def update_lead_progress(self, kpis: dict):
        ws = self._get_or_create_tab(config.TAB_LEAD_PROGRESS, [
            "Month", "MTD_Leads", "Target", "Progress_Pct",
            "Avg_Daily_Leads", "Projected_Total", "Status"
        ])
        today = date.today()
        month_str = today.strftime("%Y-%m")
        col_a = ws.col_values(1)
        avg_daily = round(kpis["mtd_leads"] / kpis["days_elapsed"], 2) if kpis["days_elapsed"] > 0 else 0
        new_row = [
            month_str,
            kpis["mtd_leads"],
            kpis["monthly_target"],
            kpis["target_progress_pct"],
            avg_daily,
            kpis["projected_monthly_leads"],
            kpis["projection_status"],
        ]
        if month_str in col_a:
            row_idx = col_a.index(month_str) + 1
            ws.update(f"A{row_idx}:G{row_idx}", [new_row])
            print(f"  Lead Progress: updated {month_str}")
        else:
            ws.append_row(new_row, value_input_option="USER_ENTERED")
            print(f"  Lead Progress: new row for {month_str}")


if __name__ == "__main__":
    client = SheetsClient()
    print(client.test_connection())
