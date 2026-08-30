from __future__ import annotations

from dataclasses import dataclass, asdict
import re
from typing import Any


@dataclass
class ClaimRecord:
    vin: str | None = None
    make: str | None = None
    model: str | None = None
    drivable: bool | None = None
    insured_name: str | None = None
    tow_location: str | None = None
    impact_point: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class Mismatch:
    field: str
    extracted: Any
    reference: Any
    reason: str


def normalize_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = re.sub(r"\s+", " ", value).strip()
    return cleaned or None


def normalize_vin(value: str | None) -> str | None:
    value = normalize_text(value)
    return value.upper() if value else None


def extract_claim(text: str) -> ClaimRecord:
    """Deterministic baseline extractor used by the public demo.

    In production this interface can be backed by an LLM/OCR adapter. Keeping
    extraction separate from validation makes the workflow testable.
    """
    def grab(pattern: str) -> str | None:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        return normalize_text(match.group(1)) if match else None

    vin = grab(r"\bVIN\s*[:#-]?\s*([A-HJ-NPR-Z0-9]{17})\b")
    make = grab(r"\bMake\s*[:#-]?\s*([^\n,]+)")
    model = grab(r"\bModel\s*[:#-]?\s*([^\n,]+)")
    insured = grab(r"\b(?:Insured|Owner)\s*(?:Name)?\s*[:#-]?\s*([^\n]+)")
    tow = grab(r"\bTow(?:ing)?\s*Location\s*[:#-]?\s*([^\n]+)")
    impact = grab(r"\bImpact\s*Point\s*[:#-]?\s*([^\n]+)")
    drivable_raw = grab(r"\bDrivable\s*[:#-]?\s*(Yes|No)")

    return ClaimRecord(
        vin=normalize_vin(vin),
        make=make,
        model=model,
        drivable=None if drivable_raw is None else drivable_raw.lower() == "yes",
        insured_name=insured,
        tow_location=tow,
        impact_point=impact,
    )


def compare_records(extracted: ClaimRecord, reference: ClaimRecord) -> list[Mismatch]:
    mismatches: list[Mismatch] = []
    for field in asdict(extracted):
        actual = getattr(extracted, field)
        expected = getattr(reference, field)
        if actual is not None and expected is not None and actual != expected:
            mismatches.append(
                Mismatch(
                    field=field,
                    extracted=actual,
                    reference=expected,
                    reason="Extracted value differs from reference claim record",
                )
            )
    return mismatches


def validation_summary(record: ClaimRecord, reference: ClaimRecord) -> dict[str, Any]:
    mismatches = compare_records(record, reference)
    checked = sum(
        getattr(record, field) is not None and getattr(reference, field) is not None
        for field in asdict(record)
    )
    return {
        "status": "REVIEW" if mismatches else "PASS",
        "fields_checked": checked,
        "mismatch_count": len(mismatches),
        "mismatches": [asdict(item) for item in mismatches],
    }
