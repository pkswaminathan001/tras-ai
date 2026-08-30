# Insurance Claims AI Automation Pipeline

A production-inspired, offline-first AI operations prototype that converts unstructured accident reports into structured claim data, validates the result, scores confidence, and routes exceptions to human review.

## Why I built it

Insurance operations teams can spend significant time reading reports, locating vehicle and accident facts, entering structured values, and cross-checking them against existing claim records. The design goal is to automate repetitive work without turning AI output into an unchecked source of truth.

## Architecture

```text
Accident / Police Report
          |
          v
 Text / PDF ingestion boundary
          |
          v
Extraction + normalization
          |
          v
 Structured ClaimRecord
          |
          v
Validation + mismatch detection
          |
          v
   Confidence scoring
       /       \
     PASS     REVIEW
                  |
             Human analyst
```

The public MVP keeps extraction deterministic so the repository runs without an API key. The extraction boundary is intentionally isolated, making a future LLM adapter replaceable without changing validation and review logic.

## Extracted fields

VIN, make, model, drivable status, insured/owner name, tow location, and impact point.

## Run it

```bash
cd projects/insurance-claims-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python demo.py
python demo.py --mismatch
pytest -q
python benchmark.py
```

## Web demo

```bash
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`. Paste a report, run analysis, and inspect the structured output, confidence, and review decision.

## Benchmark

The included benchmark contains synthetic cases covering exact matches, field mismatches, and missing fields. It is a regression test for workflow behavior, **not** a claim of production model accuracy.

Current local benchmark: **4/4 expected workflow outcomes (100%)** across the four included synthetic cases.

## Engineering decisions

- **Offline-first:** reviewers can run the demo without a model API key.
- **Validation-first:** AI/extracted data is treated as a proposal and compared against reference data.
- **Human-in-the-loop:** mismatches and incomplete records are routed to review.
- **Synthetic public data:** no confidential employer or customer documents are included.
- **Provider boundary:** model-specific logic can be added without coupling it to business validation.

## Impact evidence

My professional insurance-operations work motivated this design. I have reported approximately **40% processing-time reduction** and **25% reduction in rework/errors** for an AI-assisted workflow. Those are experience-based figures and are not represented as benchmark measurements from this repository.

## Next production-oriented increments

PDF ingestion, OCR adapter, optional LLM structured extraction, field-level provenance, persistent review queue, batch API, and a richer operations dashboard.

## Important scope note

This is a portfolio engineering demonstration. It is not a production claims decision engine, underwriting system, Guidewire integration, or automated approval system.

Author: **PR Swaminathan**
