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
    args = parser.parse_args()
    text = args.input.read_text(encoding="utf-8") if args.input else DEMO_TEXT
    reference = None
    if args.mismatch:
        reference = ClaimRecord("1HGCM82633A004352", "Honda", "Civic", False, "Arun Kumar", "Chennai Central Yard", "Front-left")
    print(json_result(run_pipeline(text, reference)))

if __name__ == "__main__":
    main()
