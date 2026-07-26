from pathlib import Path
import csv
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_validation_and_build():
    subprocess.run([sys.executable, str(ROOT/"scripts/validate_nsc.py")], check=True)
    subprocess.run([sys.executable, str(ROOT/"scripts/build_exports.py"), "--radio", "all"], check=True)

    expected = [
        ROOT/"exports/gm25/NSC_GM25_CHIRP_v2.csv",
        ROOT/"exports/uv5r/NSC_UV5R_BAOFENG_STOCK_v2_PROVISIONAL.csv",
        ROOT/"exports/uv32/NSC_UV32_CPS_v2.csv",
    ]
    for path in expected:
        assert path.exists()
        with path.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f))
        assert len(rows) == 129
