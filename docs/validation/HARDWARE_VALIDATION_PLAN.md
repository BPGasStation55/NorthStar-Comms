# Hardware Validation Plan

No profile may enable production release until its evidence is committed and all applicable checks pass.

## Required evidence

- Radio make, exact model and hardware revision
- Firmware version
- Programming-software name and version
- Direct unmodified export from that software
- Cable and driver information
- Generated test artifact commit SHA
- Import result
- Programming result
- Functional test result

## Phase 1 — Schema capture

1. Read the radio with its intended programming software.
2. Save the native image or codeplug.
3. Export a CSV without manually changing headers or values.
4. Commit the sample under `reference/` with sensitive identifiers removed.
5. Document which fields disable TX.

## Phase 2 — Import test

1. Start from a fresh read of the radio.
2. Import the generated test artifact.
3. Confirm row count, names, frequencies, tones, power, bandwidth and scan state.
4. Do not write the radio if unexpected TX values appear.

## Phase 3 — Bench programming

1. Save a recovery image before writing.
2. Program the radio.
3. Power-cycle it.
4. Read it back into the software.
5. Compare the readback against the expected artifact.

## Phase 4 — Receive-only safety

For every receive-only category:

1. Select a representative channel.
2. Attempt PTT without connecting an external power amplifier.
3. Confirm the radio refuses transmission.
4. Record the displayed behavior and any error tone/message.

Required categories include NOAA, MURS monitoring, marine, railroad, templates and any unsupported service.

## Phase 5 — Authorized transmit checks

Use only frequencies, equipment and test methods for which the operator is authorized.

Verify:

- Transmit frequency
- Offset
- Tone
- Bandwidth
- Power level
- Busy-channel lockout
- Scan behavior

## Completion

Copy `docs/validation/RESULT_TEMPLATE.md` for each radio/profile test. Attach or reference the direct CPS evidence and readback results. Update `hardware_validation_status` only through a reviewed pull request.
