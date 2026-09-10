# NovaTech Revenue Intelligence Dashboard - Submission Manifest

## Contents (zip root)

| Rubric requirement | Where |
|---|---|
| Verification log (≥6 entries, all three KBs, template format) | `verification_log.md` - 7 entries + cross-check + pandas appendix |
| Data transformation screenshots (join diagram, join config, calculated fields, data-type corrections) | `screenshots/5x-99_*`: `79_join1_added`, `84_join1_full_config`, `88_join2_full`, `89_join2_preview` (join diagram), `90-93_u_calc*` (calcs), `98/99_type_fix*` (types), `24-48_*` (source fixes) |
| Dashboard PDF export - all 3 sheets | `pdf/dashboard_export.pdf` (3 pages: Customer Health + Sales Pipeline + Marketing Funnel from the published dashboard); per-sheet PDFs alongside |
| Dashboard screenshots (published, filters, annotations, navigation) | `434/435/478` (published 3-sheet dashboard), `440_dash_*` (each sheet), `461` (deal_stage filter control), `171/208/238` (filter controls in action), `219/239/250` + `406/407` (annotations), `414/415` (navigation action config), `480/481` (navigation click → sheet jump) |
| Before/after Topic screenshots (same 3 questions) | `screenshots/qc_before1_total_revenue / before2_win_rate / before3_campaign_perf` vs `qc_after1_total_revenue / after2_win_rate / after3_campaign_perf`; Topic build: `253-264` + `346-355` (WA rename), scoping: `269-275` |
| Q Exploration Log (≥5 entries, all 3 domains, dashboard cross-check) | `q_exploration_log.md` + `screenshots/qc_qlog1..5_*` |
| Dashboard executive summary | `exec_summary.md` (raw Q summary + my notes on the inflated counts; `screenshots/490_chat_summary.png`) + `report_sarah_chen.md` (my written report) |
| Baseline Quick Chat checks | `screenshots/12-13_baseline*`, `qc_v2..v7_*` |
| Independent ground truth | `ground_truth/ground_truth.txt` + `ground_truth/profile_data.py` |
| Full build trail | `screenshots/00-529_*` (login to upload to modeling to dashboards to Q&A to rename/publish) |

## Published lab assets (namespace UdacityQuicksightLab, us-west-2)

- Datasets (SPICE, all prefixed "WA - "): WA - NovaTech CRM Deals (499), WA - NovaTech Marketing Campaigns (2,240), WA - NovaTech Support Tickets (3,000), WA - NovaTech Unified Revenue Dataset (account-level join)
- Dashboard: **WA - NovaTech Revenue Intelligence Dashboard** (53e87aec-…-e1b3d6eaba55) - single dashboard, 3 sheets: Customer Health, Sales Pipeline, Marketing Funnel; executive summary + Q&A enabled; filter controls on Customer Health (priority) and Sales Pipeline (deal_stage); cross-sheet Navigation action Customer Health → Marketing Funnel
- Analysis: WA - NovaTech Revenue Intelligence (1eb14303-…) with the same 3 sheets
- Q&A Topic: WA - NovaTech Revenue Intelligence (V2 Active, 4 datasets, short glossary)
- Note on the joined dataset: it's an account-level join, so row counts blow up per deal x ticket and sums off it run high. Sales/Marketing KPIs use the source datasets instead (see report section 4)
