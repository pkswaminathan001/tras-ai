from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
from typing import Any

FIELDS = ("vin", "make", "model", "drivable", "insured_name", "tow_location", "impact_point")

@dataclass
class ClaimRecord:
    vin: str | None = None
    make: str | None = None
    model: str | None = None
    drivable: bool | None = None
    insured_name: str | None = None
    tow_location: str | None = None
    impact_point: str | None = None
    def to_dict(self) -> dict[str, Any]: return asdict(self)

@dataclass
class Mismatch:
    field: str
    extracted: Any
    reference: Any
    reason: str

@dataclass
class PipelineResult:
    extracted: ClaimRecord
    validation: dict[str, Any]
    confidence: float
    review_required: bool
    def to_dict(self) -> dict[str, Any]:
        return {"extracted": self.extracted.to_dict(), "validation": self.validation, "confidence": self.confidence, "review_required": self.review_required}

def normalize_text(value: str | None) -> str | None:
    if value is None: return None
    cleaned = re.sub(r"\s+", " ", value).strip(" \t\r\n:,-")
    return cleaned or None

def normalize_vin(value: str | None) -> str | None:
    value = normalize_text(value)
    if not value: return None
    return re.sub(r"[^A-Za-z0-9]", "", value).upper()

def normalize_bool(value: str | bool | None) -> bool | None:
    if value is None: return None
    if isinstance(value, bool): return value
    value = value.strip().lower()
    if value in {"yes", "y", "true", "drivable", "driveable"}: return True
    if value in {"no", "n", "false", "not drivable", "undrivable"}: return False
    return None

def extract_claim(text: str) -> ClaimRecord:
    def grab(pattern: str) -> str | None:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        return normalize_text(match.group(1)) if match else None
    return ClaimRecord(
        vin=normalize_vin(grab(r"\bVIN\s*[:#-]?\s*([A-HJ-NPR-Z0-9]{17})\b")),
        make=grab(r"\bMake\s*[:#-]?\s*([^\n,]+)"),
        model=grab(r"\bModel\s*[:#-]?\s*([^\n,]+)"),
        drivable=normalize_bool(grab(r"\bDrivable\s*[:#-]?\s*([^\n]+)")),
        insured_name=grab(r"\b(?:Insured(?:\s+Name)?|Owner(?:\s+Name)?)\s*[:#-]?\s*([^\n]+)"),
        tow_location=grab(r"\bTow(?:ing)?\s+Location\s*[:#-]?\s*([^\n]+)"),
        impact_point=grab(r"\bImpact\s+Point\s*[:#-]?\s*([^\n]+)"),
    )

def compare_records(extracted: ClaimRecord, reference: ClaimRecord) -> list[Mismatch]:
    out: list[Mismatch] = []
    for field in FIELDS:
        actual, expected = getattr(extracted, field), getattr(reference, field)
        if actual is not None and expected is not None and actual != expected:
            out.append(Mismatch(field, actual, expected, "Extracted value differs from reference claim record"))
    return out

def validation_summary(record: ClaimRecord, reference: ClaimRecord) -> dict[str, Any]:
    mismatches = compare_records(record, reference)
    checked = sum(getattr(record, f) is not None and getattr(reference, f) is not None for f in FIELDS)
    missing = [f for f in FIELDS if getattr(record, f) is None]
    return {"status": "REVIEW" if mismatches or missing else "PASS", "fields_checked": checked, "fields_expected": len(FIELDS), "missing_fields": missing, "mismatch_count": len(mismatches), "mismatches": [asdict(x) for x in mismatches]}

def confidence_score(validation: dict[str, Any]) -> float:
    completeness = validation["fields_checked"] / validation["fields_expected"]
    mismatch_penalty = min(validation["mismatch_count"] / validation["fields_expected"], 1.0)
    missing_penalty = min(len(validation["missing_fields"]) / validation["fields_expected"], 1.0)
    score = 0.60 * completeness + 0.40 * (1 - mismatch_penalty) * (1 - missing_penalty)
    return round(max(0.0, min(score, 1.0)), 3)

def run_pipeline(text: str, reference: ClaimRecord | None = None) -> PipelineResult:
    extracted = extract_claim(text)
    reference = reference or ClaimRecord(**extracted.to_dict())
    validation = validation_summary(extracted, reference)
    confidence = confidence_score(validation)
    return PipelineResult(extracted, validation, confidence, validation["status"] == "REVIEW" or confidence < 0.85)

def json_result(result: PipelineResult) -> str:
    return json.dumps(result.to_dict(), indent=2, sort_keys=True)
