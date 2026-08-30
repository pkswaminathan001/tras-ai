import argparse
import json
from pathlib import Path

from pipeline import ClaimRecord, extract_claim, validation_summary


DEMO_TEXT = """ACCIDENT REPORT\nVIN: 1HGCM82633A004352\nMake: Honda\nModel: Accord\nDrivable: No\nInsured Name: Arun Kumar\nTow Location: Chennai Central Yard\nImpact Point: Front-left\n"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the insurance claims AI demo")
    parser.add_argument("--llm", action="store_true", help="Reserved for optional LLM adapter")
    parser.add_argument("--input", type=Path, help="Text report to process")
    args = parser.parse_args()

    if args.llm:
        raise SystemExit("LLM adapter is intentionally not enabled in the deterministic MVP. Add a provider adapter behind the extraction interface.")

    text = args.input.read_text(encoding="utf-8") if args.input else DEMO_TEXT
    extracted = extract_claim(text)

    # Simulates the record already present in the claims system.
    reference = ClaimRecord(**extracted.to_dict())
    result = validation_summary(extracted, reference)

    print(json.dumps({"extracted": extracted.to_dict(), "validation": result}, indent=2))


if __name__ == "__main__":
    main()
