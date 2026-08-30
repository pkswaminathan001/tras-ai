import argparse
from pathlib import Path

from pipeline import ClaimRecord, json_result, run_pipeline

DEMO_TEXT = """ACCIDENT REPORT
VIN: 1HGCM82633A004352
Make: Honda
Model: Accord
Drivable: No
Insured Name: Arun Kumar
Tow Location: Chennai Central Yard
Impact Point: Front-left
"""

def main() -> None:
    parser = argparse.ArgumentParser(description="Run insurance claims automation demo")
    parser.add_argument("--input", type=Path, help="Text report to process")
    parser.add_argument("--mismatch", action="store_true", help="Introduce a reference mismatch")
    parser.add_argument("--llm", action="store_true", help="Use optional OpenAI structured extraction")
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8") if args.input else DEMO_TEXT

    if args.llm:
        from llm_adapter import extract_with_openai
        extracted = extract_with_openai(text)
        reference = None
        if args.mismatch:
            reference = ClaimRecord("1HGCM82633A004352", "Honda", "Civic", False, "Arun Kumar", "Chennai Central Yard", "Front-left")
        # Reuse the same deterministic validation layer for model output.
        from pipeline import validation_summary, confidence_score, PipelineResult
        reference = reference or ClaimRecord(**extracted.to_dict())
        validation = validation_summary(extracted, reference)
        result = PipelineResult(extracted, validation, confidence_score(validation), validation["status"] == "REVIEW" or confidence_score(validation) < 0.85)
    else:
        reference = None
        if args.mismatch:
            reference = ClaimRecord("1HGCM82633A004352", "Honda", "Civic", False, "Arun Kumar", "Chennai Central Yard", "Front-left")
        result = run_pipeline(text, reference)
    print(json_result(result))

if __name__ == "__main__":
    main()
