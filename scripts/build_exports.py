#!/usr/bin/env python3
"""Build explicitly test-only NorthStar Comms exports from canonical data."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "master_channels.csv"
PROFILES = ROOT / "profiles"
TEST_EXPORTS = ROOT / "exports" / "test"

PROFILE_FILES = {
    "gm25": "gm25_chirp.json",
    "uv5r": "uv5r_baofeng_stock.json",
    "dm32uv": "dm32uv_cps.json",
    "uv32": "uv32_cps.json",
}


def read_channels() -> list[dict[str, str]]:
    with DATA.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def read_profile(radio: str) -> dict:
    with (PROFILES / PROFILE_FILES[radio]).open(encoding="utf-8") as handle:
        return json.load(handle)


def frequency_supported(frequency: float, ranges: list[list[float]]) -> bool:
    return any(low <= frequency <= high for low, high in ranges)


def tone_fields(channel: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    encode = channel["tone_encode"]
    decode = channel["tone_decode"]
    empty = {"", "NONE"}
    tone = ""
    rtone = "88.5"
    ctone = "88.5"
    dtcs = "023"
    rxdtcs = "023"
    cross = "Tone->Tone"

    encode_dcs = encode.startswith("D")
    decode_dcs = decode.startswith("D")
    if encode not in empty and decode in empty and not encode_dcs:
        tone, rtone = "Tone", encode
    elif encode not in empty and encode == decode and not encode_dcs:
        tone, rtone, ctone = "TSQL", encode, decode
    elif encode_dcs and decode_dcs and encode == decode:
        tone, dtcs, rxdtcs = "DTCS", encode[1:4], decode[1:4]
    elif encode not in empty or decode not in empty:
        tone = "Cross"
    return tone, rtone, ctone, dtcs, rxdtcs, cross


def tx_allowed(channel: dict[str, str], profile: dict) -> bool:
    return (
        channel["status"] == "SELECTED"
        and channel["receive_only"] == "NO"
        and channel["service"] in profile["transmit_services"]
        and bool(channel["tx_frequency"])
    )


def build_gm25(channels: list[dict[str, str]], profile: dict) -> Path:
    output = TEST_EXPORTS / "gm25" / "NSC_GM25_CHIRP_TEST_ONLY.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str | int]] = []

    for channel in channels:
        if not channel["rx_frequency"]:
            continue
        rx = float(channel["rx_frequency"])
        if not frequency_supported(rx, profile["receive_ranges_mhz"]):
            continue

        allow_tx = tx_allowed(channel, profile)
        tone, rtone, ctone, dtcs, rxdtcs, cross = tone_fields(channel)
        if allow_tx:
            tx = float(channel["tx_frequency"])
            if abs(tx - rx) < 0.000001:
                duplex, offset = "", profile["defaults"]["Offset"]
            else:
                duplex = "+" if tx > rx else "-"
                offset = f"{abs(tx - rx):.6f}"
        else:
            duplex, offset = "off", "0.000000"
            tone = ""

        rows.append(
            {
                "Location": int(channel["sequence"]),
                "Name": channel["name_short"][: profile["name_limit"]],
                "Frequency": f"{rx:.6f}",
                "Duplex": duplex,
                "Offset": offset,
                "Tone": tone,
                "rToneFreq": rtone,
                "cToneFreq": ctone,
                "DtcsCode": dtcs,
                "DtcsPolarity": profile["defaults"]["DtcsPolarity"],
                "RxDtcsCode": rxdtcs,
                "CrossMode": cross,
                "Mode": channel["bandwidth"],
                "TStep": profile["defaults"]["TStep"],
                "Skip": "S" if channel["scan_policy"] == "SKIP" else "",
                "Power": profile["power_map"][channel["power_policy"]],
                "Comment": f"{channel['nsc_id']} {channel['service']} {channel['status']} TEST ONLY",
                "URCALL": "",
                "RPT1CALL": "",
                "RPT2CALL": "",
                "DVCODE": "",
            }
        )

    write_csv(output, profile["headers"], rows)
    manifest = {
        "artifact_status": "TEST_ONLY",
        "profile_id": profile["profile_id"],
        "schema_status": profile["schema_status"],
        "hardware_validation_status": profile["hardware_validation_status"],
        "production_release_enabled": False,
        "row_count": len(rows),
        "safety": "All non-selected, receive-only and unsupported-service records use CHIRP duplex=off.",
    }
    (output.parent / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return output


def write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=headers, extrasaction="ignore", lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def build_one(radio: str, channels: list[dict[str, str]]) -> Path:
    profile = read_profile(radio)
    if not profile.get("export_enabled", False):
        raise RuntimeError(
            f"{radio} export blocked: {profile.get('blocking_reason', 'profile is disabled')}"
        )
    if profile.get("production_release_enabled", False):
        raise RuntimeError(
            f"{radio} profile unexpectedly enables production release before validation"
        )
    if radio == "gm25":
        return build_gm25(channels, profile)
    raise RuntimeError(f"{radio} has no approved exporter")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--radio", choices=["all", *PROFILE_FILES], default="all"
    )
    args = parser.parse_args()
    channels = read_channels()

    selected = list(PROFILE_FILES) if args.radio == "all" else [args.radio]
    blocked: list[str] = []
    built: list[Path] = []
    for radio in selected:
        try:
            built.append(build_one(radio, channels))
        except RuntimeError as error:
            blocked.append(str(error))

    for path in built:
        print(f"Built test artifact: {path.relative_to(ROOT)}")
    for message in blocked:
        print(f"BLOCKED: {message}")

    if args.radio != "all" and blocked:
        return 2
    if not built:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
