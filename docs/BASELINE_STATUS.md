# Test-Ready Baseline Status

**Development version:** `v2.0.0-dev`
**Baseline status:** Test-ready
**Production status:** Blocked pending hardware validation

## Completed

- Repository paths normalized for case-sensitive systems.
- `data/master_channels.csv` established as the sole editable channel source.
- Stable `NSC-001` through `NSC-128` allocation implemented.
- Unverified slots use blank frequencies rather than transmit-capable placeholders.
- Receive-only records have blank canonical TX frequencies.
- GM25 test exports force TX off for receive-only, template and unsupported-service records.
- UV-5R and DM-32UV generation is blocked until direct software evidence exists.
- UV-32 and DM-32UV are represented as separate radio models.
- Standard-library validation and regression tests pass on Linux.
- Production release output is disabled.

## Canonical data summary

| Measure | Count |
|---|---:|
| Canonical positions | 128 |
| Populated positions | 53 |
| Safely reserved positions | 75 |
| Selected records | 39 |
| Template records | 14 |
| Active production profiles | 0 |

## External validation still required

1. Import and program the GM25 test artifact.
2. Confirm every `Duplex=off` channel rejects PTT.
3. Provide a direct UV-5R stock-software CSV export.
4. Provide a direct DM-32UV CPS export with analog and DMR structures.
5. Record physical test results using the validation template.
6. Update the relevant profile only after evidence passes.

## Deliberately deferred

- Regional repeater population and permission verification
- Additional marine and railroad monitoring frequencies
- Production codeplugs
- DMR contacts, zones, scan lists and talkgroups
- TAK/CoT gateways
- Mission packages and printable reference cards
