"""
Main orchestrator — runs the full KPI pipeline.

Usage:
  python main.py              # Run for yesterday (normal daily use)
  python main.py --dry-run    # Fetch data but don't write to Sheets
  python main.py --date 2026-05-10   # Run for a specific date
"""

import sys
import argparse
from datetime import date, datetime
import config
from ga4_client     import GA4Client
from kpi_formulas   import calculate, format_for_display
from openai_client  import OpenAIClient
from sheets_client  import SheetsClient


def parse_args():
    parser = argparse.ArgumentParser(description="OutreachStudy KPI Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Fetch data only, don't write to Sheets")
    parser.add_argument("--date", type=str, help="Target date YYYY-MM-DD (default: yesterday)")
    parser.add_argument("--skip-ai", action="store_true", help="Skip OpenAI analysis")
    return parser.parse_args()


def run(target_date: date = None, dry_run: bool = False, skip_ai: bool = False):
    start_time = datetime.now()
    print(f"\n{'='*60}")
    print(f"OutreachStudy KPI Pipeline — {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")

    # ── Validate config ─────────────────────────────────────
    errors = config.validate()
    if errors:
        print("\n⚠️  Configuration errors:")
        for e in errors: print(f"   - {e}")
        print("\nFix your .env file and retry.")
        sys.exit(1)

    # ── Step 1: Pull GA4 data ────────────────────────────────
    print("\n[1/4] Pulling GA4 data…")
    ga4 = GA4Client()
    raw = ga4.pull_all(target_date=target_date)

    # ── Step 2: Calculate KPIs ───────────────────────────────
    print("\n[2/4] Calculating KPIs…")
    kpis = calculate(raw)
    summary = format_for_display(kpis)
    print(summary)

    # ── Step 3: OpenAI analysis ──────────────────────────────
    analysis = None
    if not skip_ai:
        print("\n[3/4] Running OpenAI analysis…")
        ai = OpenAIClient()
        analysis = ai.analyze(summary, kpis)
        print(f"\n  Score:      {analysis.get('performance_score')}/10")
        print(f"  Status:     {analysis.get('lead_projection_status')}")
        print(f"  Top action: {analysis.get('top_recommendation')}")
    else:
        print("\n[3/4] Skipping OpenAI analysis (--skip-ai)")

    # ── Step 4: Write to Sheets ──────────────────────────────
    if dry_run:
        print("\n[4/4] DRY RUN — skipping Sheets write")
    else:
        print("\n[4/4] Writing to Google Sheets…")
        sheets = SheetsClient()
        sheets.setup_tabs()
        sheets.write_daily_kpis(kpis)
        if analysis:
            sheets.write_ai_analysis(kpis["date"], analysis)
        sheets.write_traffic_sources(kpis["date"], raw)
        sheets.write_top_pages(kpis["date"], raw)
        sheets.update_lead_progress(kpis)

    # ── Done ─────────────────────────────────────────────────
    elapsed = (datetime.now() - start_time).seconds
    print(f"\n{'='*60}")
    print(f"✅ Pipeline complete in {elapsed}s")
    print(f"   Date:       {kpis['date']}")
    print(f"   Leads:      {kpis['lead_signup']} today / {kpis['mtd_leads']} MTD")
    print(f"   Progress:   {kpis['target_progress_pct']}% of {kpis['monthly_target']} target")
    print(f"   Projected:  {kpis['projected_monthly_leads']} leads this month")
    if not dry_run:
        print(f"   Sheet: https://docs.google.com/spreadsheets/d/{config.GOOGLE_SHEET_ID}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    args = parse_args()
    target = None
    if args.date:
        target = datetime.strptime(args.date, "%Y-%m-%d").date()
    run(target_date=target, dry_run=args.dry_run, skip_ai=args.skip_ai)
