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
          +---- optional LLM extraction
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

The default path is deterministic, so reviewers can run it without an API key. `llm_adapter.py` adds an optional OpenAI Responses API extraction path using strict JSON schema output; the same validation and review layer is applied afterward.

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

### Optional LLM mode

```bash
export OPENAI_API_KEY="your-key"
python demo.py --llm
```

The model can be changed with `OPENAI_MODEL`; the default is `gpt-5.6-luna` for a cost-sensitive extraction workload.

## Web demo

```bash
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000`. Paste a report, run analysis, and inspect the structured output, confidence, and review decision.

## Benchmark

The included benchmark contains synthetic cases covering exact matches, field mismatches, and missing fields. It is a regression test for workflow behavior, **not** a claim of production model accuracy.

Current benchmark: **4/4 expected workflow outcomes (100%)** across four synthetic cases.

## Engineering decisions

- **Offline-first:** reviewers can run the core workflow without a model API key.
- **LLM as an adapter:** model-specific logic is isolated from business validation.
- **Validation-first:** extracted values are proposals that must pass checks.
- **Human-in-the-loop:** mismatches and incomplete records are routed for review.
- **Synthetic public data:** no confidential employer or customer documents are included.

## Impact evidence

My professional insurance-operations work motivated this design. I have reported approximately **40% processing-time reduction** and **25% reduction in rework/errors** for an AI-assisted workflow. Those are experience-based figures and are not represented as benchmark measurements from this repository.

## Production-oriented roadmap

PDF ingestion → OCR → LLM extraction → field-level provenance → persistent review queue → batch processing → richer operations dashboard → model evaluation and regression suite.

## Important scope note

This is a portfolio engineering demonstration. It is not a production claims decision engine, underwriting system, Guidewire integration, or automated approval system.

Author: **PR Swaminathan**
