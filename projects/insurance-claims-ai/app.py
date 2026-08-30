from html import escape
from pathlib import Path

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from pipeline import run_pipeline

app = FastAPI(title="Insurance Claims AI Pipeline", version="1.0.0")
DEMO = Path(__file__).parent / "data" / "demo_report.txt"

PAGE = """<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Insurance Claims AI</title><style>body{font-family:system-ui;max-width:1100px;margin:30px auto;padding:0 18px;background:#f5f7fa;color:#172033}textarea{width:100%;min-height:320px;padding:12px;border:1px solid #ccd2da;border-radius:10px;font:14px ui-monospace,monospace;box-sizing:border-box}button{padding:10px 16px;border:0;border-radius:8px;background:#172033;color:white}.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:white;padding:20px;border-radius:14px;box-shadow:0 2px 12px rgba(0,0,0,.06)}pre{white-space:pre-wrap;overflow:auto}.pass{border-left:6px solid #238636}.review{border-left:6px solid #d73a49}.muted{color:#667085}@media(max-width:800px){.grid{grid-template-columns:1fr}}</style></head><body><h1>Insurance Claims AI Pipeline</h1><p class='muted'>Extract → validate → score → route for human review.</p>{body}</body></html>"""

def page(form_report: str = "", result_html: str = "") -> str:
    report = form_report or DEMO.read_text(encoding="utf-8")
    body = f"<div class='grid'><div class='card'><h2>Report</h2><form method='post' action='/analyze'><textarea name='report'>{escape(report)}</textarea><p><button type='submit'>Analyze report</button></p></form></div><div class='card'><h2>Workflow</h2><p>1. Parse fields<br>2. Normalize values<br>3. Compare with reference data<br>4. Calculate confidence<br>5. Send incomplete/mismatched cases to review</p></div></div>{result_html}"
    return PAGE.format(body=body)

def render_result(report: str) -> str:
    result = run_pipeline(report)
    cls = "review" if result.review_required else "pass"
    title = "REVIEW REQUIRED" if result.review_required else "PASS"
    return f"<div class='card {cls}'><h2>{title}</h2><p>Confidence: <strong>{result.confidence:.0%}</strong></p><pre>{escape(str(result.to_dict()))}</pre></div>"

@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return page()

@app.post("/analyze", response_class=HTMLResponse)
def analyze(report: str = Form(...)) -> str:
    return page(report, render_result(report))

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
