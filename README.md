# Field Visit Planner

A persuasive itinerary is still unusable if the return trip misses the workday.

This independent portfolio experiment by Vedant Thaker runs locally on Python 3.11. All inputs are original fictional or synthetic fixtures. It requires no cloud account, paid API, credentials, external weights or employer data.

## The decision

I turned customer-visit planning into a bounded exact problem: select appointments across two days under travel, meeting windows, daily costs and return-to-depot constraints. A highest-value-first itinerary is the baseline. My solver uses subset dynamic programming for each day, then a second dynamic program to avoid visiting a customer twice. Independent replay recomputes every arrival, finish and cost.

## Reproduce and inspect

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python run.py --output runs/ci
```

The default `python run.py` refreshes committed `results/`; `--output` writes a fresh run to an ignored directory. The seeded generator in `generate.py` writes the original input fixtures to `data/`. [Measured results](results/report.md), [raw metrics](results/metrics.json), and [source/data/result digests](results/manifest.json) make the experiment inspectable. Tests verify known answers and failure boundaries, not just successful execution.

## Measured comparison and next decision

Across **30 two-day scenarios**, exact planning selects **152 visits worth 1200 fictional priority points**, compared with **119 visits worth 983** for highest-priority-first greedy. Exact planning has strictly greater utility in **26 scenarios**. Independent replay validates every returned itinerary. These points express the chosen fixture objective, not revenue.

The next decision is to introduce uncertain travel-time ranges and customer cancellations, then compare worst-case feasibility with the static optimum. The exact bounded result alone does not justify scheduling a real calendar.

## What the result can support

Travel matrices, customer windows, costs and utility are fictional. The solver supports at most 10 sites and 3 days and optimizes this static objective exactly; it does not call calendar/travel services, send invitations or establish customer delivery impact. The baseline and optimizer receive the same cases and objective.

The next decision follows from the recorded comparison, including weak or negative outcomes. No synthetic result is presented as an employer deployment or a real-world business improvement.

See [data card](docs/data-card.md) and [reference credits](docs/provenance.md). Original code and fixtures are MIT licensed.
