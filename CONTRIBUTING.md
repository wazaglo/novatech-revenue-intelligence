# Contributing

Thanks for your interest! This is a **course capstone portfolio repo**, so the ground rules are a bit different from a typical open-source project.

## What this repo is (and isn't)

- **Is:** a record of how I designed, built, and verified a QuickSight/Quick Suite solution against a fixed brief (NovaTech's requirements doc / the Udacity rubric).
- **Isn't:** a running product or a library. The dashboards, topics, and agents live in a Vocareum lab account that is torn down after the course, so the repo + screenshots are the deliverable.

## Ways to contribute

| Kind of feedback | How |
|---|---|
| Errors in analysis, numbers, or claims | Open an issue - the fastest way to make this better. Point at the file/section; I re-verify and credit reporters in the doc |
| Better grain/join or verification approaches | Issue or PR against `docs/methodology.md` - design critiques especially welcome |
| Reproduction problems | Issue with your OS/Python version; the ground-truth script needs `pandas` and a local copy of the 3 starter CSVs (course materials, not redistributed) |

Please **don't** open PRs that restate conclusions already in `docs/` - this repo intentionally keeps one authored voice.

## Reproducing the checks

```bash
# NovaTech: recompute the headline ground-truth numbers from the raw CSVs
# (starter CSVs are course materials - supply your own copy)
NOVA_DATA_DIR=/path/to/Structured\ Data python deliverables/ground_truth/profile_data.py

# Market Intelligence: recompute the publisher ranking from the Kaggle CSV
python -c "import csv;from collections import defaultdict;rows=list(csv.DictReader(open('data/vgsales.csv')));pub=defaultdict(float);[pub.__setitem__(r['Publisher'],pub[r['Publisher']]+float(r['Global_Sales'])) for r in rows];print(sorted(pub.items(),key=lambda x:-x[1])[:3])"
```

## Style notes

- Every quantitative claim must cite its source: raw dataset, QuickSight screenshot, or Quick Research report.
- Screenshots are append-only evidence; don't edit or relabel history.
- Docs are written in first person on purpose - they're my learning record.

## License

By opening an issue or PR you agree your contributions are offered under the same CC BY-NC-ND 4.0 terms that cover this repository (see `LICENSE`).
