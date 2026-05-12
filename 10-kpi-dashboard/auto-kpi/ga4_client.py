"""
GA4 Data API client.
Pulls metrics from both outreachstudy.eu and apply.outreachstudy.eu.
"""

from datetime import date, timedelta
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest, DateRange, Metric, Dimension,
    OrderBy, FilterExpression, Filter,
)
from auth import get_credentials
import config


class GA4Client:
    def __init__(self):
        creds = get_credentials()
        self.client = BetaAnalyticsDataClient(credentials=creds)

    def test_connection(self):
        try:
            self._run(config.GA4_PROPERTY_MAIN, "yesterday", "yesterday", metrics=["sessions"], dimensions=[])
            return "GA4 connection OK"
        except Exception as e:
            return f"GA4 connection FAILED: {e}"

    def _run(self, property_id, start, end, metrics, dimensions, order_metric=None, limit=20, dim_filter=None):
        req = RunReportRequest(
            property=property_id,
            date_ranges=[DateRange(start_date=start, end_date=end)],
            metrics=[Metric(name=m) for m in metrics],
            dimensions=[Dimension(name=d) for d in dimensions],
            limit=limit,
        )
        if order_metric:
            req.order_bys = [OrderBy(metric=OrderBy.MetricOrderBy(metric_name=order_metric), desc=True)]
        if dim_filter:
            req.dimension_filter = dim_filter
        return self.client.run_report(req)

    def _val(self, row, i, cast=float):
        try:
            return cast(row.metric_values[i].value)
        except (IndexError, ValueError):
            return 0

    def _dim(self, row, i):
        try:
            return row.dimension_values[i].value
        except IndexError:
            return ""

    # ──────────────────────────────────────────
    # OVERVIEW METRICS
    # ──────────────────────────────────────────
    def get_overview(self, property_id: str, start: str, end: str) -> dict:
        resp = self._run(
            property_id, start, end,
            metrics=["totalUsers", "sessions", "newUsers", "screenPageViews",
                     "engagementRate", "averageSessionDuration", "engagedSessions"],
            dimensions=[]
        )
        row = resp.rows[0] if resp.rows else None
        if not row:
            return {k: 0 for k in ["users", "sessions", "new_users", "pageviews",
                                    "engagement_rate", "avg_session_duration_sec", "engaged_sessions"]}
        return {
            "users":                  int(self._val(row, 0)),
            "sessions":               int(self._val(row, 1)),
            "new_users":              int(self._val(row, 2)),
            "pageviews":              int(self._val(row, 3)),
            "engagement_rate":        round(self._val(row, 4) * 100, 2),
            "avg_session_duration_sec": round(self._val(row, 5), 1),
            "engaged_sessions":       int(self._val(row, 6)),
        }

    # ──────────────────────────────────────────
    # TRAFFIC SOURCES
    # ──────────────────────────────────────────
    def get_traffic_sources(self, property_id: str, start: str, end: str) -> dict:
        resp = self._run(
            property_id, start, end,
            metrics=["sessions", "totalUsers"],
            dimensions=["sessionDefaultChannelGrouping"],
            order_metric="sessions",
            limit=20
        )
        result = {
            "organic": 0, "paid": 0, "direct": 0,
            "referral": 0, "social": 0, "other": 0,
            "rows": []
        }
        for row in resp.rows:
            ch = self._dim(row, 0).lower()
            s  = int(self._val(row, 0))
            u  = int(self._val(row, 1))
            result["rows"].append({"channel": self._dim(row, 0), "sessions": s, "users": u})
            if "organic search" in ch:    result["organic"]  += s
            elif "paid" in ch or "cpc" in ch: result["paid"] += s
            elif "direct" in ch:          result["direct"]   += s
            elif "referral" in ch:        result["referral"] += s
            elif "social" in ch:          result["social"]   += s
            else:                         result["other"]    += s
        return result

    # ──────────────────────────────────────────
    # CUSTOM EVENTS
    # ──────────────────────────────────────────
    def get_events(self, property_id: str, start: str, end: str) -> dict:
        dim_filter = FilterExpression(
            filter=Filter(
                field_name="eventName",
                in_list_filter=Filter.InListFilter(values=config.CUSTOM_EVENTS)
            )
        )
        resp = self._run(
            property_id, start, end,
            metrics=["eventCount", "totalUsers"],
            dimensions=["eventName"],
            order_metric="eventCount",
            limit=50,
            dim_filter=dim_filter
        )
        counts = {e: 0 for e in config.CUSTOM_EVENTS}
        for row in resp.rows:
            name = self._dim(row, 0)
            if name in counts:
                counts[name] = int(self._val(row, 0))
        return counts

    # ──────────────────────────────────────────
    # TOP PAGES
    # ──────────────────────────────────────────
    def get_top_pages(self, property_id: str, start: str, end: str, limit: int = 10) -> list:
        resp = self._run(
            property_id, start, end,
            metrics=["screenPageViews", "totalUsers", "averageSessionDuration", "engagementRate"],
            dimensions=["pagePath", "pageTitle"],
            order_metric="screenPageViews",
            limit=limit
        )
        pages = []
        for row in resp.rows:
            pages.append({
                "path":             self._dim(row, 0),
                "title":            self._dim(row, 1),
                "views":            int(self._val(row, 0)),
                "users":            int(self._val(row, 1)),
                "avg_duration_sec": round(self._val(row, 2), 1),
                "engagement_rate":  round(self._val(row, 3) * 100, 2),
            })
        return pages

    # ──────────────────────────────────────────
    # COUNTRY BREAKDOWN
    # ──────────────────────────────────────────
    def get_countries(self, property_id: str, start: str, end: str, limit: int = 10) -> list:
        resp = self._run(
            property_id, start, end,
            metrics=["sessions", "totalUsers"],
            dimensions=["country"],
            order_metric="sessions",
            limit=limit
        )
        return [
            {
                "country": self._dim(row, 0),
                "sessions": int(self._val(row, 0)),
                "users":    int(self._val(row, 1)),
                "target_market": self._dim(row, 0) in config.TARGET_COUNTRIES,
            }
            for row in resp.rows
        ]

    # ──────────────────────────────────────────
    # MONTH-TO-DATE LEAD COUNT
    # ──────────────────────────────────────────
    def get_mtd_leads(self, property_id: str) -> int:
        today = date.today()
        start = today.replace(day=1).strftime("%Y-%m-%d")
        end   = (today - timedelta(days=1)).strftime("%Y-%m-%d")
        if start > end:
            return 0
        events = self.get_events(property_id, start, end)
        return events.get("lead_signup", 0)

    # ──────────────────────────────────────────
    # FULL DAILY PULL (both sites)
    # ──────────────────────────────────────────
    def pull_all(self, target_date: date = None) -> dict:
        if target_date is None:
            target_date = date.today() - timedelta(days=1)
        start = end = target_date.strftime("%Y-%m-%d")

        print(f"  Pulling GA4 data for {start}…")

        main_overview  = self.get_overview(config.GA4_PROPERTY_MAIN,  start, end)
        main_traffic   = self.get_traffic_sources(config.GA4_PROPERTY_MAIN,  start, end)
        main_events    = self.get_events(config.GA4_PROPERTY_MAIN,  start, end)
        main_pages     = self.get_top_pages(config.GA4_PROPERTY_MAIN,  start, end)
        main_countries = self.get_countries(config.GA4_PROPERTY_MAIN,  start, end)

        apply_overview  = self.get_overview(config.GA4_PROPERTY_APPLY, start, end)
        apply_traffic   = self.get_traffic_sources(config.GA4_PROPERTY_APPLY, start, end)
        apply_events    = self.get_events(config.GA4_PROPERTY_APPLY, start, end)
        apply_pages     = self.get_top_pages(config.GA4_PROPERTY_APPLY, start, end)

        mtd_leads = self.get_mtd_leads(config.GA4_PROPERTY_APPLY)

        print(f"  GA4 pull complete. MTD leads: {mtd_leads}")

        return {
            "date":  start,
            "main":  {"overview": main_overview,  "traffic": main_traffic,
                      "events": main_events,       "pages": main_pages,
                      "countries": main_countries},
            "apply": {"overview": apply_overview,  "traffic": apply_traffic,
                      "events": apply_events,       "pages": apply_pages},
            "mtd_leads": mtd_leads,
        }


if __name__ == "__main__":
    client = GA4Client()
    print(client.test_connection())
