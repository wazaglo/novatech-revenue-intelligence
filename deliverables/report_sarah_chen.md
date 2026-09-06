# Revenue Intelligence Dashboard — Executive Summary

**To:** Sarah Chen, VP Sales & Marketing, NovaTech Solutions
**From:** BI Analytics
**Date:** 2026-09-05
**Platform:** Amazon Quick (Quick Suite) — QuickSight namespace `UdacityQuicksightLab`, us-west-2

## 1. Purpose

You asked for "the numbers, not just the data": a single revenue-intelligence view that connects **marketing spend → sales pipeline → customer health** so leadership can see where money is made and lost. One published dashboard with three sheets delivers this:

**WA - NovaTech Revenue Intelligence Dashboard** (dashboards/53e87aec-…-e1b3d6eaba55)

| Sheet | Purpose | Source |
|---|---|---|
| Sales Pipeline | Pipeline & win/loss KPIs | WA - NovaTech CRM Deals (499 rows) |
| Marketing Funnel | Campaign spend vs. return | WA - NovaTech Marketing Campaigns (2,240 rows) |
| Customer Health | Post-sale risk, built on the unified join | WA - NovaTech Unified Revenue Dataset |

A unified dataset joins all three CSVs on `account_id` (left join CRM⟕Marketing, then ⟕Support), preserving every deal even when an account has no leads or tickets. Exported PDFs of all three sheets are in `pdf/` (`dashboard_export.pdf` merges them).

## 2. Key KPIs (verified three ways: data dictionary ↔ Quick Chat ↔ dataset/dashboard)

- **Won revenue: $707,201** across **315 of 499 closed deals → 63.1% win rate.** Central region leads ($274K, 69.9% win rate).
- **Marketing is losing money: every one of the 6 campaign programs has negative ROI.** $12.36M spend vs $1.13M attributed revenue (−90.9% blended). Best channel: Direct Mail (53% response rate, −70.7% ROI). Worst: Organic Search / Email (−97.8% / −94.9%).
- **Customer health is concentrated risk: top account YieldMax (ACCT-041) has 334 tickets and $40.7K revenue — 4× the next ticket count.** 59 tickets unresolved (avg resolution 2.5 days); 684 negative-sentiment tickets.

## 3. Recommendations grounded in the data

1. **Rebalance campaign mix.** Pause or redesign Organic Search & Email (near-total loss, lowest response); pilot a Direct Mail budget increase — it converts at 53% but has the smallest volume (149 campaigns).
2. **Attack 'Pricing' as a loss reason** — it is the #1 reason deals are lost, followed by Product Fit; Central's playbook (69.9% win rate) should be lifted into East (57.8%).
3. **Rescue program for YieldMax, TrueNorth, LionGate, AlphaCore** — high ticket load on meaningful revenue; UltraLink is the clearest under-water account (140 tickets vs $7,950 revenue).

## 4. Data-quality caveats (found during ETL, all documented in the verification log)

- Planted **duplicate keys**: 3 `opportunity_id` and 4 `ticket_id` duplicates → deal/ticket counts deduplicate on read (496 unique opportunities, 2,996 unique tickets).
- **Undocumented nulls**: `customer_sentiment` has 59 missing values the data dictionary claims don't exist.
- **Orphan accounts** ACCT-101–115 in marketing/support; left joins keep CRM rows intact (150 marketing + 131 support rows hang off accounts with no deals).
- **Fan-out warning:** the unified 63,420-row model multiplies rows (leads × tickets per account). Averages/rankings/composition are safe on it; **sums are not** — which is why Sales and Marketing KPIs read from the single-source datasets and the Customer Health sheet states this in-sheet.

## 5. Q&A governance

A QuickSight/Quick Q&A Topic **"WA - NovaTech Revenue Intelligence"** (Version 2 Active) fronts all four datasets with a business glossary (revenue = Won deal_value; ROI, response-rate and at-risk definitions; known data-quality notes). Before/after comparisons (`screenshots/qc_before*` vs `qc_after*`) show the Topic making answers dataset-aware and fan-out-aware. Ask Q for exploration; quote the dashboard for governed numbers. Full exploration log: `q_exploration_log.md`. An auto-generated executive summary of the published dashboard is captured in `exec_summary.md`.

## 6. Using the dashboard

- **Filter controls** sit at the top of the Customer Health sheet (priority) and the Sales Pipeline sheet (deal_stage); selections re-filter every visual on the sheet — one-click exploration.
- Cross-sheet navigation: a Navigation action on the Customer Health sheet jumps to the Marketing Funnel sheet (menu/selection on the priority chart), so analysts can move risk → spend in one click.
- Cross-check any Q answer against the matching sheet before it enters a deck (see Q log cross-check column).
