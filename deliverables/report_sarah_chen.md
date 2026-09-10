# Revenue Intelligence Dashboard - Executive Summary

**To:** Sarah Chen, VP Sales & Marketing, NovaTech Solutions
**From:** BI Analytics
**Date:** 2026-09-05
**Platform:** Amazon Quick (Quick Suite) - QuickSight namespace `UdacityQuicksightLab`, us-west-2

## 1. Purpose

You asked for "the numbers, not just the data": one view that ties marketing spend
to pipeline to customer health, so you can see where money is made and lost.
I published one dashboard with three sheets for that:

**WA - NovaTech Revenue Intelligence Dashboard** (dashboards/53e87aec-…-e1b3d6eaba55)

| Sheet | Purpose | Source |
|---|---|---|
| Sales Pipeline | Pipeline & win/loss KPIs | WA - NovaTech CRM Deals (499 rows) |
| Marketing Funnel | Campaign spend vs. return | WA - NovaTech Marketing Campaigns (2,240 rows) |
| Customer Health | Post-sale risk, built on the unified join | WA - NovaTech Unified Revenue Dataset |

A joined dataset ties all three CSVs on `account_id` (CRM left join Marketing, then left join Support). Left joins so no deal drops when an account has no leads or tickets. PDFs of all three sheets are in `pdf/` (`dashboard_export.pdf` merges them).

## 2. Key KPIs (I checked each in the dictionary, in Quick Chat, and in pandas/the dashboard)

- **Won revenue: $707,201** across **315 of 499 deals, 63.1% win rate.** Central leads ($274K, 69.9% win rate).
- **Marketing is losing money: all 6 programs negative.** $12.36M spend vs $1.13M attributed (-90.9% blended). Best of a bad lot: Direct Mail (53% response, -70.7% ROI). Worst: Organic Search / Email (-97.8% / -94.9%).
- **Risk sits in a few accounts: YieldMax (ACCT-041) has 334 tickets on $40.7K revenue, about 4x the next count.** 59 tickets still open (avg 2.5 days to close); 684 negative-sentiment tickets.

## 3. What I'd do about it

1. **Fix the mix.** Pause or rework Organic Search and Email (near-total loss, lowest response); test more Direct Mail budget - it converts at 53% but only ran 149 times.
2. **Go after 'Pricing' losses.** It's the top loss reason, then Product Fit. I'd lift what Central does (69.9% win) into East (57.8%).
3. **Check on YieldMax, TrueNorth, LionGate, AlphaCore.** A lot of tickets on real revenue. UltraLink worries me most (140 tickets on $7,950 revenue).

## 4. Data quirks (I found these while building, all in the verification log)

- **Duplicate keys:** 3 `opportunity_id` and 4 `ticket_id` dupes, so counts dedupe on read (496 unique opps, 2,996 unique tickets).
- **Nulls the dictionary doesn't mention**: `customer_sentiment` has 59 blanks.
- **Orphan accounts** ACCT-101-115 in marketing/support. Left joins keep the CRM rows; 150 marketing + 131 support rows sit on accounts with no deals.
- **Join warning:** the 63,420-row model multiplies rows (leads x tickets per account). Averages and rankings are fine on it; **sums run high**. That's why Sales and Marketing KPIs use the source datasets, and the Customer Health sheet says so in the sheet.

## 5. Q&A setup

The Q&A Topic **"WA - NovaTech Revenue Intelligence"** (Version 2 Active) sits on all four datasets with a short glossary (revenue = Won deal_value, ROI/response/at-risk meanings, data quirks). I asked the same 3 questions before and after (`screenshots/qc_before*` vs `qc_after*`) - after the Topic the answers picked the right dataset. I use Q to poke around and the dashboard when a number has to be right. Full log: `q_exploration_log.md`. The raw Q summary is in `exec_summary.md` with my notes on which counts not to quote.

## 6. Using the dashboard

- **Filters** are at the top of Customer Health (priority) and Sales Pipeline (deal_stage). Picking one refilters the sheet.
- Clicking the priority chart jumps to the Marketing Funnel sheet, so you can go from a risky account to spend in one click.
- Check any Q answer against the sheet before it goes in a deck (see the cross-check column in the Q log).
