from __future__ import annotations

from typing import Any

from .models import MappedRecord, RoomRecord


def map_records(records: list[RoomRecord], config: dict[str, Any]) -> tuple[list[MappedRecord], list[RoomRecord]]:
    semantic_map = {
        alias.casefold(): field
        for field, aliases in config.get("room_type_mappings", {}).items()
        for alias in aliases
    }
    mapped: list[MappedRecord] = []
    unmapped: list[RoomRecord] = []

    for record in records:
        field = semantic_map.get(record.room_type.casefold())
        if field is None:
            unmapped.append(record)
            continue
        mapped.append(MappedRecord(unit=record.unit, field=field, area=record.area, source=record))

    return mapped, unmapped
