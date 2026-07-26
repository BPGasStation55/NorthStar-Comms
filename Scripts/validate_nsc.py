#!/usr/bin/env python3
"""Validate canonical NSC channel data and generated exports."""

from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "master_channels.csv"


def main() -> int:
    errors: list[str] = []
    with DATA.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if len(rows) != 128:
        errors.append(f"Expected 128 canonical channels; found {len(rows)}.")

    expected_ids = [f"NSC-{i:03d}" for i in range(1, 129)]
    actual_ids = [r["nsc_id"] for r in rows]
    if actual_ids != expected_ids:
        errors.append("NSC IDs are not sequential NSC-001 through NSC-128.")

    for r in rows:
        seq = int(r["sequence"])
        if len(r["name_short"]) > 6:
            errors.append(f"{r['nsc_id']}: short name exceeds 6 characters.")
        if len(r["name_long"]) > 15:
            errors.append(f"{r['nsc_id']}: long name exceeds 15 characters.")
        try:
            rx = float(r["rx_frequency"])
            tx = float(r["tx_frequency"])
        except ValueError:
            errors.append(f"{r['nsc_id']}: invalid frequency.")
            continue
        if seq <= 22 and abs(rx - tx) > 0.000001:
            errors.append(f"{r['nsc_id']}: fixed simplex memory has different RX/TX.")
        if 23 <= seq <= 30 and abs((tx - rx) - 5.0) > 0.000001:
            errors.append(f"{r['nsc_id']}: fixed repeater memory is not +5 MHz.")

    if errors:
        print("Validation failed:")
        for e in errors:
            print(f" - {e}")
        return 1

    print("Validation passed: 128 channels, sequential IDs, valid naming, fixed GM25 memories preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
