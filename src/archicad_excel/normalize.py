from __future__ import annotations

import re


def normalize_unit(value: str, prefixes: list[str] | None = None) -> str:
    text = (value or "").strip()
    for prefix in prefixes or []:
        text = re.sub(rf"^{re.escape(prefix)}[_\-\s]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^.*?_", "", text) if re.match(r"^[A-Za-z0-9]+_TOP", text, re.I) else text
    match = re.search(r"TOP\s*0*(\d+)", text, re.IGNORECASE)
    if match:
        return f"TOP {int(match.group(1)):02d}"
    return text.upper()


def normalize_room_identifier(value: str, prefixes: list[str] | None = None) -> str | None:
    text = (value or "").strip()
    for prefix in prefixes or []:
        text = re.sub(rf"^{re.escape(prefix)}[_\-\s]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"^.*?_", "", text) if re.match(r"^[A-Za-z0-9]+_KA", text, re.I) else text
    match = re.search(r"\bKA\s*0*(\d+)\b", text, re.IGNORECASE)
    if match:
        return f"KA{int(match.group(1))}"
    return None


def unit_from_identifier(identifier: str, pattern: str = "TOP {number:02d}") -> str:
    match = re.search(r"(\d+)", identifier or "")
    if not match:
        raise ValueError(f"Identifier has no numeric suffix: {identifier!r}")
    return pattern.format(number=int(match.group(1)))
