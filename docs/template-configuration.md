# Template Configuration

Template profiles describe where semantic fields live in a workbook. They must not contain production addresses, client names, or project-specific private details in a public repository.

Example:

```yaml
template:
  worksheet: Topographie
  unit_table:
    first_data_row: 6
    last_data_row: 62
    unit_column: D
  fields:
    wohnnutzflaeche:
      column: R
    balkon:
      column: U
    loggia:
      column: S
    kellerabteil:
      column: X
  total_row: 63
```

The Vorlage remains the formatting authority. The writer copies the workbook and only updates cells specified by the profile.
