# What I learned building this (first-person retrospective)

This is my own account of the build - what worked, what bit me, and what I'd do
differently. Kept deliberately honest; a BI project you can't defend line-by-line isn't
finished.

## What actually worked
- **Baseline before building.** Reading the three Quick Chat knowledge bases and the data
  dictionary *first* meant I already knew the numbers should be ~499 deals / ~2,240
  campaigns / ~3,000 tickets. When the real CSVs came back slightly different, I didn't
  trust either source blindly - I wrote a pandas ground-truth file and made every later
  check agnostic to the exact row count. That single habit made the verification log write
  itself.
- **Three-way cross-check.** Every KPI was confirmed by (a) the data dictionary / pandas,
  (b) Quick Chat / the Q&A Topic, and (c) the dataset or dashboard card. When the three
  disagreed (average deal size by company), the disagreement *was* the lesson: see the
  fan-out note below.
- **Annotations as decisions, not decoration.** Each sheet has exactly one annotation that
  names a number *and* an action ("Won revenue is $707,201 from 315 won deals (63.1% win
  rate) - prioritize Enterprise and Large pipeline coverage"). If a chart can't carry a number like that, it shouldn't be on the
  sheet.

## What bit me
- **Fan-out.** The unified model is an account-level join, so leads × tickets multiply per
  account. Averages survive that; SUMs don't. Q once reported an inflated average deal size
  because it answered off the joined table. My fix was structural: **KPI cards bind to the
  source datasets**, and the Customer Health sheet says its grain out loud. I'd put that
  warning in the Topic glossary from day one.
- **Placeholder / empty visuals break PDF export.** An empty AutoGraph visual silently made
  an exported PDF page unusable; I had to delete it and re-export. Lesson: export your PDFs
  *as a verification step*, not just as a deliverable.
- **Stale/duplicate lab resources.** Re-running the build left a duplicate dataset and
  superseded dashboards. I deleted them at the end (screenshots `492`, `520`, `527`) so the
  published environment matches the submitted package one-to-one.
- **KPI cards can't be click-navigation sources.** Navigation "on select" needs a
  selectable data point; a KPI has none. I re-attached the cross-sheet action to the
  priority bar chart so it actually fires.

## What I'd do differently
- Scope filter controls to the two sheets that need them on day one rather than discovering
  the ≥2-sheets requirement late.
- Publish *one* multi-sheet dashboard from the start; my first instinct was three
  single-purpose dashboards, which the rubric explicitly does not want.
- Keep a tiny scratch script to assert the model grain (63,420 = Σ deals×leads×tickets per
  account) after every dataset refresh - I did it by hand and would automate it.

## The number I'd defend anywhere
**$707,201** won revenue from **315 of 499** deals (**63.1%**). I can reproduce it from the
raw CSV in one pandas line, see it on the dashboard KPI, and get the same answer from the
governed Q&A Topic. That end-to-end agreement is the actual deliverable - the dashboard is
just how other people get to it.
