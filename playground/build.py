"""Copy abkit and the example experiments next to the playground page (playground/site/), for Pyodide.

    python playground/build.py
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "playground" / "site"


def main() -> None:
    shutil.rmtree(SITE, ignore_errors=True)
    (SITE / "py" / "abkit").mkdir(parents=True)
    files = []
    for f in sorted((ROOT / "abkit").glob("*.py")):
        shutil.copy(f, SITE / "py" / "abkit" / f.name)
        files.append(f"abkit/{f.name}")
    (SITE / "examples").mkdir()
    for name in ("checkout_experiment.csv", "checkout_experiment_broken.csv"):
        shutil.copy(ROOT / "data" / name, SITE / "examples" / name)
    (SITE / "manifest.json").write_text(json.dumps({"files": files}))
    shutil.copy(ROOT / "playground" / "index.html", SITE / "index.html")
    print(f"built {SITE}")


if __name__ == "__main__":
    main()
