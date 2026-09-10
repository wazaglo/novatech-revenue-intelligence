# NovaTech Revenue Intelligence - Amazon QuickSight BI Build

I built this in Amazon QuickSight (Quick Suite) for my Udacity capstone: raw starter
CSVs to a three-sheet dashboard with Q&A. I recomputed every dashboard number
from the raw files in pandas before I published anything.

*Udacity nd2726 capstone · Vocareum lab, us-west-2 · September 2026 · Wisdom Azaglo*

## Results at a glance

| Metric | Value | Verified against |
|---|---|---|
| Won revenue | **$707,201** (315/499 deals, 63.1% win) | pandas on raw CSV = Quick Chat = dashboard KPI |
| Funnel | 609 / 2,240 responses (**27.2%**) | same three-way check |
| Campaign ROI | **−83.7% … −97.7%** (all six negative) | recomputed per campaign |
| Model grain | **63,420 rows = predicted fan-out Σ(deals×leads×tickets)/account** | pandas prediction, exact match |
| Data-quality findings | dup keys, 59 null sentiment rows, 15 orphan accounts | documented, not silently fixed |
| Churn-risk signal | ACCT-041: 334 tickets / $40,722 income | flagged for CS team |

The hard part was **grain**. Account-level left joins blow up row counts, so I kept
the joined model for Q&A but pointed every dashboard KPI at its source dataset.
I learned that the hard way when Quick Chat got the average right and the sum
wrong (Q log #2).

## Start here

1. [`deliverables/report_sarah_chen.md`](deliverables/report_sarah_chen.md) - the stakeholder report this was actually for
2. [`deliverables/verification_log.md`](deliverables/verification_log.md) - how I checked every figure (data dictionary vs Quick Chat vs pandas/dashboard)
3. [`deliverables/exec_summary.md`](deliverables/exec_summary.md) - raw Q summary plus my notes on what not to quote from it
4. [`deliverables/pdf/dashboard_export.pdf`](deliverables/pdf/dashboard_export.pdf) - all three sheets exported
5. [`docs/`](docs) - methodology, screenshot evidence guide, first-person retrospective
6. [`WALKTHROUGH.md`](WALKTHROUGH.md) - step-by-step reproduction: every input and its provenance, build order, failure log

## What was built

- **Datasets (SPICE, `WA -` prefixed)** - CRM (499), marketing (2,240), support (3,000) + **unified account-level model** (left joins CRM to Marketing to Support on `account_id`) with `days_to_close`, `campaign_roi_pct`, `resolution_days`, `at_risk_flag`
- **One published dashboard - `WA - NovaTech Revenue Intelligence Dashboard`** (`53e87aec-721e-491e-8436-e1b3d6eaba55`)
  - *Sales Pipeline* - $707,201 KPI, revenue by region/loss reason/tier, `deal_stage` filter, one written annotation
  - *Marketing Funnel* - spend vs revenue per campaign, responses by channel, funnel stages, `campaign_channel` filter
  - *Customer Health* - resolution time by priority, sentiment donut, volume by company, priority filter, grain note in the sheet
  - Cross-sheet navigation, 3 written annotations, Q summary, Q&A on
- **Q&A topic** - `WA - NovaTech Revenue Intelligence` (V2 Active) over all four datasets with a short glossary; before/after shots and five test questions in [`deliverables/q_exploration_log.md`](deliverables/q_exploration_log.md)
- **Ground-truth script** - [`deliverables/ground_truth/profile_data.py`](deliverables/ground_truth/profile_data.py) redoes every headline number from the raw CSVs

## Evidence trail

288 screenshots in [`deliverables/screenshots/`](deliverables/screenshots) in build order: baseline checks (00-54), upload and type fixes (55-99), joined model and fan-out proof (100-199), sheets and filters (200-449), Q&A topic and chat (qc_*, 490), cleanup and final state (5xx). [`docs/evidence_guide.md`](docs/evidence_guide.md) points at the ones that matter; the rest is there so I can prove what I did.

## Repo map

```
deliverables/
  report_sarah_chen.md      stakeholder report        verification_log.md   three-way verification
  q_exploration_log.md      Q&A testing notes         exec_summary.md       Q summary + my notes
  pdf/                      merged 3-sheet export     ground_truth/         pandas replication kit
  screenshots/              288 evidence frames       README.md             rubric ↔ artifact map
docs/
  methodology.md            grain/fan-out design reasoning
  evidence_guide.md         screenshot tour
  retrospective.md          decisions, mistakes, lessons
WALKTHROUGH.md              full reproduction guide (inputs, provenance, order, failures)
```

The submission zip delivered to Udacity is byte-equivalent to `deliverables/` (kept out of git to hold repo size down).

## Honest limitations

One quarter of data so no trends. The joined model is intentionally wide - it costs
storage and it inflates sums, which is why Sales/Marketing KPIs don't use it.
I left messy `Other` tier labels alone and flagged them instead of quietly fixing
them. More in [`docs/retrospective.md`](docs/retrospective.md).

## Contributing & license

Found an error in a number or a claim? Open an issue - see [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to reproduce the checks. Content licensed CC BY-NC-ND 4.0 ([`LICENSE`](LICENSE)).
