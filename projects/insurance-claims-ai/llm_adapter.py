from __future__ import annotations

import json
import os

from pipeline import ClaimRecord

SCHEMA = {
    "type": "object",
    "properties": {
        "vin": {"type": ["string", "null"]},
        "make": {"type": ["string", "null"]},
        "model": {"type": ["string", "null"]},
        "drivable": {"type": ["boolean", "null"]},
        "insured_name": {"type": ["string", "null"]},
        "tow_location": {"type": ["string", "null"]},
        "impact_point": {"type": ["string", "null"]},
    },
    "required": ["vin", "make", "model", "drivable", "insured_name", "tow_location", "impact_point"],
    "additionalProperties": False,
}

SYSTEM_PROMPT = """Extract insurance accident-report fields into the supplied JSON schema. Never invent a value. Use null when the report does not contain enough evidence. This is extraction only, not a claims decision."""


def extract_with_openai(text: str, model: str | None = None) -> ClaimRecord:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install the optional dependency first: pip install openai") from exc

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required for --llm mode")

    client = OpenAI()
    response = client.responses.create(
        model=model or os.getenv("OPENAI_MODEL", "gpt-5.6-luna"),
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": "claim_record",
                "schema": SCHEMA,
                "strict": True,
            }
        },
    )
    data = json.loads(response.output_text)
    return ClaimRecord(**data)
