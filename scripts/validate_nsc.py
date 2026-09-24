#!/usr/bin/env python3
"""Validate the NorthStar Comms test-ready canonical baseline."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "master_channels.csv"
RADIO_MODELS = ROOT / "data" / "radio_models.csv"
PROFILES = ROOT / "profiles"
GM25_EXPORT = ROOT / "exports" / "test" / "gm25" / "NSC_GM25_CHIRP_TEST_ONLY.csv"

EXPECTED_RANGES = [
    (1, 22, "01 GMRS Standard"),
    (23, 30, "02 GMRS Repeater"),
    (31, 50, "03 GMRS Local"),
    (51, 57, "04 NOAA"),
    (58, 62, "05 MURS"),
    (63, 80, "06 Amateur Simplex"),
    (81, 112, "07 Amateur Local Repeater"),
    (113, 120, "08 Marine Monitor"),
    (121, 128, "09 Railroad Monitor"),
]
ALLOWED = {
    "service": {"GMRS", "NOAA", "MURS", "AMATEUR", "MARINE", "RAILROAD"},
    "bandwidth": {"FM", "NFM"},
    "power_policy": {"LOW", "HIGH"},
    "receive_only": {"YES", "NO"},
    "status": {"SELECTED", "TEMPLATE", "RESERVED"},
    "scan_policy": {"INCLUDE", "SKIP"},
}


def read_csv(path: Path, encoding: str = "utf-8") -> list[dict[str, str]]:
    with path.open(encoding=encoding, newline="") as handle:
        return list(csv.DictReader(handle))


def validate_channels(rows: list[dict[str, str]]) -> list[str]:
    errors: list[str] = []
    if len(rows) != 128:
        errors.append(f"Expected 128 canonical positions; found {len(rows)}")
        return errors

    for index, row in enumerate(rows, start=1):
        expected_id = f"NSC-{index:03d}"
        if row["nsc_id"] != expected_id:
            errors.append(f"Position {index}: expected {expected_id}; found {row['nsc_id']}")
        if row["sequence"] != str(index):
            errors.append(f"{expected_id}: sequence does not equal {index}")
        if len(row["name_short"]) > 6:
            errors.append(f"{expected_id}: short name exceeds 6 characters")
        if len(row["name_long"]) > 15:
            errors.append(f"{expected_id}: long name exceeds 15 characters")
        for field, values in ALLOWED.items():
            if row[field] not in values:
                errors.append(f"{expected_id}: invalid {field}={row[field]!r}")

        if row["status"] == "RESERVED" and (
            row["rx_frequency"] or row["tx_frequency"]
        ):
            errors.append(f"{expected_id}: reserved positions must not contain frequencies")
        if row["receive_only"] == "YES" and row["tx_frequency"]:
            errors.append(f"{expected_id}: receive-only record contains a TX frequency")
        if row["receive_only"] == "NO" and not row["tx_frequency"]:
            errors.append(f"{expected_id}: TX-capable record is missing TX frequency")
        if row["status"] == "SELECTED" and not row["rx_frequency"]:
            errors.append(f"{expected_id}: selected record is missing RX frequency")
        for field in ("rx_frequency", "tx_frequency"):
            if row[field]:
                try:
                    float(row[field])
                except ValueError:
                    errors.append(f"{expected_id}: invalid {field}")

    for start, end, bank in EXPECTED_RANGES:
        for row in rows[start - 1 : end]:
            if row["bank"] != bank:
                errors.append(
                    f"{row['nsc_id']}: expected bank {bank!r}; found {row['bank']!r}"
                )

    expected_gmrs = [
        462.5625, 462.5875, 462.6125, 462.6375, 462.6625, 462.6875,
        462.7125, 467.5625, 467.5875, 467.6125, 467.6375, 467.6625,
        467.6875, 467.7125, 462.55, 462.575, 462.6, 462.625, 462.65,
        462.675, 462.7, 462.725,
    ]
    for index, frequency in enumerate(expected_gmrs):
        row = rows[index]
        if abs(float(row["rx_frequency"]) - frequency) > 0.000001:
            errors.append(f"{row['nsc_id']}: incorrect standard GMRS frequency")
        expected_power = "LOW" if 8 <= index + 1 <= 14 else "HIGH"
        expected_bandwidth = "NFM" if 8 <= index + 1 <= 14 else "FM"
        if row["power_policy"] != expected_power:
            errors.append(f"{row['nsc_id']}: incorrect GMRS power policy")
        if row["bandwidth"] != expected_bandwidth:
            errors.append(f"{row['nsc_id']}: incorrect GMRS bandwidth")

    for row in rows[22:30]:
        if abs(float(row["tx_frequency"]) - float(row["rx_frequency"]) - 5.0) > 0.000001:
            errors.append(f"{row['nsc_id']}: generic GMRS repeater pair is not +5 MHz")
        if row["status"] != "TEMPLATE":
            errors.append(f"{row['nsc_id']}: generic repeater must remain TEMPLATE")

    active_short_names = [
        row["name_short"] for row in rows if row["status"] != "RESERVED"
    ]
    duplicates = [name for name, count in Counter(active_short_names).items() if count > 1]
    if duplicates:
        errors.append(f"Duplicate active short names: {', '.join(sorted(duplicates))}")
    return errors


def validate_profiles() -> list[str]:
    errors: list[str] = []
    models = {row["radio_model_id"]: row for row in read_csv(RADIO_MODELS)}
    if set(models) != {"RMD-001", "RMD-002", "RMD-003", "RMD-004"}:
        errors.append("Radio model registry must define RMD-001 through RMD-004")
    if models.get("RMD-003", {}).get("model") != "DM-32UV":
        errors.append("RMD-003 must identify the DM-32UV")
    if models.get("RMD-004", {}).get("model") != "UV-32":
        errors.append("RMD-004 must identify the separate UV-32")
    profiles = {}
    for path in sorted(PROFILES.glob("*.json")):
        profile = json.loads(path.read_text(encoding="utf-8"))
        profile_id = profile["profile_id"]
        if profile_id in profiles:
            errors.append(f"Duplicate profile_id {profile_id}")
        profiles[profile_id] = profile
        if profile["radio_model_id"] not in models:
            errors.append(f"{profile_id}: unknown radio_model_id")
        if profile.get("production_release_enabled") is not False:
            errors.append(f"{profile_id}: production release must remain disabled")

    dm32 = profiles.get("dm32uv_cps")
    uv32 = profiles.get("uv32_cps_reference")
    if not dm32 or not uv32:
        errors.append("Separate DM-32UV and UV-32 profiles are required")
    elif dm32["radio_model_id"] == uv32["radio_model_id"]:
        errors.append("DM-32UV and UV-32 must use separate model IDs")
    if dm32 and dm32.get("export_enabled"):
        errors.append("DM-32UV export must remain blocked pending direct CPS evidence")
    if uv32 and uv32.get("export_enabled"):
        errors.append("UV-32 reference profile must not be an active exporter")
    return errors


def validate_gm25_export(channels: list[dict[str, str]]) -> list[str]:
    if not GM25_EXPORT.exists():
        return []
    errors: list[str] = []
    canonical = {row["nsc_id"]: row for row in channels}
    rows = read_csv(GM25_EXPORT, encoding="utf-8-sig")
    for row in rows:
        parts = row["Comment"].split()
        if not parts:
            errors.append(f"GM25 memory {row['Location']}: missing NSC ID comment")
            continue
        nsc_id = parts[0]
        channel = canonical.get(nsc_id)
        if channel is None:
            errors.append(f"GM25 memory {row['Location']}: unknown {nsc_id}")
            continue
        allowed_tx = (
            channel["service"] == "GMRS"
            and channel["status"] == "SELECTED"
            and channel["receive_only"] == "NO"
        )
        if not allowed_tx and row["Duplex"] != "off":
            errors.append(f"{nsc_id}: GM25 test export failed to inhibit TX")
        if channel["status"] == "RESERVED":
            errors.append(f"{nsc_id}: reserved record was exported")
    return errors


def main() -> int:
    rows = read_csv(DATA)
    errors = validate_channels(rows) + validate_profiles() + validate_gm25_export(rows)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1
    populated = sum(bool(row["rx_frequency"]) for row in rows)
    reserved = sum(row["status"] == "RESERVED" for row in rows)
    print(
        "Validation passed: "
        f"128 canonical positions, {populated} populated, {reserved} safely reserved; "
        "production export remains disabled."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
