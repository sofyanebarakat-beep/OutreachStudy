"""
OpenAI GPT-4o client.
Sends KPI data and returns structured analysis + recommendations.
"""

import json
import time
from openai import OpenAI
import config

SYSTEM_PROMPT = """You are a senior digital marketing analyst for OutreachStudy.eu —
a student recruitment company targeting African students (Ghana, Nigeria, Morocco, Uganda, Kenya)
who want to study English programs in Malta.

Business goal: Generate 300 leads per month from the apply.outreachstudy.eu platform.
A "lead" is a completed form submission (lead_signup event in GA4).

Your job: Analyze the daily KPI data and provide a clear, practical performance report.

Always respond in valid JSON with exactly these keys:
{
  "performance_score": <integer 1-10>,
  "summary": "<2-sentence overview of yesterday's performance>",
  "whats_working": ["<item>", "<item>", "<item>"],
  "whats_not_working": ["<item>", "<item>", "<item>"],
  "top_recommendation": "<single most important action to take today>",
  "lead_projection_status": "<On track | Slightly behind | Behind — action needed>",
  "action_items": ["1. <action>", "2. <action>", "3. <action>"],
  "full_analysis": "<3-4 paragraph detailed analysis>"
}

Rules:
- Be direct and specific. No generic marketing advice.
- Base all recommendations on the actual numbers provided.
- If lead_signup is 0, that is a critical problem — say so clearly.
- Always reference the 300/month target in your projection.
- If form_start > 0 but form_submit is low, flag the form abandonment.
- If engagement_rate < 35%, flag the content/UX issue.
- If organic traffic is growing, acknowledge it as a positive SEO signal.
"""


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)

    def test_connection(self) -> str:
        try:
            resp = self.client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[{"role": "user", "content": "Reply with: OK"}],
                max_tokens=5
            )
            return f"OpenAI connection OK ({config.OPENAI_MODEL})"
        except Exception as e:
            return f"OpenAI connection FAILED: {e}"

    def analyze(self, kpi_summary: str, kpis: dict, retries: int = 3) -> dict:
        user_message = f"""Analyze this KPI data for OutreachStudy.eu:

{kpi_summary}

Additional context:
- Yesterday's leads: {kpis.get('lead_signup', 0)}
- MTD leads: {kpis.get('mtd_leads', 0)} / {kpis.get('monthly_target', 300)}
- Projected monthly: {kpis.get('projected_monthly_leads', 0)}
- Required daily pace: {kpis.get('required_daily_pace', 0)} leads/day

Provide your analysis in the required JSON format."""

        for attempt in range(retries):
            try:
                resp = self.client.chat.completions.create(
                    model=config.OPENAI_MODEL,
                    messages=[
                        {"role": "system",  "content": SYSTEM_PROMPT},
                        {"role": "user",    "content": user_message},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3,
                    max_tokens=1500,
                )
                content = resp.choices[0].message.content
                analysis = json.loads(content)
                print(f"  OpenAI analysis complete. Score: {analysis.get('performance_score')}/10")
                return analysis

            except Exception as e:
                if attempt < retries - 1:
                    wait = 30 * (attempt + 1)
                    print(f"  OpenAI attempt {attempt+1} failed: {e}. Retrying in {wait}s…")
                    time.sleep(wait)
                else:
                    print(f"  OpenAI failed after {retries} attempts: {e}")
                    return self._fallback_analysis(kpis)

    def _fallback_analysis(self, kpis: dict) -> dict:
        leads = kpis.get("lead_signup", 0)
        proj  = kpis.get("projected_monthly_leads", 0)
        target = kpis.get("monthly_target", 300)
        status = "On track" if proj >= target * 0.95 else ("Slightly behind" if proj >= target * 0.75 else "Behind — action needed")
        return {
            "performance_score": 5,
            "summary": f"Analysis unavailable (API error). Yesterday: {leads} leads. MTD projection: {proj}.",
            "whats_working": ["Data collected successfully"],
            "whats_not_working": ["OpenAI analysis failed — check API key and quota"],
            "top_recommendation": "Check OpenAI API key and retry manually.",
            "lead_projection_status": status,
            "action_items": ["1. Check OpenAI API key", "2. Review raw KPIs in Daily_KPIs tab", "3. Run main.py manually"],
            "full_analysis": "OpenAI analysis failed. Please check the logs and retry.",
        }


if __name__ == "__main__":
    client = OpenAIClient()
    print(client.test_connection())
