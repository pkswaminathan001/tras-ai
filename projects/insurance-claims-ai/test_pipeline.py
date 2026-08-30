from pipeline import ClaimRecord, extract_claim, run_pipeline

REPORT = """VIN: 1HGCM82633A004352
Make: Honda
Model: Accord
Drivable: No
Insured Name: Arun Kumar
Tow Location: Chennai Central Yard
Impact Point: Front-left
"""

def test_extract_all_fields():
    r = extract_claim(REPORT)
    assert r.vin == "1HGCM82633A004352"
    assert r.make == "Honda"
    assert r.model == "Accord"
    assert r.drivable is False
    assert r.insured_name == "Arun Kumar"
    assert r.tow_location == "Chennai Central Yard"
    assert r.impact_point == "Front-left"

def test_match_passes():
    ref = ClaimRecord("1HGCM82633A004352", "Honda", "Accord", False, "Arun Kumar", "Chennai Central Yard", "Front-left")
    result = run_pipeline(REPORT, ref)
    assert result.validation["status"] == "PASS"
    assert not result.review_required
    assert result.confidence >= 0.85

def test_mismatch_routes_review():
    ref = ClaimRecord("1HGCM82633A004352", "Honda", "Civic", False, "Arun Kumar", "Chennai Central Yard", "Front-left")
    result = run_pipeline(REPORT, ref)
    assert result.validation["status"] == "REVIEW"
    assert any(m["field"] == "model" for m in result.validation["mismatches"])
    assert result.review_required

def test_missing_field_routes_review():
    report = REPORT.replace("Impact Point: Front-left\n", "")
    ref = ClaimRecord("1HGCM82633A004352", "Honda", "Accord", False, "Arun Kumar", "Chennai Central Yard", "Front-left")
    result = run_pipeline(report, ref)
    assert "impact_point" in result.validation["missing_fields"]
    assert result.review_required
