# NorthStar-Comms Roadmap

## Current baseline

| Item | Status |
|---|---|
| Development version | `v2.0.0-dev` |
| Repository state | Test-ready development baseline |
| Canonical source | `data/master_channels.csv` |
| Production exports | Disabled |
| Next external gate | Physical CPS and radio validation |

## Milestone 0 — Project foundation

**Status: Complete**

- Repository, license and project governance
- Stable `NSC-###` identifier convention
- Architecture and data-dictionary foundation
- Historical `v0.1.0` and Version 1 checkpoint retained

## Milestone 1 — Canonical data foundation

**Status: Baseline complete; population continues**

- [x] Canonical 128-position allocation
- [x] Safe blank reserved positions
- [x] Standard GMRS, NOAA and MURS records
- [x] Initial amateur, marine and railroad records
- [x] Radio profiles separated by actual model
- [ ] Verify and populate GMRS repeaters within 75 miles of Eden Prairie
- [ ] Verify and populate local amateur repeaters
- [ ] Add remaining marine and railroad monitoring records from authoritative sources
- [ ] Generate the Excel review workbook from canonical repository data

## Milestone 2 — Radio export validation

**Status: Test-ready; hardware validation pending**

- [x] GM25 direct CHIRP schema retained
- [x] Receive-only and unsupported-service TX inhibition
- [x] Unverified exporter blocking
- [x] Automated Linux validation and tests
- [ ] GM25 CHIRP import and radio programming test
- [ ] GM25 receive-only/PTT inhibition test
- [ ] Direct UV-5R stock-software CSV export
- [ ] UV-5R import, programming and receive-only test
- [ ] Direct DM-32UV CPS export
- [ ] DM-32UV analog and DMR schema mapping
- [ ] DM-32UV import, programming and receive-only test
- [ ] Enable production output only after recorded evidence passes

## Milestone 3 — Regional frequency data

**Status: Planned**

- Sourced repeater records and provenance
- Owner/access requirements
- GPS locations and operational status
- Minnesota and Wisconsin travel coverage
- Field observations and last-confirmed dates

## Milestone 4 — Operational documentation

**Status: In progress**

- Hardware validation procedures
- Quick-reference cards
- Programming guides
- Family and convoy communications plans
- ICS-205 and check-in procedures

## Milestone 5 — Portable and fixed systems

**Status: Concept decisions documented**

- EK01 compact emergency receive/RF-awareness kit
- GK01 grab communications kit
- FB01 field base
- Icom mobile and future fixed-base ecosystem
- Equipment, battery and maintenance tracking

## Milestone 6 — Networking and situational awareness

**Status: Deferred architecture**

- ATAK-CIV and WinTAK
- Offline maps and shared mission data
- Optional TAK Server
- APRS, DMR GPS and sensor gateways only after interface validation
- Mesh, Winlink and satellite paths

TAK/CoT remains separate from radio-native APRS and DMR GPS until a tested gateway proves the data mapping and failure behavior.

## Milestone 7 — Mapping, automation and mission packages

**Status: Future**

- Repeater and coverage maps
- Route-specific packages
- ICS documentation generation
- Reference-card generation
- Release packaging
- Field-test visualization

## Release gate

A stable release requires:

1. Canonical validation passes.
2. Generated artifacts reproduce without a Git diff.
3. The target profile has direct CPS schema evidence.
4. CPS import succeeds.
5. The physical radio programs successfully.
6. Receive-only channels reject PTT.
7. Authorized TX channels use the expected frequency, offset, tone, bandwidth and power.
8. Test evidence is recorded in the repository.
