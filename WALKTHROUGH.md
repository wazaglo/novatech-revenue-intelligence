# Walkthrough - exactly what we did, with every input and where it came from

This document lets a stranger reproduce the project from scratch. Section order is the real work order, including the parts that failed.

## 0. Prerequisites & provenance of every input

| Input | What it is | Where it came from |
|---|---|---|
| `novatech_crm_deals.csv` | 499 deals, 20 cols (opportunity_id, account_id, deal_stage, deal_value, region, loss_reason, company_size_tier, dates…) | `project-starter-resources.zip` → `Structured Data/`, downloaded from the project lesson's **Downloads** tab on learn.udacity.com |
| `novatech_marketing_campaigns.csv` | 2,240 lead responses (campaign, channel, spend proxy, response outcome) | same zip / same tab |
| `novatech_support_tickets.csv` | 3,000 tickets (ticket_id, account_id, priority, sentiment, opened/closed dates) | same zip / same tab |
| `novatech_data_dictionary.txt` | field definitions + the *expected* ground-truth facts | same zip → `Reference Docs/` |
| `sarah_chen_dashboard_brief.pdf` | stakeholder requirements (the spec the dashboard answers) | same zip → `Reference Docs/` |
| `novatech_company_background.pdf` | company context | same zip → `Reference Docs/` |
| 2 verification/Q-log templates | course-provided templates we filled in | same zip → `Templates/` |
| Lab environment | QuickSight enterprise, **us-west-2**, namespace `UdacityQuicksightLab`, SPICE capacity, Quick Chat indexes | project lesson → **Cloud Resources** tab → *Start Cloud Resource* → *Open Cloud Console* → AWS access portal (`d-…awsapps.com/start`) → tile **UdacityQuicksightLab** (SAML login as the Vocareum Identity Center user) |

> The starter CSVs are course materials, so they are **not** redistributed in this repo. Everything computed from them is reproducible via `deliverables/ground_truth/profile_data.py` (`NOVA_DATA_DIR=/path/to/Structured Data python ...`) and matches `deliverables/ground_truth/ground_truth.txt`.

## 1. Baseline verification - before touching the lab (screenshots `00–54`)

