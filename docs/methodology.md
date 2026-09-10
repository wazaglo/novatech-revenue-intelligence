# How I built it and why

Notes to myself on what I actually did. Anything I claim here has a screenshot
or log entry in `deliverables/`.

## 1. I checked the numbers before I built anything

I ran the three Quick Chat knowledge bases and read the data dictionary first,
then redid every benchmark in pandas (`deliverables/ground_truth/`). The CSVs
didn't match the dictionary (499 vs 500 deals, 2,240 vs 2,200 campaign rows,
3,000 vs 2,995 tickets) so I stopped trusting either one and made the pandas
output my reference. Good thing too - Q later gave me an average deal size off
the joined table (see Q log #2).

What that meant after:
- Every check in the verification log uses rates and unique counts, not hardcoded
  totals, so it still holds if a row shifts.
- KPI cards pull from the **source** datasets, never the joined one.

## 2. Data quality findings (planted + real)

| Issue | Evidence | Handling |
|---|---|---|
| Auto-detected `deal_value`/`annual_income` as text | `screenshots/98_type_fix_step.png` | Type corrected to decimal in dataset edit (`99_type_fix_set.png`) |
| 3 duplicate `opportunity_id`, 4 duplicate `ticket_id` | ground_truth §2 | Counts deduplicate on read; documented in report §4 |
| 59 null `customer_sentiment` (dictionary says non-null) | ground_truth §3 | Donut shows explicit "Unknown"; `resolution_days` made null-tolerant |
| Orphan accounts ACCT-101-115 in marketing/support | ground_truth §4 | Left joins preserve all CRM rows; orphans disclosed in report |

## 3. The joined model and why it blows up

Join order: **CRM left join Marketing on `account_id`, then left join Support on `account_id`**.
I used left joins so a deal stays even if its account has no leads or tickets.

Grain is per account, so leads x tickets multiply: I added up
deals x leads x tickets per account by hand and got **63,420**. Refresh showed
63,420 (`screenshots/106-111_step3_*`). Exact hit.

Rule I stuck to after that:
- OK on the joined set: averages, distinct counts, rankings, shares.
- Not OK: any SUM - it runs high. So Sales/Marketing KPIs read from the
  source datasets, and the Customer Health sheet says this in the sheet itself.

## 4. Calculated fields I actually needed

- `days_to_close = dateDiff(close_date, created_date, MM)` - how fast deals close, null-safe.
- `campaign_roi_pct = (attributed_revenue - campaign_spend) / campaign_spend * 100`
  - all 6 programs negative (-83.7% to -97.7%). That was the headline.
- `resolution_days`, `resolved`, `tickets_last_30_days`, `customer_health_score`
  (0.5 recency / 0.3 volume / 0.2 sentiment) - wrote them in the glossary so Q
  and I meant the same thing.

## 5. One dashboard, three sheets (my first try was three dashboards)

The rubric wants one dashboard with 3 sheets, not three dashboards - I started
with three and had to merge. Order is risk, then pipeline, then spend. I only
put filters where someone would actually click:
- Customer Health (`priority`) and Sales Pipeline (`deal_stage`). That covers the
  "controls on 2+ sheets" bit and the two questions I kept getting: which tickets
  need a look now, which stage is stuck.
- One Navigation action on the priority chart to the Marketing Funnel. That's the
  jump an exec makes: risky account, what did we spend on them.
- 3 written annotations, one per sheet. Each states a number and what I'd do.

## 6. Q&A setup

Topic `WA - NovaTech Revenue Intelligence` (V2, all 4 datasets) holds the glossary
(revenue = Won `deal_value`, ROI/response/at-risk meanings, join warning).
I ran the same 3 questions before and after (`screenshots/qc_before*` vs `qc_after*`).
After the Topic the answers stopped guessing the dataset. My rule in the report:
**ask Q to poke around, quote the dashboard when it counts.**
