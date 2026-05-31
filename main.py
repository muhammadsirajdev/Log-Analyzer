import sys
import os
import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from analyzer.parser import parse_log_file
from analyzer.stats import compute_stats


app = FastAPI(title="Log Analyzer")

app.mount("/static", StaticFiles(directory="static"), name="static")


analysis_result = {}


@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    dashboard_path = os.path.join("static", "dashboard.html")
    with open(dashboard_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/results")
def get_results():
    if not analysis_result:
        raise HTTPException(status_code=404, detail="No analysis loaded yet.")
    return JSONResponse(content=analysis_result)


def analyze_file(filepath: str):
    global analysis_result

    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    print(f"📂 Parsing log file: {filepath}")
    entries, skipped = parse_log_file(filepath)

    print(f"✅ Parsed {len(entries)} entries")
    print(f"⚠️  Skipped {len(skipped)} malformed lines")

    stats = compute_stats(entries)

    stats["skipped_count"] = len(skipped)
    stats["skipped_examples"] = [
        {"line_num": ln, "content": content[:120]}
        for ln, content in skipped[:10]
    ]
    stats["log_file"] = os.path.basename(filepath)

    analysis_result = stats
    print(f"📊 Stats computed. Opening dashboard at http://localhost:8000")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path-to-log-file>")
        sys.exit(1)

    log_path = sys.argv[1]
    analyze_file(log_path)

    uvicorn.run(app, host="0.0.0.0", port=8000)
