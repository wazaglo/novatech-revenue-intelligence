# Contributing

Thanks for looking. This is a **course capstone portfolio repo**, so it's a bit different from normal open-source.

## What this repo is (and isn't)

- **Is:** a record of how I designed, built, and verified a QuickSight/Quick Suite solution against a fixed brief (NovaTech's requirements doc / the Udacity rubric).
- **Isn't:** a running product or a library. The dashboards, topics, and agents live in a Vocareum lab account that is torn down after the course, so the repo + screenshots are the deliverable.

## Ways to contribute

| Kind of feedback | How |
|---|---|
| Errors in analysis, numbers, or claims | Open an issue - the fastest way to make this better. Point at the file/section; I re-verify and credit reporters in the doc |
| Better grain/join or verification approaches | Issue or PR against `docs/methodology.md` - design critiques especially welcome |
| Reproduction problems | Issue with your OS/Python version; the ground-truth script needs `pandas` and a local copy of the 3 starter CSVs (course materials, not redistributed) |

Please **don't** open PRs that restate what's already in `docs/` - I'm keeping one voice in there on purpose.

## Reproducing the checks

```bash
# Recompute the headline numbers from the raw CSVs
# (starter CSVs are course materials - supply your own copy)
NOVA_DATA_DIR=/path/to/Structured\ Data python deliverables/ground_truth/profile_data.py
```

## Style notes

- Every quantitative claim must cite its source: raw dataset, QuickSight screenshot, or Quick Research report.
- Screenshots are append-only evidence; don't edit or relabel history.
- Docs are written in first person on purpose - they're my learning record.

## License

By opening an issue or PR you agree your contributions are offered under the same CC BY-NC-ND 4.0 terms that cover this repository (see `LICENSE`).
