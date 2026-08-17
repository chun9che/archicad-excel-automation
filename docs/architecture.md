# Architecture

The engine is intentionally split into small concerns:

- `parser.py` reads Archicad exports and returns normalized room records.
- `normalize.py` normalizes unit and stable room identifiers such as `PROJECT_TOP 17` and `PROJECT_KA17`.
- `mapping.py` maps source room names to semantic target fields.
- `template.py` reads template profiles and inspects unknown Excel templates.
- `writer.py` copies the Vorlage and writes only configured target cells.
- `qc.py` produces machine-readable QC and a concise human summary.

The parser has no Excel knowledge. The writer has no Archicad-specific parsing logic. Project-specific behavior belongs in YAML configuration.

Private production workbooks can be used as implementation cases, but they are not the shape of the reusable core.
