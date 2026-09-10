# What I learned building this

My own notes on the build - what worked, what bit me, what I'd do differently.
I'm keeping this blunt. If I can't defend a number line by line, it's not done.

## What actually worked
- **I checked first, built second.** I read the three Quick Chat knowledge bases and the data
  dictionary before I touched anything, so I knew to expect about 499 deals / 2,240
  campaigns / 3,000 tickets. The real CSVs came back a row or two off, so I didn't
  trust either source - I wrote a pandas ground-truth file and made every later
  check use rates and unique counts instead of hardcoded totals. That one habit
  made the verification log easy.
- **I checked everything three ways.** Every KPI had to match in (a) the dictionary / pandas,
  (b) Quick Chat / the Q&A Topic, and (c) the dataset or dashboard card. When they
  didn't line up (average deal size by company), that mismatch was the whole lesson.
  See the join note below.
- **Annotations carry a decision.** Each sheet has one annotation with a number *and*
  what I'd do about it ("Won revenue is $707,201 from 315 won deals (63.1% win
  rate) - prioritize Enterprise and Large pipeline coverage"). If a chart can't
  support a line like that, I left it off.

## What bit me
- **Join blow-up.** The joined model is per account, so leads x tickets multiply.
  Averages live through that; SUMs don't. Q gave me an inflated average deal size
  once because it answered off the joined table. My fix: **KPIs pull from the
  source datasets**, and the Customer Health sheet states its grain in plain text.
  Next time I'd put that warning in the Topic glossary on day one.
- **Empty visuals break PDF export.** One empty AutoGraph visual gave me an unusable
  PDF page. I deleted it and re-exported. Now I export the PDF as a check, not
  just at the end.
- **I left duplicates lying around.** Re-running the build left a duplicate dataset
  and old dashboards. I deleted them at the end (screenshots `492`, `520`, `527`)
  so what's published matches the zip.
- **KPI cards can't start navigation.** "On select" needs something clickable and a
  KPI has nothing to click. I moved the action to the priority bar chart so it
  actually runs.

## What I'd do differently
- Put the two filter controls in on day one instead of finding the 2-sheet
  requirement late.
- Publish *one* multi-sheet dashboard from the start. My first instinct was three
  separate ones, which isn't what the rubric wants.
- I checked the 63,420 grain by hand each time. I'd keep a two-line script that
  asserts deals x leads x tickets per account after every refresh.

## The number I'd defend anywhere
**$707,201** from **315 of 499** deals (**63.1%**). I can redo it from the
raw CSV in one pandas line, see it on the dashboard KPI, and get the same answer
from the Q&A Topic. That match is the real deliverable - the dashboard is just
how someone else gets to it.
