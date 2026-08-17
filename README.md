# Archicad Excel Automation

Archicad Excel Automation is a reusable workflow for mapping Archicad room-area exports into client-provided Excel templates while preserving the original workbook formatting, formulas, and print layout.

It is intended for architecture and BIM workflows where a project-specific Archicad room schedule must populate an externally supplied Excel workbook. The engine separates parsing, normalization, semantic room mapping, template profiles, writing, and QC so new projects should normally require configuration rather than Python code changes.

## Workflow

```text
Archicad export
    -> parser
    -> normalized room records
    -> project mapping configuration
    -> template profile
    -> Excel writer
    -> QC
    -> delivery workbook
```

## Quick Start

Install in editable mode:

```bash
python -m pip install -e .
```

Inspect a new Excel template:

```bash
python scripts/inspect_template.py "Vorlage.xlsx"
```

Run a configured mapping:

```bash
python -m archicad_excel.cli run \
  --input "examples/sanitized/archicad_export.txt" \
  --template "Client Template.xlsx" \
  --project-config "configs/example_project.yaml" \
  --template-config "configs/example_template.yaml" \
  --output "mapped-output.xlsx"
```

The writer copies the source Vorlage first and only updates configured target cells. It does not recreate the workbook from scratch.

## Public Data Policy

This repository is public. It contains reusable code, docs, tests, and synthetic examples only. Do not commit production Excel workbooks, Archicad exports, client templates, project addresses, Google Drive IDs, credentials, tokens, or local paths.

## License

MIT.