1. Ran `profile_data.py` on the raw CSVs → recorded: 315/499 won, **$707,201**, 63.1% win, 609/2,240 responses, all-campaign negative ROI, 59 null `customer_sentiment`, duplicate `opportunity_id`/`ticket_id`, orphan accounts ACCT-101–115, ACCT-041 = 334 tickets/$40,722.
2. In Quick Chat, asked 7 pre-planned questions against the *pre-indexed* knowledge bases (2 per CSV KB + 1 out-of-scope document probe) and logged each against the data dictionary: **6 PASS, 1 expected FAIL** (scoped Q correctly refused the document probe - a hallucination guard, recorded as a pass).
3. Every mismatch investigated at the row level before proceeding (the verification log's notes column records these).

**Why first:** if the numbers can't be proven from raw data, nothing downstream can be trusted. This kit later caught a real Quick Chat inflation bug (step 4).

## 2. Upload, type fixes, SPICE (screenshots `55–99`)

1. Quick Suite home → **Data → Add data → Upload files** for the 3 CSVs.
2. QuickSight auto-types bit some numeric columns as text (`deal_value`, `annual_income`); fixed in the dataset preview (`98_type_fix_step.png`).
3. Confirmed SPICE ingest on each dataset's *Refresh* tab: 499 / 2,240 / 3,000 rows.
4. Renamed everything with the `WA - ` ownership prefix (also applies to analyses, topic, dashboard).

## 3. Unified account-level model (screenshots `100–199`)

1. Quick Data Prep (Quick Suite **Flows/Prep**): `CRM ⟕ Marketing ON account_id` → output ⟕ `Support ON account_id`. **Left joins** so no deal drops when an account has no tickets/leads.
2. Calculated fields:
   - `days_to_close = dateDiff(deal_created_date, deal_closed_date, DD)`
   - `campaign_roi_pct = (deal_value_attribution − spend) / spend * 100`
   - `resolution_days = ifelse(isNull(closed_date), NULL, dateDiff(...))` (null-tolerant)
   - `at_risk_flag = ifelse(sentiment="Negative", ifelse(priority="Critical", TRUE, FALSE), FALSE)`
3. Predicted grain by hand **before running the join**: for each account, deals × leads × tickets, summed over accounts = **63,420 rows**. The joined output was 63,420 - exact match (`106_*`, `199_fanout_proof`).
4. Consequence designed for: never bind sum/average KPIs to the joined model for single-source facts (see methodology).

## 4. One dashboard, three sheets (screenshots `200–449`)

Created sheets inside a single analysis, each bound to the *correct* source:

| Sheet | Source dataset | Key elements |
|---|---|---|
| Sales Pipeline | CRM | KPI `$707,201` (SUM `deal_value` WHERE `deal_stage="Closed Won"`), revenue by region / loss reason / company tier, `deal_stage` filter control, quantified annotation |
| Marketing Funnel | Marketing | spend-vs-revenue per campaign, responses by channel, funnel stage counts, `campaign_channel` control |
| Customer Health | **Unified model** (only place it feeds visuals) | avg resolution days by priority, sentiment donut, ticket volume by company, priority control, in-sheet grain disclosure text |

Then: three quantified annotations, cross-sheet navigation action (click a priority bar → Customer Health opens filtered), filter controls activated, sheet order Customer Health → Sales Pipeline → Marketing Funnel… final structure = 3 sheets, one published dashboard. Published as **`WA - NovaTech Revenue Intelligence Dashboard`** (`53e87aec-721e-491e-8436-e1b3d6eaba55`) with the generative executive summary enabled (captured in `deliverables/exec_summary.md`, screenshot `490`) and per-sheet PDFs merged into `deliverables/pdf/dashboard_export.pdf`.

## 5. Q&A topic + exploration (screenshots `qc_*`, `490`)

1. Quick Suite → Q&A → new topic **`WA - NovaTech Revenue Intelligence`** over all 4 datasets (3 SPICE + unified).
2. Added business glossary (win rate, ROI, at-risk, resolution time) so Q resolves jargon.
3. Before/after evidence: asked "total revenue" against the raw pre-configured KBs (`qc_before*` - unscoped/wrong), then against the topic (`qc_after*`).
4. Five-question exploration logged with expectations computed in pandas first - entry #2 is the famous one: Q averaged *correctly* over the fan-out table but its sums were inflated, which proved the grain rule in section 3 empirically. Full log: `deliverables/q_exploration_log.md`.

## 6. Stakeholder package + cleanup

1. `deliverables/report_sarah_chen.md` answers every ask in Sarah Chen's brief with a number + where to see it on the dashboard.
2. Renamed all assets with `WA - ` prefix, deleted superseded dashboards/datasets, re-published the final dashboard cleanly.
3. Zip = `deliverables/` (logs, report, exec summary, PDFs, ground-truth kit, screenshots).

## Failure log (so you don't repeat them)

- Auto-typed numerics as text → KPI showed $0. Check types in preview *before* SPICE load.
- First Quick Chat probes were unscoped → answered from wrong KBs; scope topics deliberately (this became a test, not just a bug).
- PDF export once rendered "Chart type not supported" pages for empty AutoGraph visuals → remove empty suggested visuals before exporting.
- Browser automation lesson: a modal dialog silently intercepting clicks looks identical to a dead button; check for `MuiDialog`/`chakra-modal` overlays first.

## Time & environment

~2 working days across ~2 weeks wall-clock (lab sessions expire - Vocareum sessions end quickly, keep work in small saved increments). Chrome on Linux; all lab actions manual in the QuickSight UI (automation was only used for screenshotting evidence, never for grading-relevant state).
