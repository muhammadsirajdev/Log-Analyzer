# Log Analyzer

A web dashboard that reads any server log file and shows useful metrics —
error rates, slow endpoints, traffic timelines, and more.

---

## Quick Start

### 1. Install dependencies

```bash
pip install fastapi uvicorn
```

### 2. Generate a sample log file (for testing)

```bash
python scripts/generate_logs.py 2000 logs/sample.log
```

This creates `logs/sample.log` with 2000 lines, including intentional
messy lines (bad timestamps, JSON format, malformed entries, etc.).

### 3. Run the analyzer

```bash
python main.py logs/sample.log
```

### 4. Open the dashboard

Visit **http://localhost:8000** in your browser.

---

## Using your own log file

```bash
python main.py /path/to/your/server.log
```

The tool accepts any path — filename doesn't matter.

---

## Project Structure

```
log-analyzer/
├── analyzer/
│   ├── __init__.py      # Python package marker
│   ├── parser.py        # Parses log lines (all formats)
│   └── stats.py         # Computes metrics from parsed entries
├── scripts/
│   └── generate_logs.py # Test log generator
├── static/
│   └── dashboard.html   # Web dashboard (HTML + Chart.js)
├── logs/                # Generated log files go here
├── main.py              # FastAPI server + entry point
├── ANSWERS.md           # Design decisions explained
└── README.md
```

---

## Log formats supported

| Format | Example |
|---|---|
| Standard ISO timestamp | `2024-03-15T14:23:01Z 192.168.1.42 GET /api/users 200 142ms` |
| Slash timestamp | `2024/03/15 14:23:01 ...` |
| Human date | `15-Mar-2024 14:23:01 ...` |
| Unix epoch | `1710512581 ...` |
| Response time in ms | `142ms` |
| Response time in s | `0.142s` |
| Bare response time | `142` |
| JSON lines | `{"timestamp": "...", "ip": "...", ...}` |
| Missing status code | `... - 142ms` |
| Extra fields | `... 200 142ms "Mozilla/5.0..."` |

Malformed/unparseable lines are counted and shown in the dashboard — nothing is silently dropped.

---

## Generator options

```bash
python scripts/generate_logs.py                    # 1000 lines → logs/sample.log
python scripts/generate_logs.py 5000               # 5000 lines → logs/sample.log
python scripts/generate_logs.py 5000 out/test.log  # 5000 lines → out/test.log
```