# ANSWERS.md — Design Decisions

## Why a web dashboard?

When you're on-call and something breaks at 2am, you need to see patterns instantly.
A terminal report forces you to scroll and squint. A browser dashboard lets you:

- Spot the spike on a timeline chart in one glance
- See which endpoints are slow vs which are error-prone in parallel panels
- Share a URL with a teammate rather than copy-pasting terminal output

So the dashboard is the right call for operational use.

---

## What does the dashboard show and why?

| Panel | Why it's useful |
|---|---|
| **Summary cards** | First thing you see: total requests, error rate, avg/P99 response time, skipped lines |
| **Timeline (requests/hour)** | Instantly reveals traffic spikes, drops, or anomalies correlated with incidents |
| **Status code pie** | Shows the health of the system — is it mostly 2xx or drowning in 5xx? |
| **HTTP methods bar** | Sanity check: if DELETE is suddenly 40% of traffic, that's an alert |
| **Response time percentiles** | P99 is more useful than average — one slow endpoint hides in averages |
| **10 slowest endpoints** | Tells you exactly where to start optimizing |
| **10 most requested** | Shows what your users actually use |
| **Error-prone endpoints** | Which paths keep returning 4xx/5xx — authentication issues, broken routes |
| **Top IPs** | Spot abusive clients or bots hammering a single endpoint |
| **Malformed lines** | Transparency: shows exactly what was skipped and why |

---

## How malformed lines are handled

The tool **never crashes** on bad input. For every line it reads:

1. Try to parse as JSON (handles the "someone changed the logging config" case)
2. Try to parse as standard format with a flexible regex
3. If neither works → add to the skipped list, continue to the next line

The dashboard shows:
- Total number of skipped lines (so you know data is missing)
- Up to 10 examples of skipped lines (so you can debug the format)

This is better than silently dropping them or crashing.

---

## How different timestamp formats are handled

The parser tries 5 different `strptime` formats in order, then falls back to Unix epoch.
If nothing works, the timestamp is recorded as `null` — the entry is still counted in
all statistics that don't need a timestamp (status codes, response times, etc.).

---

## How different response time units are handled

The parser normalizes everything to **milliseconds**:
- `142ms`   → 142.0
- `0.142s`  → 142.0
- `142`     → 142.0 (bare number assumed to be ms)

All percentile and average calculations work on the normalized values.

---

## Tech stack choice

| Layer | Choice | Reason |
|---|---|---|
| Language | Python | Best regex + datetime libraries; readable for ops teams |
| Web server | FastAPI | Minimal boilerplate; serves HTML + JSON API in one file |
| Charts | Chart.js (CDN) | No build step; beautiful defaults; zero npm required |
| Styling | Pure CSS | No framework dependency; loads instantly |

The whole tool is **zero npm, zero webpack, zero Docker** — just `pip install` and run.