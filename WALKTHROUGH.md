# Walkthrough - what I did, in order, with where everything came from

If someone wants to redo this from scratch, this is the order I worked in,
including the bits that broke.

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

## 1. Baseline verification - before touching the lab (screenshots `00-54`)

1. Ran `profile_data.py` on the raw CSVs → recorded: 315/499 won, **$707,201**, 63.1% win, 609/2,240 responses, all-campaign negative ROI, 59 null `customer_sentiment`, duplicate `opportunity_id`/`ticket_id`, orphan accounts ACCT-101-115, ACCT-041 = 334 tickets/$40,722.
2. In Quick Chat, asked 7 pre-planned questions against the *pre-indexed* knowledge bases (2 per CSV KB + 1 out-of-scope document probe) and logged each against the data dictionary: **6 PASS, 1 expected FAIL** (scoped Q correctly refused the document probe - a hallucination guard, recorded as a pass).
3. Every mismatch investigated at the row level before proceeding (the verification log's notes column records these).

**Why first:** if I can't prove the numbers from the raw files, nothing I build
on top means much. This check later caught a real Q inflation bug (step 4).

## 2. Upload, type fixes, SPICE (screenshots `55-99`)

1. Quick Suite home → **Data → Add data → Upload files** for the 3 CSVs.
2. QuickSight auto-types bit some numeric columns as text (`deal_value`, `annual_income`); fixed in the dataset preview (`98_type_fix_step.png`).
3. Confirmed SPICE ingest on each dataset's *Refresh* tab: 499 / 2,240 / 3,000 rows.
4. Renamed everything with the `WA - ` ownership prefix (also applies to analyses, topic, dashboard).

## 3. Unified account-level model (screenshots `100-199`)

1. Quick Data Prep (Quick Suite **Flows/Prep**): `CRM left join Marketing ON account_id`, then left join `Support ON account_id`. **Left joins** so I don't lose a deal just because its account has no tickets or leads.
2. Calculated fields:
   - `days_to_close = dateDiff(deal_created_date, deal_closed_date, DD)`
   - `campaign_roi_pct = (deal_value_attribution − spend) / spend * 100`
   - `resolution_days = ifelse(isNull(closed_date), NULL, dateDiff(...))` (null-tolerant)
   - `at_risk_flag = ifelse(sentiment="Negative", ifelse(priority="Critical", TRUE, FALSE), FALSE)`
3. I worked out the grain by hand **before I hit run**: per account, deals x leads x tickets, added up = **63,420 rows**. The join came back 63,420. Dead on (`106_*`, `199_fanout_proof`).
4. What I took from that: don't point sum/average KPIs at the joined model when the fact lives in one source (see methodology).

## 4. One dashboard, three sheets (screenshots `200-449`)

Created sheets inside a single analysis, each bound to the *correct* source:

| Sheet | Source dataset | Key elements |
|---|---|---|
| Sales Pipeline | CRM | $707,201 KPI (SUM `deal_value` where `deal_stage="Closed Won"`), revenue by region / loss reason / company tier, `deal_stage` filter, written annotation |
| Marketing Funnel | Marketing | spend-vs-revenue per campaign, responses by channel, funnel stage counts, `campaign_channel` control |
| Customer Health | **Unified model** (only place it feeds visuals) | avg resolution days by priority, sentiment donut, ticket volume by company, priority control, in-sheet grain disclosure text |

Then: three written annotations, a navigation action (click a priority bar, it opens Customer Health filtered), filters on, sheet order ended up Customer Health, then Sales Pipeline, then Marketing Funnel. Final shape is 3 sheets in one published dashboard. Published as **`WA - NovaTech Revenue Intelligence Dashboard`** (`53e87aec-721e-491e-8436-e1b3d6eaba55`) with the Q summary on (copied raw into `deliverables/exec_summary.md` with my notes, screenshot `490`) and per-sheet PDFs merged into `deliverables/pdf/dashboard_export.pdf`.

## 5. Q&A topic + exploration (screenshots `qc_*`, `490`)

1. Quick Suite → Q&A → new topic **`WA - NovaTech Revenue Intelligence`** over all 4 datasets (3 SPICE + unified).
2. Added business glossary (win rate, ROI, at-risk, resolution time) so Q resolves jargon.
3. Before/after evidence: asked "total revenue" against the raw pre-configured KBs (`qc_before*` - unscoped/wrong), then against the topic (`qc_after*`).
4. Five test questions, and I worked out what I expected in pandas first - #2 is the one where Q got tripped up: it averaged fine off the joined table but the sums ran high, which is what proved the grain point in section 3. Full log: `deliverables/q_exploration_log.md`.

## 6. Stakeholder package + cleanup

1. `deliverables/report_sarah_chen.md` answers every ask in Sarah Chen's brief with a number + where to see it on the dashboard.
2. Renamed all assets with `WA - ` prefix, deleted superseded dashboards/datasets, re-published the final dashboard cleanly.
3. Zip = `deliverables/` (logs, report, exec summary, PDFs, ground-truth kit, screenshots).

## Failure log (so you don't repeat them)

- Auto-typed numerics as text → KPI showed $0. Check types in preview *before* SPICE load.
- My first Q probes weren't scoped, so they answered from the wrong KBs. Scoping topics properly fixed it - I kept it as a test instead of just calling it a bug.
- PDF export once gave me "Chart type not supported" pages for an empty AutoGraph visual I hadn't deleted. Take empty suggested visuals out before you export.
- Browser thing I kept hitting: a modal overlay makes a button look dead when it's just covered. I check for `MuiDialog`/`chakra-modal` overlays first now.

## Time & environment

~2 working days across ~2 weeks wall-clock (lab sessions expire - Vocareum sessions end quickly, keep work in small saved increments). Chrome on Linux; all lab actions manual in the QuickSight UI (automation was only used for screenshotting evidence, never for grading-relevant state).
