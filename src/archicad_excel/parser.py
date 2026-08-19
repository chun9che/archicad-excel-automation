from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .models import RoomRecord
from .normalize import normalize_room_identifier, normalize_unit, unit_from_identifier


def _parse_area(value: str, decimal_separator: str = ",") -> float:
    text = (value or "").strip()
    if decimal_separator == ",":
        text = text.replace(".", "").replace(",", ".")
    return float(text)


def parse_archicad_txt(path: str | Path, config: dict[str, Any]) -> list[RoomRecord]:
    """Parse a delimited Archicad room export into normalized records.

    The parser only produces normalized room facts. It does not know anything
    about Excel sheets or target columns.
    """

    parser_cfg = config.get("parser", {})
    delimiter = parser_cfg.get("delimiter", "\t")
    encoding = parser_cfg.get("encoding", "utf-8-sig")
    decimal_separator = parser_cfg.get("decimal_separator", ",")
    columns = parser_cfg.get(
        "columns",
        {"floor": "Geschoß", "unit": "Top", "room_type": "Raumname", "area": "Fläche"},
    )
    prefixes = config.get("normalization", {}).get("strip_prefixes", [])
    special = config.get("special_mappings", {})

    records: list[RoomRecord] = []
    with Path(path).open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        for source_row, row in enumerate(reader, start=2):
            if not row or not any((value or "").strip() for value in row.values()):
                continue
            source_unit = (row.get(columns["unit"]) or "").strip()
            room_type = (row.get(columns["room_type"]) or "").strip()
            if not source_unit or not room_type:
                continue

            source_unit_id = normalize_room_identifier(source_unit, prefixes)
            room_name_id = normalize_room_identifier(room_type, prefixes)
            room_id = room_name_id or source_unit_id
            unit = normalize_unit(source_unit, prefixes)
            normalized_room_type = room_type

            for rule in special.values():
                source_room = rule.get("source_room_type")
                identifier_prefix = (rule.get("identifier_pattern") or "").split("{", 1)[0]
                source_room_matches = source_room and source_room.casefold() == room_type.casefold()
                identifier_matches = bool(
                    room_id and identifier_prefix and room_id.upper().startswith(identifier_prefix.upper())
                )
                if room_id and (source_room_matches or identifier_matches):
                    unit = unit_from_identifier(room_id, rule.get("target_unit_pattern", "TOP {number:02d}"))
                    normalized_room_type = rule.get("target_room_type") or source_room or room_type

            records.append(
                RoomRecord(
                    unit=unit,
                    room_id=room_id,
                    room_type=normalized_room_type,
                    floor=(row.get(columns["floor"]) or "").strip(),
                    area=_parse_area(row.get(columns["area"]) or "0", decimal_separator),
                    source_unit=source_unit,
                    source_room_type=room_type,
                    source_row=source_row,
                )
            )
    return records
