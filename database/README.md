# Database Reference

`Master/Master_Radio_Database.xlsx` is preserved as a legacy schema, validation-list and provenance prototype.

It currently contains no canonical channel rows and is not the active source used by the export engine. See `docs/architecture/CANONICAL_SOURCE_POLICY.md`.

Do not populate the workbook manually while `data/master_channels.csv` is authoritative. A later milestone may generate a review workbook from repository-native canonical tables.
