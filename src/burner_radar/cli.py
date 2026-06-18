"""Command-line entry point: `python -m burner_radar` or `burner-radar`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .collector import build


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="burner-radar")
    sub = parser.add_subparsers(dest="cmd", required=True)

    build_p = sub.add_parser("build", help="Rebuild data/domains.{txt,json}")
    build_p.add_argument("--data-dir", default="data", help="Output directory (default: ./data)")

    args = parser.parse_args(argv)

    if args.cmd == "build":
        data_dir = Path(args.data_dir).resolve()
        data_dir.mkdir(parents=True, exist_ok=True)
        summary = build(data_dir)
        print(f"[done] {summary['count']} domains written to {data_dir}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
