# NovaTech Revenue Intelligence Dashboard — Submission Manifest

## Contents (zip root)

| Rubric requirement | Where |
|---|---|
| Verification log (≥6 entries, all three KBs, template format) | `verification_log.md` — 7 entries + cross-check + pandas appendix |
| Data transformation screenshots (join diagram, join config, calculated fields, data-type corrections) | `screenshots/5x–99_*`: `79_join1_added`, `84_join1_full_config`, `88_join2_full`, `89_join2_preview` (join diagram), `90–93_u_calc*` (calculated fields), `98/99_type_fix*` (data types), `24–48_*` (source-dataset type fixes & calcs) |
| Dashboard PDF export — all 3 sheets | `pdf/dashboard_export.pdf` (merged: sales_pipeline.pdf + marketing_funnel.pdf + customer_health.pdf); per-sheet PDFs alongside |
| Dashboard screenshots (published, filters, annotations) | `screenshots/225–226` (Sales KPI $707,201 + filter control), `231–240` (Marketing), `248–251` (Customer Health), `171/208/238` (filter controls), `219/239/250` (annotations) |
| Before/after Topic screenshots (same 3 questions) | `screenshots/qc_before1_total_revenue / before2_win_rate / before3_campaign_perf` vs `qc_after1_total_revenue / after2_win_rate / after3_campaign_perf`; Topic build: `253–264`, scoping: `269–275` |
| Q Exploration Log (≥5 entries, all 3 domains, dashboard cross-check) | `q_exploration_log.md` + `screenshots/qc_qlog1..5_*` |
| Dashboard executive summary | `report_sarah_chen.md` (auto executive summary is also enabled on all three published dashboards) |
| Baseline Quick Chat verification evidence | `screenshots/12–13_baseline*`, `qc_v2..v7_*` |
| Independent ground truth | `ground_truth/ground_truth.txt` + `ground_truth/profile_data.py` |
| Full build evidence trail | `screenshots/00–275_*` (login → upload → ETL → modeling → dashboards → Q&A) |

## Published lab assets (namespace UdacityQuicksightLab, us-west-2)

- Datasets (SPICE): novatech_crm_deals.csv (499), novatech_marketing_campaigns.csv (2,240), novatech_support_tickets.csv (3,000), unified join novatech_crm_deals.csv (63,420)
- Dashboards: NovaTech Sales Pipeline (054c808a-…78dc3ffe86b4), NovaTech Marketing Funnel (48b9920d-…73faf07ae61b), NovaTech Customer Health (5e0b028a-…6922649889de)
- Q&A Topic: NovaTech Revenue Intelligence (V1 Active, 4 datasets, business glossary)
