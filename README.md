# Resource Health Tool

A Python-powered auditing tool for a community resource database in Contentful. It scores every listing's health — freshness, link validity, completeness — via a configurable, weighted rule engine, and exports the results to CSV for review and tracking.

This project doubles as a learning project: it's my first Python codebase, built incrementally while learning the language, `asyncio`, regex, and general software architecture patterns.

> **A note on data:** this repo's code is public, but the real content it operates on (organization names, phone numbers, URLs) belongs to a private community database and is never committed here. `data/sample_export.json` is fake, illustrative data with the same shape as a real export, so the tool can be run end-to-end without any real data.

## What it does

1. **Ingests** structured content from Contentful (currently via CLI export; Content Delivery API planned) and resolves linked entries (websites, phone numbers, categories) into a clean internal data model.
2. **Checks link health** — asynchronously validates every website URL associated with every resource, with concurrency capped to avoid overwhelming target servers, and caches results so link checks don't need to run on every scoring pass.
3. **Scores each entry** against a set of independent, pluggable rules — e.g., "hasn't been updated in over a year," "has broken links," "description is too short to be useful," "phone number missing a description." Each rule contributes a proportional share of a 0–100 health score, based on its configured weight relative to every other active rule.
4. **Reports results** as a sorted CSV, worst-scoring entries first, with the specific reasons behind each entry's deductions.

## Architecture

```
src/health_checker/
├── client.py          # Contentful ingestion — raw JSON → Entry objects
├── models.py           # Entry, Resource, Website, PhoneNumber, Category dataclasses
├── create_broken_link_batch_list.py     # Async, concurrency-limited link validation
├── scoring.py           # Aggregates rule results into a final weighted score
├── reporting.py         # CSV/JSON report generation
└── rules/
    ├── base.py          # Rule interface (abstract base class) and RuleResult
    ├── freshness.py
    ├── are_links_broken.py
    ├── phone_number_exists.py
    └── ...               # one file per independent scoring rule

scripts/
├── run_check.py                 # Score entries and generate a report
├── build_broken_link_lookup.py  # Refresh the cached link-health lookup
└── refresh_all.py                # Full pipeline: export → link check → score → report

tests/
└── ...                # pytest suite, one test file per rule
```

**Design principles this project leans on:**
- **Separation of concerns** — Contentful-specific parsing (`client.py`) never leaks into scoring logic (`rules/`), and rules never know where their input data came from.
- **A uniform `Rule` interface** — every rule implements the same `evaluate(entry) -> RuleResult` contract (enforced via an abstract base class), so new rules can be added without touching the scoring or reporting layers.
- **Weighted, proportional scoring** — each rule reports a 0.0–1.0 *severity* for a given entry; the scoring layer converts that into an actual point deduction based on the rule's `weight` relative to the total weight of all active rules. This means adding or removing a rule automatically rebalances every other rule's share of the 100-point scale, with no manual recalculation required.
- **Cached, decoupled link checking** — link validation is slow and network-dependent, so it runs as its own scheduled step, independent of scoring, with results cached to a local lookup file.

## Running it

```bash
# set up a virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# copy the sample data to try it out without real credentials
cp data/sample_export.json data/export.json

# score entries and generate a report
python3 scripts/run_check.py --limit 10

# or run the full pipeline (requires Contentful credentials — see below)
python3 scripts/refresh_all.py --exclude-status "Permanently Closed"
```

### Configuration

Real runs against a live Contentful space require a `.env` file (see `.env.example`) with:

```
CONTENTFUL_SPACE_ID=
CONTENTFUL_MANAGEMENT_TOKEN=
```

## Roadmap

- [ ] Migrate from Contentful CLI export to the Content Delivery API
- [ ] Scheduled refresh via GitHub Actions (private data, public code)
- [ ] JSON and HTML report formats alongside CSV
- [ ] Warehouse-backed historical tracking of scores over time (Snowflake + dbt)