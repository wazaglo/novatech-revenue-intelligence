# NovaTech Data Verification Log

**Student Name:** BI Analyst, NovaTech Solutions  
**Date:** 2026-09-05

## Instructions

Query each pre-indexed knowledge base using Quick Chat. For each question, record the expected answer (from the data dictionary), Q's actual response, and whether they match. Minimum 6 entries (2 per data knowledge base).

## Verification Log

| # | Knowledge Base | Question Asked | Expected Answer | Q's Actual Answer | Match? | Notes |
|---|----------------|---------------|-----------------|-------------------|--------|-------|
| 1 | NovaTech CRM Deals | What is the total revenue from closed-won deals in the CRM dataset? | Sum of deal_value where deal_stage = Won = **$707,201** (315 won deals, data dictionary) | **$707,201 across 315 won deals** | PASS | Exact match. Screenshot: qc_v?/13_baseline_q1_answer.png |
| 2 | NovaTech CRM Deals | How many unique account_ids are in the CRM deals dataset? | **85** unique accounts (ACCT-001 to ACCT-085) | **85 unique account IDs** | PASS | Exact match |
| 3 | NovaTech Marketing Campaigns | How many leads responded positively (campaign_response = 1) and what is the overall response rate percentage? | **609 of 2,240 leads = 27.2%** | **609 positive responses, 2,240 total leads, 27.19%** | PASS | Q reports 27.19% vs dictionary's rounded 27.2% - same value |
| 4 | NovaTech Marketing Campaigns | What is the earliest and latest campaign_date in the marketing campaigns dataset? | **2023-01-01 to 2025-01-31** | **Earliest: January 1, 2023; Latest: January 31, 2025** | PASS | Exact match |
| 5 | NovaTech Support Tickets | How many support tickets have a missing ticket_resolved_date (unresolved tickets)? | **59** nulls (2.0%) per data dictionary | **59 tickets with missing ticket_resolved_date** | PASS | Exact match |
| 6 | NovaTech Support Tickets | Count the support tickets by priority level (critical, high, medium, low). | low=1500, medium=1050, high=400, critical=50 (dictionary) | **Low 1,500 / Medium 1,050 / High 400 / Critical 50; total 3,000** | PASS | Exact match on all four levels; total confirms 3,000 rows |
| 7 | NovaTech Reference Documents | According to the company background, how many active accounts does NovaTech serve and what are its two product lines? | **85 active accounts; NovaPulse (core) and NovaEdge (secondary)** | Q could not find a company background document - chat was scoped to the three CSV datasets only | FAIL (expected) | The chat scope was limited to the three CSV knowledge bases, which correctly excludes un-shared documents. Re-asked with the document in scope (see Notes). Demonstrates that scoped Q does not hallucinate answers it cannot source |

## Cross-Check

Pick one fact from above and confirm it independently in the QuickSight dataset preview.

- **Fact verified:** Support Tickets dataset contains 3,000 rows and the priority distribution low=1500 / medium=1050 / high=400 / critical=50
- **Chat said:** Low 1,500 / Medium 1,050 / High 400 / Critical 50 (total 3,000)
- **QuickSight shows:** The published SPICE dataset `novatech_support_tickets.csv` reports **3,000 dataset rows** on its Refresh tab (screenshot `118_refresh_novatech_support_tic.png`); CRM source reports 499 rows (`120_crm_source_rows.png`), marketing 2,240 (`118_refresh_novatech_marketing_c.png`), and the unified joined dataset 63,420 (`117_unified_refresh.png`) - matching the predicted join fan-out exactly. The Sales Pipeline dashboard KPI (Sum of deal_value on the CRM dataset) independently reproduces **$707,201** - the same figure Q returned and the data dictionary documents (`226_sales_dash_published.png`).
- **Consistent?** Yes - Quick Chat, the data dictionary, and the dataset preview all agree. Independent pandas check on the source CSV confirms the same counts.

## Extra data quirks (beyond the dictionary)

- **Duplicate keys:** 3 duped `opportunity_id` values in CRM (e.g., OPP-44760 appears on two different accounts) and 4 duped `ticket_id` values in Support. The dictionary calls these "unique identifiers," so I treated them as planted and deduped on read.
- **Nulls it doesn't mention:** `customer_sentiment` has 59 blanks in Support, but the dictionary lists "Nulls: None" for that field.
- **Orphans:** 150 marketing rows and 204 support rows reference ACCT-101-ACCT-115, which do not exist in CRM - I checked this in pandas too. They drop out under inner joins so I used left joins.

## Independent check (pandas on the source CSVs)

I redid every chat answer in pandas too (script `ground_truth/profile_data.py`, full output in `ground_truth/ground_truth.txt`): 499 CRM rows / 315 Won / $707,201 / 85 accounts; 2,240 leads / 609 responses (27.19%); 3,000 tickets / 59 unresolved / priority 1500-1050-400-50. Everything Q said lines up with both the dictionary and pandas.

## Dashboard ↔ chat consistency (post-build)

| Fact | Quick Chat said | Dashboard shows | Match |
|---|---|---|---|
| Total revenue | $707,201 (topic-scoped answer, `qc_after1_total_revenue.png`) | Sales Pipeline KPI **$707,201** (`226_sales_dash_published.png`, `pdf/sales_pipeline.pdf`) | Yes |
| Win rate | 63.75% on unified rows (`qc_after2_win_rate.png`) | 63.1% (315/499) in Sales sheet annotation - unified-row vs deduped-deal grain difference, documented in Q log #2 | Explained |
| Best/worst channels | DM 53.0% best, Email 8.7% worst (`qc_qlog1_channel_conversion.png`) | Marketing Funnel response-by-channel bar (`234_mkt_channel.png`, `pdf/marketing_funnel.pdf`) | Yes |
