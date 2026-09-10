# Evidence trail - how to read `deliverables/screenshots/`

I screenshotted as I went. You don't need all 288; these are the ones I'd actually
open.

| #s | Phase | What to look at |
|---|---|---|
| `00`, `03` | Lab access | Vocareum → AWS access portal → QuickSight (`UdacityQuicksightLab`) |
| `12-13` | Baseline | Quick Chat answer vs data dictionary **before** any changes |
| `14-23` | Upload | CSV upload dialogs, dataset edit settings |
| `24-48` | Types & calcs | text→decimal corrections on `deal_value`, `annual_income`; calc editor with `IFELSE` ROI formula |
| `55-99` | Unified model | join diagram & full config (`79`, `84`, `88-89`), calc fields (`90-93`), type fixes (`98-99`) |
| `105-121` | Fan-out proof | dedupe steps + SPICE refresh showing **63,420** rows = predicted Σ |
| `135-171` | Customer Health sheet | KPI, sentiment donut, tickets by company, priority chart; filter panel → control at top of sheet |
| `172-215` | Sales Pipeline sheet | KPI $707,201, stage/region/segment charts, `deal_stage` control, Actions → Navigation config |
| `217-226` | Annotations + publish | written annotation text; publish dialog |
| `227-230` | PDF export | export menu, generated PDF |
| `231-240` | Marketing Funnel sheet | spend-vs-revenue, channel, funnel, control, annotation |
| `241-251` | Sheet hygiene | removing placeholder sheets/visuals, final 3-sheet order |
| `252-275` | Q&A Topic | topic wizard, dataset scoping, glossary, publish |
| `qc_before*` / `qc_after*` | Before/after | same 3 questions, before vs after the Topic |
| `qc_qlog1..5_*` | Test questions | 5 questions across 3 areas with dashboard checks |
| `332`, `341`, `345`, `354-355` | Naming | resources renamed with initials (`WA - …`), Topic V2 Active |
| `364-399` | Single-dashboard merge | hub analysis: 3 sheets, unified-dataset visuals on Customer Health, controls, KPI re-verified at $707,201 |
| `406-415` | Annotations + nav action | text boxes on all sheets; Navigation action → Marketing Funnel |
| `434-478` | Publish + interactivity | published dashboard, controls working, filter menu (`454-455`), action on selectable visual |
| `480-481` | Navigation proof | before-click vs after-click: Customer Health → Marketing Funnel sheet jump |
| `485-488` | PDF hygiene | removing empty visuals that broke PDF rendering |
| `490` | Q summary | Amazon Q summary of the published dashboard (kept raw in `exec_summary.md` with my notes) |
| `492`, `520`, `527`, `529` | Cleanup + final | duplicate datasets deleted, superseded dashboards deleted, final published 3-sheet dashboard |

## Where the "how do I know it's right" lives

1. `deliverables/verification_log.md` - 7 checks in the course template. I kept every
   check row-count agnostic so it still holds if the CSVs shift by a row or two.
2. `deliverables/ground_truth/` - the pandas script that redoes it all from the raw
   CSVs, no QuickSight involved.
3. `deliverables/q_exploration_log.md` - every Q answer checked against a dashboard
   sheet, including one where Q got it wrong (join duplication) and how I caught it.
