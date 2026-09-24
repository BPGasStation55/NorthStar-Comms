from __future__ import annotations

import csv
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_nsc.py"
BUILDER = ROOT / "scripts" / "build_exports.py"
CANONICAL = ROOT / "data" / "master_channels.csv"
GM25_EXPORT = ROOT / "exports" / "test" / "gm25" / "NSC_GM25_CHIRP_TEST_ONLY.csv"


def read_csv(path: Path, encoding: str = "utf-8") -> list[dict[str, str]]:
    with path.open(encoding=encoding, newline="") as handle:
        return list(csv.DictReader(handle))


class TestBaseline(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run(
            [sys.executable, str(BUILDER), "--radio", "all"],
            cwd=ROOT,
            check=True,
        )

    def test_validator_passes(self) -> None:
        subprocess.run([sys.executable, str(VALIDATOR)], cwd=ROOT, check=True)

    def test_canonical_plan_has_exact_ranges(self) -> None:
        rows = read_csv(CANONICAL)
        self.assertEqual(len(rows), 128)
        expected = [
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
        for start, end, bank in expected:
            self.assertTrue(all(row["bank"] == bank for row in rows[start - 1 : end]))

    def test_receive_only_records_have_no_tx_frequency(self) -> None:
        rows = read_csv(CANONICAL)
        self.assertTrue(
            all(not row["tx_frequency"] for row in rows if row["receive_only"] == "YES")
        )

    def test_reserved_records_have_no_frequency(self) -> None:
        rows = read_csv(CANONICAL)
        self.assertTrue(
            all(
                not row["rx_frequency"] and not row["tx_frequency"]
                for row in rows
                if row["status"] == "RESERVED"
            )
        )

    def test_gm25_export_inhibits_nonapproved_tx(self) -> None:
        canonical = {row["nsc_id"]: row for row in read_csv(CANONICAL)}
        exported = read_csv(GM25_EXPORT, encoding="utf-8-sig")
        self.assertGreater(len(exported), 0)
        for row in exported:
            nsc_id = row["Comment"].split()[0]
            source = canonical[nsc_id]
            allowed = (
                source["service"] == "GMRS"
                and source["status"] == "SELECTED"
                and source["receive_only"] == "NO"
            )
            if not allowed:
                self.assertEqual(row["Duplex"], "off", nsc_id)

    def test_gm25_manifest_is_test_only(self) -> None:
        manifest = json.loads(
            (GM25_EXPORT.parent / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["artifact_status"], "TEST_ONLY")
        self.assertFalse(manifest["production_release_enabled"])
        self.assertEqual(manifest["hardware_validation_status"], "pending")

    def test_unverified_exporters_are_blocked(self) -> None:
        for radio in ("uv5r", "dm32uv", "uv32"):
            completed = subprocess.run(
                [sys.executable, str(BUILDER), "--radio", radio],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 2, radio)
            self.assertIn("BLOCKED:", completed.stdout)

    def test_dm32uv_and_uv32_are_separate(self) -> None:
        dm32 = json.loads((ROOT / "profiles" / "dm32uv_cps.json").read_text())
        uv32 = json.loads((ROOT / "profiles" / "uv32_cps.json").read_text())
        self.assertNotEqual(dm32["radio_model_id"], uv32["radio_model_id"])
        self.assertEqual(dm32["memory_count"], 4000)
        self.assertEqual(uv32["schema_status"], "reference_only")

    def test_radio_model_registry_is_explicit(self) -> None:
        models = {row["radio_model_id"]: row for row in read_csv(ROOT / "data" / "radio_models.csv")}
        self.assertEqual(models["RMD-003"]["model"], "DM-32UV")
        self.assertEqual(models["RMD-004"]["model"], "UV-32")
        self.assertEqual(models["RMD-004"]["support_status"], "REFERENCE_ONLY")

    def test_markdown_fences_are_balanced(self) -> None:
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            count = sum(
                line.lstrip().startswith("```")
                for line in path.read_text(encoding="utf-8").splitlines()
            )
            self.assertEqual(count % 2, 0, str(path.relative_to(ROOT)))

    def test_legacy_uppercase_directories_are_gone(self) -> None:
        for name in (
            "Archive", "Assets", "Database", "Documentation", "Exports",
            "Maps", "Scripts", "Tests",
        ):
            self.assertFalse((ROOT / name).exists(), name)


if __name__ == "__main__":
    unittest.main()
