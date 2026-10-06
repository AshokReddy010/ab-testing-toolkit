"""Analyse an experiment file and write the readout.

    python scripts/run_readout.py data/checkout_experiment.csv "Checkout redesign"
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from abkit import analyse_experiment, render_readout  # noqa: E402


def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/checkout_experiment.csv")
    name = sys.argv[2] if len(sys.argv) > 2 else "Checkout redesign"
    readout = analyse_experiment(pd.read_csv(path), name=name)
    text = render_readout(readout)
    out = Path("reports") / f"{path.stem}_readout.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(text)
    print(f"Saved to {out}")


if __name__ == "__main__":
    main()
