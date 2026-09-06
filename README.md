# NovaTech Revenue Intelligence - Amazon QuickSight BI Build

A complete business-intelligence project in Amazon QuickSight (Amazon Quick Suite): from raw starter CSVs to a governed, three-sheet executive dashboard with Q&A - where **every number in the dashboard was independently recomputed from the raw files before publication**.

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

The central design problem here is **grain**: account-level left joins fan out rows, so the model stores them for Q&A breadth while every dashboard KPI binds to its source dataset - a lesson learned the hard way when Quick Chat averaged correctly but summed inflated (Q log #2).

## Start here

1. [`deliverables/report_sarah_chen.md`](deliverables/report_sarah_chen.md) - the stakeholder report the project was actually for
2. [`deliverables/verification_log.md`](deliverables/verification_log.md) - how every figure was proven (data dictionary ↔ Quick Chat ↔ pandas/dashboard)
3. [`deliverables/exec_summary.md`](deliverables/exec_summary.md) - the dashboard's generative executive summary
4. [`pdf/dashboard_export.pdf`](deliverables/pdf/dashboard_export.pdf) - all three sheets exported
5. [`docs/`](docs) - methodology, screenshot evidence guide, first-person retrospective
6. [`WALKTHROUGH.md`](WALKTHROUGH.md) - step-by-step reproduction: every input and its provenance, build order, failure log

## What was built

- **Datasets (SPICE, `WA -` prefixed)** - CRM (499), marketing (2,240), support (3,000) + **unified account-level model** (left joins CRM ⟕ Marketing ⟕ Support on `account_id`) with calculated fields `days_to_close`, `campaign_roi_pct`, `resolution_days`, `at_risk_flag`
- **One published dashboard - `WA - NovaTech Revenue Intelligence Dashboard`** (`53e87aec-721e-491e-8436-e1b3d6eaba55`)
  - *Sales Pipeline* - KPI $707,201, revenue by region/loss reason/tier, `deal_stage` filter control, quantified annotation
  - *Marketing Funnel* - spend-vs-revenue per campaign, responses by channel, funnel stages, `campaign_channel` control
  - *Customer Health* - resolution time by priority, sentiment donut, volume by company, priority control, grain disclosure
  - Cross-sheet navigation, 3 quantified annotations, generative executive summary, Q&A enabled
- **Governed Q&A topic** - `WA - NovaTech Revenue Intelligence` (V2 Active) over all four datasets with business glossary; before/after evidence and five-question exploration in [`deliverables/q_exploration_log.md`](deliverables/q_exploration_log.md)
- **Ground-truth toolkit** - [`deliverables/ground_truth/profile_data.py`](deliverables/ground_truth/profile_data.py) reproduces every headline number from the raw CSVs

## Evidence trail

288 dated screenshots in [`deliverables/screenshots/`](deliverables/screenshots) record the build in order: baseline verification (`00–54`) → upload & type fixes (`55–99`) → unified model & fan-out proof (`100–199`) → dashboard sheets & filters (`200–449`) → Q&A topic & chat (`qc_*`, `490`) → cleanup & final state (`5xx`). [`docs/evidence_guide.md`](docs/evidence_guide.md) walks the important frames; the rest is kept for auditability.

## Repo map

```
deliverables/
  report_sarah_chen.md      stakeholder report        verification_log.md   three-way verification
  q_exploration_log.md      Q&A testing evidence      exec_summary.md       generated dashboard summary
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

Single-quarter data (no trend lines possible); the unified model is deliberately denormalized for Q&A breadth at the cost of storage; `Other` category hygiene (e.g., company-tier labels) was surfaced to stakeholders rather than silently corrected. See [`docs/retrospective.md`](docs/retrospective.md).

## Contributing & license

Found an error in a number or a claim? Open an issue - see [`CONTRIBUTING.md`](CONTRIBUTING.md) for how to reproduce the checks. Content licensed CC BY-NC-ND 4.0 ([`LICENSE`](LICENSE)).
