# Methodology & Design Decisions

Why the project was built the way it is. Every claim here is backed by an artifact in
`deliverables/` (screenshot id or log entry).

## 1. Verify first, build second

Before touching any configuration I queried the three pre-indexed Quick Chat knowledge
bases and the data dictionary, then recomputed every benchmark number offline with pandas
(`deliverables/ground_truth/`). Only after the row counts in the starter CSVs disagreed
with the course data dictionary (499 vs 500 deals, 2,240 vs 2,200 campaign rows, 3,000 vs
2,995 tickets) did I commit to a ground-truth file as the single source of truth for the
whole project. This caught a Quick Chat answer that confidently reported an average deal
size computed over a fan-out-joined table — see Q log entry #2 and the fan-out section below.

Consequences that shaped everything downstream:
- Every benchmark in the verification log is **row-count agnostic** (`unique won deals /
  total deals`, not hardcoded totals).
- KPI cards bind to measures defined from the **source** datasets, never the joined model.

## 2. Data quality findings (planted + real)

| Issue | Evidence | Handling |
|---|---|---|
| Auto-detected `deal_value`/`annual_income` as text | `screenshots/98_type_fix_step.png` | Type corrected to decimal in dataset edit (`99_type_fix_set.png`) |
| 3 duplicate `opportunity_id`, 4 duplicate `ticket_id` | ground_truth §2 | Counts deduplicate on read; documented in report §4 |
| 59 null `customer_sentiment` (dictionary says non-null) | ground_truth §3 | Donut shows explicit "Unknown"; `resolution_days` made null-tolerant |
| Orphan accounts ACCT-101–115 in marketing/support | ground_truth §4 | Left joins preserve all CRM rows; orphans disclosed in report |

## 3. The unified model: grain and fan-out

Join order: **CRM ⟕ Marketing on `account_id`, then ⟕ Support on `account_id`**
(left joins; every deal survives even without leads or tickets).

Account-level grain ⇒ a Cartesian product per account between its leads and its tickets:
predicted unified rows Σ(deals×leads×tickets per account) = **63,420**, matched exactly on
refresh (`screenshots/106–111_step3_*`).

Design rule derived from that number:
- **Safe on the unified set:** averages, counts-distinct, rankings, composition.
- **Unsafe:** any SUM (inflated by fan-out). Sales/Marketing KPIs therefore read from the
  single-source datasets; the Customer Health sheet states the grain in-sheet.

## 4. Calculated fields — chosen to test real semantics

- `days_to_close = dateDiff(close_date, created_date, MM)` — pipeline velocity, null-safe.
- `campaign_roi_pct = (attributed_revenue - campaign_spend) / campaign_spend * 100`
  — every one of the 6 programs is negative (−83.7%…−97.7%): the headline finding.
- `resolution_days`, `resolved`, `tickets_last_30_days`, `customer_health_score`
  (weights 0.5 recency / 0.3 volume / 0.2 sentiment) — documented in the glossary so Q
  and humans agree on definitions.

## 5. One dashboard, three sheets (not three dashboards)

The rubric asks for a single 3-sheet dashboard (Marketing Funnel / Sales Pipeline /
Customer Health). Sheets are ordered journey-first: risk → pipeline → spend. Interaction
budget spent deliberately:
- Filter controls on Customer Health (`priority`) and Sales Pipeline (`deal_stage`) —
  satisfies "controls on ≥2 sheets" where they answer the two questions leadership asks
  ("which tickets now?", "which stage is at risk?").
- One cross-sheet **Navigation action** on the priority chart → Marketing Funnel: the
  risk-to-spend jump an exec actually asks for.
- 3 quantified annotations (one per sheet), each naming the number and the action.

## 6. Q&A governance

Topic `WA - NovaTech Revenue Intelligence` (V2, all 4 datasets) carries the business
glossary (revenue = Won `deal_value`, ROI/response/at-risk definitions, fan-out warning).
Before/after runs of the same 3 questions (`screenshots/qc_before*` vs `qc_after*`) show
the Topic converting vague answers into dataset-aware ones. Standing rule in the report:
**ask Q to explore, quote the dashboard to decide.**
