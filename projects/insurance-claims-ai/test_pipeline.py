from pipeline import ClaimRecord, compare_records, extract_claim, validation_summary


def test_extracts_claim_fields():
    text = """VIN: 1HGCM82633A004352\nMake: Honda\nModel: Accord\nDrivable: No\nInsured Name: Arun Kumar\nTow Location: Chennai Central Yard\nImpact Point: Front-left"""
    record = extract_claim(text)
    assert record.vin == "1HGCM82633A004352"
    assert record.make == "Honda"
    assert record.model == "Accord"
    assert record.drivable is False
    assert record.insured_name == "Arun Kumar"


def test_detects_mismatch():
    actual = ClaimRecord(vin="1HGCM82633A004352", make="Honda")
    reference = ClaimRecord(vin="1HGCM82633A004352", make="Toyota")
    mismatches = compare_records(actual, reference)
    assert len(mismatches) == 1
    assert mismatches[0].field == "make"


def test_clean_record_passes():
    record = ClaimRecord(vin="1HGCM82633A004352", make="Honda")
    result = validation_summary(record, ClaimRecord(vin="1HGCM82633A004352", make="Honda"))
    assert result["status"] == "PASS"
    assert result["mismatch_count"] == 0
