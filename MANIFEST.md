# NSC Version 2 Migration Kit

## Replace or add

| Kit path | Repository action |
|---|---|
| `data/master_channels.csv` | Add as the Version 2 canonical source |
| `profiles/*.json` | Add or merge into the existing profiles folder |
| `scripts/build_exports.py` | Add; replace an older exporter only after comparing |
| `scripts/validate_nsc.py` | Add |
| `tests/test_build.py` | Add or merge into existing tests |
| `exports/*/*.csv` | Generated test artifacts; replace older test exports |
| `docs/migrations/NSC_V2_MIGRATION.md` | Add |
| `snippets/README_V2_SECTION.md` | Copy section into existing README; do not replace README |
| `snippets/CHANGELOG_V2_ENTRY.md` | Copy entry into existing CHANGELOG; do not replace CHANGELOG |
| `snippets/GITIGNORE_ADDITIONS.txt` | Append relevant lines to existing `.gitignore` |

## Reference files

The `reference/` directory preserves input formats used during migration analysis. These are not authoritative channel data.
