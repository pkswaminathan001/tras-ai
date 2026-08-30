import json
from pathlib import Path
from pipeline import ClaimRecord, run_pipeline

DATA = Path(__file__).parent / "data" / "benchmark.json"

def main() -> None:
    cases = json.loads(DATA.read_text(encoding="utf-8"))
    passed = 0
    reviews = 0
    for case in cases:
        result = run_pipeline(case["report"], ClaimRecord(**case["reference"]))
        ok = result.validation["status"] == case["expected_status"]
        passed += ok
        reviews += result.review_required
        print(f"{case['id']}: {result.validation['status']} | confidence={result.confidence:.3f} | {'PASS' if ok else 'FAIL'}")
    print(f"\nExpected workflow outcomes: {passed}/{len(cases)} ({passed/len(cases):.1%})")
    print(f"Review routing: {reviews}/{len(cases)} ({reviews/len(cases):.1%})")

if __name__ == "__main__":
    main()
