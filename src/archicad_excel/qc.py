from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict
from typing import Any

from .models import MappedRecord, RoomRecord


def run_qc(records: list[RoomRecord], mapped: list[MappedRecord], unmapped: list[RoomRecord]) -> dict[str, Any]:
    id_counts = Counter(record.room_id for record in records if record.room_id)
    duplicate_ids = sorted(identifier for identifier, count in id_counts.items() if count > 1)
    source_totals = defaultdict(float)
    mapped_totals = defaultdict(float)
    conflicts = []

    values_by_target = defaultdict(set)
    for record in records:
        source_totals[record.room_type] += record.area
    for record in mapped:
        mapped_totals[record.field] += record.area
        values_by_target[(record.unit, record.field)].add(round(record.area, 4))

    for (unit, field), values in values_by_target.items():
        if len(values) > 1:
            conflicts.append({"unit": unit, "field": field, "values": sorted(values)})

    result = {
        "source_record_count": len(records),
        "mapped_record_count": len(mapped),
        "unmapped_record_count": len(unmapped),
        "unmapped_records": [asdict(record) for record in unmapped],
        "duplicate_identifiers": duplicate_ids,
        "conflicting_values": conflicts,
        "source_totals": dict(source_totals),
        "mapped_totals": dict(mapped_totals),
        "status": "PASS" if not unmapped and not duplicate_ids and not conflicts else "FAIL",
    }
    return result


def human_report(qc: dict[str, Any]) -> str:
    lines = [
        f"QC status: {qc['status']}",
        f"Source records: {qc['source_record_count']}",
        f"Mapped records: {qc['mapped_record_count']}",
        f"Unmapped records: {qc['unmapped_record_count']}",
        f"Duplicate identifiers: {', '.join(qc['duplicate_identifiers']) or 'none'}",
        f"Conflicting values: {len(qc['conflicting_values'])}",
    ]
    return "\n".join(lines)
