"""
KPI calculations and projections.
Events tracked: apply_click, lead_signup only.
"""

from datetime import date
import calendar
import config


def safe_div(numerator, denominator, multiply=1, decimals=2):
    if not denominator:
        return 0.0
    return round((numerator / denominator) * multiply, decimals)


def calculate(raw: dict) -> dict:
    today       = date.today()
    report_date = raw["date"]
    main        = raw["main"]
    apply       = raw["apply"]
    mtd_leads   = raw["mtd_leads"]

    m_ov = main["overview"]
    m_ev = main["events"]
    m_tr = main["traffic"]

    a_ov = apply["overview"]
    a_ev = apply["events"]

    apply_click = m_ev.get("apply_click", 0)
    lead_signup = a_ev.get("lead_signup", 0)

    # Apply Click Rate: how many sessions led to an apply click
    apply_click_rate = safe_div(apply_click, m_ov["sessions"], multiply=100)

    # Lead Conversion Rate: apply site visitors who became leads
    lead_conv_rate = safe_div(lead_signup, a_ov["users"], multiply=100)

    # Website Lead Rate: main site visitors who eventually became leads
    website_lead_conv_rate = safe_div(lead_signup, m_ov["users"], multiply=100)

    # Monthly lead progress
    days_elapsed   = today.day - 1
    days_in_month  = calendar.monthrange(today.year, today.month)[1]
    days_remaining = days_in_month - days_elapsed

    projected_monthly = round((mtd_leads / days_elapsed) * days_in_month, 1) if days_elapsed > 0 else 0
    target_progress   = safe_div(mtd_leads, config.MONTHLY_LEAD_TARGET, multiply=100)
    required_daily    = round((config.MONTHLY_LEAD_TARGET - mtd_leads) / days_remaining, 1) if days_remaining > 0 else 0

    if projected_monthly >= config.MONTHLY_LEAD_TARGET * 0.95:
        projection_status = "On track"
    elif projected_monthly >= config.MONTHLY_LEAD_TARGET * 0.75:
        projection_status = "Slightly behind"
    else:
        projection_status = "Behind — action needed"

    return {
        "date": report_date,

        # Main site overview
        "main_users":            m_ov["users"],
        "main_sessions":         m_ov["sessions"],
        "main_new_users":        m_ov["new_users"],
        "main_pageviews":        m_ov["pageviews"],
        "main_engagement_rate":  m_ov["engagement_rate"],
        "main_avg_duration_sec": m_ov["avg_session_duration_sec"],
        "main_engaged_sessions": m_ov["engaged_sessions"],

        # Main site traffic sources
        "main_organic":   m_tr["organic"],
        "main_paid":      m_tr["paid"],
        "main_direct":    m_tr["direct"],
        "main_referral":  m_tr["referral"],
        "main_social":    m_tr["social"],

        # Apply site overview
        "apply_users":            a_ov["users"],
        "apply_sessions":         a_ov["sessions"],
        "apply_engagement_rate":  a_ov["engagement_rate"],
        "apply_avg_duration_sec": a_ov["avg_session_duration_sec"],

        # The 2 tracked events
        "apply_click": apply_click,
        "lead_signup":  lead_signup,

        # Calculated KPIs
        "apply_click_rate":       apply_click_rate,
        "lead_conv_rate":         lead_conv_rate,
        "website_lead_conv_rate": website_lead_conv_rate,

        # Monthly lead progress
        "mtd_leads":               mtd_leads,
        "monthly_target":          config.MONTHLY_LEAD_TARGET,
        "target_progress_pct":     target_progress,
        "projected_monthly_leads": projected_monthly,
        "days_elapsed":            days_elapsed,
        "days_in_month":           days_in_month,
        "days_remaining":          days_remaining,
        "required_daily_pace":     required_daily,
        "projection_status":       projection_status,
    }


def format_for_display(kpis: dict) -> str:
    def dur(s):
        m = int(s // 60)
        sec = int(s % 60)
        return f"{m}m {sec:02d}s"

    return f"""
=== OUTREACH STUDY — DAILY KPI REPORT ({kpis['date']}) ===

MAIN WEBSITE (outreachstudy.eu)
  Users:              {kpis['main_users']:,}
  Sessions:           {kpis['main_sessions']:,}
  New Users:          {kpis['main_new_users']:,}
  Pageviews:          {kpis['main_pageviews']:,}
  Engagement Rate:    {kpis['main_engagement_rate']}%   (target ≥50%)
  Avg Session:        {dur(kpis['main_avg_duration_sec'])}   (target ≥2:30)

TRAFFIC SOURCES (main site)
  Organic Search:     {kpis['main_organic']:,}
  Paid Social/Search: {kpis['main_paid']:,}
  Direct:             {kpis['main_direct']:,}
  Referral:           {kpis['main_referral']:,}
  Social (organic):   {kpis['main_social']:,}

APPLY PLATFORM (apply.outreachstudy.eu)
  Users:              {kpis['apply_users']:,}
  Sessions:           {kpis['apply_sessions']:,}
  Engagement Rate:    {kpis['apply_engagement_rate']}%

EVENTS
  Apply clicks:       {kpis['apply_click']}   (outreachstudy.eu → apply site)
  Apply Click Rate:   {kpis['apply_click_rate']}%   (target ≥5%)
  Leads (lead_signup): {kpis['lead_signup']}   (reached /ask-us page)
  Lead Conv Rate:     {kpis['lead_conv_rate']}%   (apply visitors → leads)
  Website Lead Rate:  {kpis['website_lead_conv_rate']}%   (main visitors → leads)

MONTHLY PROGRESS TOWARD 300 LEADS
  Target:             {kpis['monthly_target']} leads
  MTD Leads:          {kpis['mtd_leads']} ({kpis['target_progress_pct']}% of target)
  Day {kpis['days_elapsed']} of {kpis['days_in_month']}
  Projected Total:    {kpis['projected_monthly_leads']} leads
  Required Pace:      {kpis['required_daily_pace']} leads/day to hit target
  Status:             {kpis['projection_status']}
""".strip()
