# Test-Ready Baseline Manifest

## Authoritative inputs

| Path | Role |
|---|---|
| `data/master_channels.csv` | Canonical 128-position channel plan |
| `data/radio_models.csv` | Canonical radio-model registry |
| `profiles/gm25_chirp.json` | GM25 test-export policy |
| `profiles/uv5r_baofeng_stock.json` | Blocked UV-5R profile and evidence requirement |
| `profiles/dm32uv_cps.json` | Blocked DM-32UV profile and evidence requirement |
| `profiles/uv32_cps.json` | Separate analog UV-32 reference profile |

## Executable controls

| Path | Role |
|---|---|
| `scripts/validate_nsc.py` | Canonical, profile and generated-export safety checks |
| `scripts/build_exports.py` | Deterministic test-artifact builder |
| `tests/test_baseline.py` | Standard-library regression suite |
| `.github/workflows/ci.yml` | Linux continuous integration |
| `SHA256SUMS.txt` | Integrity checks for baseline source and generated artifacts |

## Generated artifacts

Only `exports/test/` contains current generated artifacts. Every artifact and manifest is explicitly marked test-only.

## Preserved references

- `database/master/Master_Radio_Database.xlsx` is a legacy schema prototype, not an active channel source.
- `reference/` contains source-format evidence.
- `archive/legacy-v2-exports/` preserves superseded exports that must not be imported.
