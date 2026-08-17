from __future__ import annotations

import argparse
import json
from pathlib import Path

from .mapping import map_records
from .parser import parse_archicad_txt
from .qc import human_report, run_qc
from .template import inspect_template, load_yaml
from .writer import write_workbook


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="archicad-excel")
    sub = parser.add_subparsers(dest="command", required=True)

    inspect_cmd = sub.add_parser("inspect-template")
    inspect_cmd.add_argument("template")
    inspect_cmd.add_argument("--json", action="store_true")

    run_cmd = sub.add_parser("run")
    run_cmd.add_argument("--input", required=True)
    run_cmd.add_argument("--template", required=True)
    run_cmd.add_argument("--project-config", required=True)
    run_cmd.add_argument("--template-config", required=True)
    run_cmd.add_argument("--output", required=True)
    run_cmd.add_argument("--qc-json")

    args = parser.parse_args(argv)
    if args.command == "inspect-template":
        result = inspect_template(args.template)
        print(json.dumps(result, indent=2, ensure_ascii=False) if args.json else _format_inspection(result))
        return 0

    project_config = load_yaml(args.project_config)
    template_config = load_yaml(args.template_config)
    records = parse_archicad_txt(args.input, project_config)
    mapped, unmapped = map_records(records, project_config)
    write_result = write_workbook(args.template, args.output, mapped, template_config)
    qc = run_qc(records, mapped, unmapped)
    qc["writer"] = write_result
    if args.qc_json:
        Path(args.qc_json).write_text(json.dumps(qc, indent=2, ensure_ascii=False), encoding="utf-8")
    print(human_report(qc))
    return 0 if qc["status"] == "PASS" and not write_result["missing_targets"] else 2


def _format_inspection(result: dict) -> str:
    lines = []
    for sheet in result["worksheets"]:
        lines.append(f"Worksheet: {sheet['name']}")
        lines.append(f"  Used range: {sheet['used_range']}")
        lines.append(f"  Merged cells: {len(sheet['merged_cells'])}")
        lines.append(f"  Rotated headers: {len(sheet['rotated_headers'])}")
        lines.append(f"  Candidate header rows: {[item['row'] for item in sheet['candidate_headers']]}")
        lines.append(f"  Candidate total rows: {[item['row'] for item in sheet['candidate_total_rows']]}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
