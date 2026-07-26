#!/usr/bin/env python3
"""Generate NorthStar Comms radio-programming exports from the canonical channel database."""

from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "master_channels.csv"
PROFILES = ROOT / "profiles"
EXPORTS = ROOT / "exports"


def read_channels() -> list[dict[str, str]]:
    with DATA.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def read_profile(name: str) -> dict:
    with (PROFILES / name).open(encoding="utf-8") as f:
        return json.load(f)


def tone_fields(ch: dict[str, str]) -> tuple[str, str, str, str, str, str]:
    enc = ch["tone_encode"]
    dec = ch["tone_decode"]
    empty = {"", "None", None}
    tone = ""
    rtone = "88.5"
    ctone = "88.5"
    dtcs = "023"
    rxdtcs = "023"
    cross = "Tone->Tone"

    enc_is_dcs = isinstance(enc, str) and enc.startswith("D")
    dec_is_dcs = isinstance(dec, str) and dec.startswith("D")

    if enc not in empty and dec in empty and not enc_is_dcs:
        tone, rtone = "Tone", enc
    elif enc not in empty and dec not in empty and enc == dec and not enc_is_dcs:
        tone, rtone, ctone = "TSQL", enc, dec
    elif enc_is_dcs and dec_is_dcs and enc == dec:
        tone = "DTCS"
        dtcs = enc[1:4]
        rxdtcs = dec[1:4]
    elif enc not in empty or dec not in empty:
        tone = "Cross"

    return tone, rtone, ctone, dtcs, rxdtcs, cross


def build_gm25(channels: list[dict[str, str]]) -> Path:
    p = read_profile("gm25_chirp.json")
    out = EXPORTS / "gm25" / "NSC_GM25_CHIRP_v2.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for ch in channels[:p["export_count"]]:
        seq = int(ch["sequence"])
        rx = float(ch["rx_frequency"])
        tx = float(ch["tx_frequency"])
        tone, rtone, ctone, dtcs, rxdtcs, cross = tone_fields(ch)

        if ch["receive_only"] == "Yes" or ch["status"] == "Reserved":
            duplex = "off"
        elif abs(tx - rx) < 0.000001:
            duplex = ""
        elif tx > rx:
            duplex = "+"
        else:
            duplex = "-"

        offset = p["defaults"]["Offset"] if duplex == "" else (
            f"{abs(tx-rx):.6f}" if duplex in {"+", "-"} else "0.000000"
        )

        rows.append({
            "Location": seq,
            "Name": ch["name_short"][:p["name_limit"]],
            "Frequency": f"{rx:.6f}",
            "Duplex": duplex,
            "Offset": offset,
            "Tone": tone,
            "rToneFreq": rtone,
            "cToneFreq": ctone,
            "DtcsCode": dtcs,
            "DtcsPolarity": p["defaults"]["DtcsPolarity"],
            "RxDtcsCode": rxdtcs,
            "CrossMode": cross,
            "Mode": ch["bandwidth"],
            "TStep": p["defaults"]["TStep"],
            "Skip": "S" if ch["scan_policy"] == "skip" else "",
            "Power": p["power_map"].get(ch["power_policy"], "3.0W"),
            "Comment": f"{ch['nsc_id']} {ch['status']}",
            "URCALL": "",
            "RPT1CALL": "",
            "RPT2CALL": "",
            "DVCODE": "",
        })

    write_csv(out, p["headers"], rows)
    return out


def build_uv5r(channels: list[dict[str, str]]) -> Path:
    p = read_profile("uv5r_baofeng_stock.json")
    out = EXPORTS / "uv5r" / "NSC_UV5R_BAOFENG_STOCK_v2_PROVISIONAL.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for ch in channels[:p["export_count"]]:
        freq = float(ch["rx_frequency"])
        rows.append({
            "Channel": ch["sequence"],
            "Band": "VHF" if freq < 300 else "UHF",
            "RX Frequency": ch["rx_frequency"],
            "TX Frequency": ch["tx_frequency"],
            "CTCSS/DCS Dec": ch["tone_decode"] or "None",
            "CTCSS/DCS Enc": ch["tone_encode"] or "None",
            "TX Power": ch["power_policy"],
            "W/N": "Narrow" if ch["bandwidth"] == "NFM" else "Wide",
            "PTT-ID": p["defaults"]["PTT-ID"],
            "BusyLock": p["defaults"]["BusyLock"],
            "Scan_Add": "No" if ch["scan_policy"] == "skip" else p["defaults"]["Scan_Add"],
            "SigCode": p["defaults"]["SigCode"],
            "CH-Name": ch["name_long"],
        })

    write_csv(out, p["headers"], rows)
    return out


def build_uv32(channels: list[dict[str, str]]) -> Path:
    p = read_profile("uv32_cps.json")
    out = EXPORTS / "uv32" / "NSC_UV32_CPS_v2.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for ch in channels[:p["export_count"]]:
        rows.append({
            "Channel #": ch["sequence"],
            "Name": ch["name_long"][:p["name_limit"]],
            "Type": p["defaults"]["Type"],
            "RX Frequency": ch["rx_frequency"],
            "TX Frequency": ch["tx_frequency"],
            "Power": ch["power_policy"],
            "Width": p["width_map"][ch["bandwidth"]],
            "CTS/DCS Decode": ch["tone_decode"] or "None",
            "CTS/DCE Encode": ch["tone_encode"] or "None",
            "Color Code": p["defaults"]["Color Code"],
            "TX Contact": p["defaults"]["TX Contact"],
            "RX Group List": p["defaults"]["RX Group List"],
            "Time Slot": p["defaults"]["Time Slot"],
        })

    write_csv(out, p["headers"], rows)
    return out


def write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--radio", choices=["all", "gm25", "uv5r", "uv32"], default="all")
    args = parser.parse_args()
    channels = read_channels()

    builders = {"gm25": build_gm25, "uv5r": build_uv5r, "uv32": build_uv32}
    selected = builders if args.radio == "all" else {args.radio: builders[args.radio]}
    for name, builder in selected.items():
        print(f"{name}: {builder(channels)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
