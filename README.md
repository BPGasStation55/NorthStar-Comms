# NorthStar-Comms

> **One Database. Every Radio. Every Mission.**

NorthStar-Comms is an offline-first communications planning and radio-configuration toolkit for GMRS, amateur radio, monitoring, travel and prepared field operations.

## Current status

This repository is a **test-ready development baseline** for `v2.0.0-dev`.

- Canonical channel data is maintained in `data/master_channels.csv`.
- The 128 canonical positions use stable `NSC-001` through `NSC-128` identifiers.
- All generated artifacts remain test-only until their exact CPS schema and physical radio behavior are validated.
- Production release generation is disabled.
- Legacy Version 2 exports are preserved in `archive/legacy-v2-exports/` and must not be imported.

## Safety boundary

Only the GM-15 Pro/GM25 CHIRP schema currently has enough source evidence to generate a test artifact. Its exporter forces CHIRP `Duplex=off` for receive-only channels, templates and services that the radio profile is not authorized to transmit on.

UV-5R and DM-32UV generation is blocked until direct exports from their actual programming software establish the exact schema and receive-only encoding. The separate UV-32 reference schema is not treated as DM-32UV evidence.

No generated file is production-ready until CPS import, radio programming, receive-only behavior and functional hardware tests are recorded.

## Canonical 128-position structure

| Positions | Purpose |
|---|---|
| 001–022 | Standard GMRS |
| 023–030 | Generic GMRS repeater templates |
| 031–050 | Verified local/travel GMRS repeater slots |
| 051–057 | NOAA receive-only |
| 058–062 | MURS receive-only in NSC profiles |
| 063–080 | Amateur simplex |
| 081–112 | Verified local amateur repeater slots |
| 113–120 | Marine receive-only |
| 121–128 | Railroad receive-only |

Unverified positions remain reserved with blank frequencies. Placeholder frequencies are not used.

## Build and validation

Python 3.11 or newer is sufficient; the baseline uses only the standard library.

```bash
python scripts/validate_nsc.py
python scripts/build_exports.py --radio all
python -m unittest discover -s tests -v
sha256sum -c SHA256SUMS.txt
```

Generated test artifacts are written under `exports/test/`. A profile that lacks sufficient evidence exits as blocked instead of creating a speculative file.

## Radio profile status

| Radio | Schema | Test export | Production |
|---|---|---:|---:|
| GM-15 Pro / GM25 CHIRP family | Direct CHIRP reference available | Enabled | Blocked pending hardware validation |
| UV-5R stock software | Direct CSV missing | Blocked | Blocked |
| DM-32UV CPS | Direct CPS export missing | Blocked | Blocked |
| UV-32 analog CPS | Reference only; separate model | Blocked | Not a DM-32UV target |

## Repository layout

```text
data/                  Canonical editable data
profiles/              Radio-specific capability and export gates
scripts/               Validation and deterministic builders
tests/                 Standard-library automated tests
exports/test/          Generated test-only artifacts
database/              Legacy workbook and database reference material
docs/                  Architecture, decisions, kits and validation plans
reference/             Source-format evidence
archive/               Superseded artifacts retained for traceability
```

The workbook at `database/master/Master_Radio_Database.xlsx` is retained as a legacy schema prototype. It is not an independently editable channel source and currently contains no canonical channel rows.

## Current operational direction

- Icom is the selected primary future radio ecosystem.
- The two existing DM-32UV radios remain the limited DMR allocation: one for the Grab Kit and one for a mobile/base role.
- EK01 is the compact rapid-deployment receive and RF-awareness kit.
- ATAK-CIV and WinTAK remain long-term integrations. TAK/CoT data remains separate from APRS and DMR GPS until a gateway is explicitly validated.

See `docs/BASELINE_STATUS.md` and `docs/validation/HARDWARE_VALIDATION_PLAN.md` for the current gate status and required physical validation.

## License and compliance

The project is provided under the MIT License. Users remain responsible for licensing, equipment authorization, repeater permission and lawful operation. A technically programmable frequency is not automatically authorized for transmission.
