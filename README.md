# NovaTech Revenue Intelligence Dashboard (Amazon Quick / QuickSight)

End-to-end BI project in the Udacity Vocareum lab: verified starter data, built an ETL + unified account-level model, published one 3-sheet interactive dashboard, configured a governed Q&A Topic, and cross-validated every number three ways (data dictionary ↔ Quick Chat ↔ dashboard/pandas).

**Submission package:** [`novatech_revenue_intelligence_submission.zip`](novatech_revenue_intelligence_submission.zip) — same contents as [`deliverables/`](deliverables).

## How it was done

### Step 1 — Baseline verification (before touching anything)
Queried the pre-indexed Quick Chat knowledge bases with 7 questions (2 per CSV KB + 1 document probe) and compared answers to the data dictionary. 6/6 PASS, 1 expected FAIL (document out of scope → proved scoped Q does not hallucinate). Every fact was *also* recomputed offline with pandas ([`deliverables/ground_truth/`](deliverables/ground_truth)) — this later caught a subtle Q discrepancy.
→ [`deliverables/verification_log.md`](deliverables/verification_log.md)

### Step 2 — Upload & data quality
Uploaded the 3 CSVs, fixed auto-detected types (`deal_value`, `annual_income` text→decimal), captured SPICE row counts on each dataset's Refresh tab (499 / 2,240 / 3,000). Discovered planted issues: duplicate `opportunity_id`/`ticket_id` keys, 59 undocumented null `customer_sentiment`, orphan accounts ACCT-101–115.

### Step 3 — Unified model
In Quick Data Prep: **CRM ⟕ Marketing on `account_id`, then ⟕ Support on `account_id`** (left joins so no deals drop). Added calculated fields `days_to_close` (`dateDiff`), `campaign_roi_pct`, `resolution_days` (null-tolerant), `at_risk_flag` (nested `ifelse`). Final row count **63,420 = exactly the predicted fan-out** Σ deals×leads×tickets per account — verified by pandas. Join diagram/config/type-fix/calcs: screenshots `55–99_*`.

### Step 4 — One dashboard, 3 sheets + Q&A Topic
- **Sales Pipeline** (CRM source): KPI **$707,201 won revenue** (matches ground truth to the dollar), revenue by region/loss-reason/company-tier, `deal_stage` filter control, quantified annotation.
- **Marketing Funnel** (MK source): spend-vs-revenue by campaign (all 6 negative ROI), response by channel, funnel-stage counts, `campaign_channel` control.
- **Customer Health** (unified join): average resolution by priority, sentiment donut, ticket volume by company, priority control, in-sheet grain disclosure.
- The three sheets live in ONE published dashboard, **WA - NovaTech Revenue Intelligence Dashboard** (filter controls on Customer Health + Sales Pipeline, cross-sheet navigation action, 3 quantified annotations, generative executive summary enabled). The auto-generated exec summary is captured in `deliverables/exec_summary.md`; PDFs exported per sheet and merged into [`pdf/dashboard_export.pdf`](deliverables/pdf/dashboard_export.pdf).
- Q&A Topic **"WA - NovaTech Revenue Intelligence"** over all 4 datasets with business glossary; before/after chat screenshots (`qc_before*` vs `qc_after*`) and the 5-question exploration log → [`deliverables/q_exploration_log.md`](deliverables/q_exploration_log.md).

**Key finding worth repeating:** Q answered "average deal size by company size" over the fan-out-joined table and got inflated-per-row averages, while the dashboard (correct source dataset) gives the true deduped numbers — see Q log entry #2 for why averages survive fan-out but sums don't, and how that drove the model design.

## Layout
```
deliverables/            submission package (logs, report, exec summary, PDFs, evidence screenshots, ground truth)
  README.md              rubric ↔ artifact map
novatech_revenue_intelligence_submission.zip
```

## Lab assets (us-west-2, namespace UdacityQuicksightLab)
Datasets SPICE (all "WA - " prefixed): 3 sources + unified account-level join · Dashboard **WA - NovaTech Revenue Intelligence Dashboard** `53e87aec-721e-491e-8436-e1b3d6eaba55` (sheets: Customer Health, Sales Pipeline, Marketing Funnel) · Topic **WA - NovaTech Revenue Intelligence** (V2 Active)
