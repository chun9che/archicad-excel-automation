from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoomRecord:
    unit: str
    room_id: str | None
    room_type: str
    floor: str
    area: float
    source_unit: str
    source_room_type: str
    source_row: int


@dataclass(frozen=True)
class MappedRecord:
    unit: str
    field: str
    area: float
    source: RoomRecord
