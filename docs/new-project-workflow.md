# New Project Workflow

1. Export room data from Archicad as a delimited room schedule.
2. Receive and open the client's Excel Vorlage.
3. Run template inspection:

   ```bash
   python scripts/inspect_template.py "Vorlage.xlsx"
   ```

4. Identify the worksheet, unit rows, unit identifier column, target columns, and total row.
5. Create or update a template configuration YAML.
6. Create a project configuration YAML with parser settings, normalization rules, and room-name mappings.
7. Run the mapping engine.
8. Inspect the generated QC report.
9. Open the resulting Excel workbook manually for final visual QC.
10. Deliver according to the client's required Excel workflow.

## Adding A New Semantic Field

If a new room type `Abstellraum` should map to a semantic field named `abstellraum`, add configuration like:

```yaml
room_type_mappings:
  abstellraum:
    - Abstellraum
    - AR
```

Then add the target column to the template profile:

```yaml
template:
  fields:
    abstellraum:
      column: P
```

The Excel processing engine should not need code changes for this type of extension.
