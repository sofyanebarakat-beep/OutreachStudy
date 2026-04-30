# Auto-Agent Workflow for OutreachStudy

This workflow makes the marketing agents work together for SEO, SEM, competitors, content, outreach, and analytics.

## Main Goal
Generate leads for students who want to study in Malta.

## Agent Order

1. **Orchestrator Agent**
   - Receives the business goal
   - Sends tasks to each agent
   - Collects the final outputs

2. **Competitor Agent**
   - Finds competitors
   - Studies their keywords, ads, landing pages, and offers
   - Sends insights to SEO Agent and SEM Agent

3. **SEO Agent**
   - Builds keyword groups
   - Creates blog ideas
   - Creates landing page SEO structure
   - Sends keywords to Content Agent and SEM Agent

4. **SEM Agent**
   - Builds Google Ads and Meta Ads strategy
   - Allocates monthly budget
   - Creates campaigns, ad copy, and keyword targeting
   - Sends campaign plan to Analytics Agent

5. **Content Agent**
   - Creates blog outlines, landing page copy, lead magnets, and social content
   - Uses SEO keywords and competitor insights

6. **Outreach Agent**
   - Creates DM scripts, email scripts, WhatsApp scripts, and follow-up flows
   - Uses target audience and offers

7. **Analytics Agent**
   - Defines KPIs
   - Creates tracking plan
   - Reviews performance and gives optimization actions

## Output Files
Each agent should save its result in the correct folder:

- `marketing-system/research/competitor-analysis.md`
- `marketing-system/seo/keyword-research.md`
- `marketing-system/sem/ad-strategy.md`
- `marketing-system/content/content-plan.md`
- `marketing-system/outreach/outreach-scripts.md`
- `marketing-system/tracking/kpi-tracking.md`

## Simple Workflow

```text
User Goal
  ↓
Orchestrator Agent
  ↓
Competitor Agent
  ↓
SEO Agent + SEM Agent
  ↓
Content Agent + Outreach Agent
  ↓
Analytics Agent
  ↓
Final Marketing Action Plan
```

## Default Budget Split
For SEM, use this starting split unless another budget is given:

- 50% High-intent Google Search keywords
- 25% Competitor keyword campaigns
- 15% Retargeting ads
- 10% Testing new audiences and creatives

## Final Output Required
The orchestrator must produce:

1. Competitor summary
2. Keyword list
3. Ad campaign structure
4. Budget allocation
5. Landing page recommendation
6. Outreach messages
7. KPI tracking plan
8. Next 7-day action plan
