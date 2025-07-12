#!/usr/bin/env python3


import re, sys, json, argparse
from pathlib import Path
from typing import Dict, List

import requests
from rich import print
from rich.table import Table

CACHE = Path(__file__).with_name("patterns_cache.json")
SOURCES = {
    "secrets-patterns-db":
    "https://raw.githubusercontent.com/mazen160/secrets-patterns-db/main/secrets.json",
    "trufflehog": 
    "https://raw.githubusercontent.com/dxa4481/truffleHogRegexes/master/truffleHogRegexes/regexes.json",
}

# ───────────────────────────────────────── patterns loader
def fetch_and_merge(force=False) -> List[Dict]:
    if CACHE.exists() and not force:
        return json.loads(CACHE.read_text())

    merged = []
    for name, url in SOURCES.items():
        try:
            print(f"[cyan]↯  Fetching {name} patterns…")
            data = requests.get(url, timeout=15).json()
            if name == "secrets-patterns-db":
                for item in data:
                    merged.append({"name": item["name"], "regex": item["regex"]})
            else:
                for item in data.values():
                    merged.append({"name": item["Name"], "regex": item["Regex"]})
        except Exception as e:
            print(f"[red]Failed to pull {name}: {e}")

    uniq = {}
    for m in merged:
        uniq[m["regex"]] = m
    CACHE.write_text(json.dumps(list(uniq.values()), ensure_ascii=False, indent=2))
    return list(uniq.values())

PATTERNS = fetch_and_merge()

# ───────────────────────────────────────── identifier
def identify(key: str):
    matches = [(p["name"], len(p["regex"])) for p in PATTERNS
               if re.fullmatch(p["regex"], key)]
    if not matches:
        return None, 0.0
    best = min(matches, key=lambda x: x[1])
    confidence = 1 / (matches.index(best) + 1)
    return best[0], round(confidence, 3)

# ───────────────────────────────────────── CLI
def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Identify API keys")
    scan.add_argument("file", help="Keys file or - for stdin")

    upd = sub.add_parser("update-patterns", help="Refresh patterns cache")

    args = ap.parse_args()

    if args.cmd == "update-patterns":
        fetch_and_merge(force=True)
        print("[green]✓ Patterns cache refreshed.")
        sys.exit(0)

    keys = (Path(args.file).read_text().splitlines()
            if args.file != "-" else sys.stdin.read().splitlines())

    table = Table(title="API Key Scanner Results")
    table.add_column("Key")
    table.add_column("Service")
    table.add_column("Confidence")

    for k in keys:
        svc, conf = identify(k)
        table.add_row(k, svc or "-", f"{conf:.2f}")

    print(table)

if __name__ == "__main__":
    main()
