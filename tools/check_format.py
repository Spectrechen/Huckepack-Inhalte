#!/usr/bin/env python3
"""Format check for Huckepack content packs (no app needed). The full check is huckepack-lint in the app."""
import json, re, sys

PLACES = {"numbers-hill", "mill", "market", "clock-tower", "syllable-school", "library", "post-office", "farm",
          "weather-station", "crossing", "bus-stop", "tea-house", "zoo", "lighthouse"}
TYPES = {"splitInfo", "relay", "matchPairs", "bothAgree"}
SUBJECTS = {"math", "german", "science", "english"}
PART = re.compile(r"^[a-z0-9-]+$")

def check(path):
    errors = []
    raw = open(path, "rb").read()
    if len(raw) > 512 * 1024: errors.append("larger than 512 KB")
    p = json.loads(raw)
    pid = p.get("id", "")
    parts = pid.split(".")
    if len(parts) < 3 or not all(PART.match(x) for x in parts): errors.append(f"pack id '{pid}' must look like de.author.name")
    for key in ("version", "title", "author", "licence", "levels"):
        if key not in p: errors.append(f"missing '{key}'")
    if not isinstance(p.get("version"), int) or p.get("version", 0) < 1: errors.append("version must be an integer >= 1")
    if "de" not in p.get("title", {}): errors.append("title needs 'de'")
    levels = p.get("levels", [])
    if not 1 <= len(levels) <= 20: errors.append("1-20 levels")
    for l in levels:
        lid = l.get("id", "")
        if not lid.startswith(pid + "/") or len(lid) <= len(pid) + 1: errors.append(f"level id '{lid}' must start with '{pid}/'")
        if l.get("place") not in PLACES: errors.append(f"{lid}: unknown place '{l.get('place')}'")
        if l.get("subject") not in SUBJECTS: errors.append(f"{lid}: unknown subject '{l.get('subject')}'")
        if l.get("schemaVersion") != 1: errors.append(f"{lid}: schemaVersion must be 1")
        tasks = l.get("tasks", [])
        if not tasks: errors.append(f"{lid}: no tasks")
        ids = [t.get("id") for t in tasks]
        if len(ids) != len(set(ids)): errors.append(f"{lid}: duplicate task ids")
        for t in tasks:
            if t.get("type") not in TYPES: errors.append(f"{lid}/{t.get('id')}: unknown type '{t.get('type')}'")
            if not t.get("skills"): errors.append(f"{lid}/{t.get('id')}: no skills")
    return errors

failed = False
for path in sys.argv[1:]:
    try: errs = check(path)
    except Exception as e: errs = [str(e)]
    for e in errs: print(f"✗ {path}: {e}")
    if errs: failed = True
    else: print(f"✓ {path}")
sys.exit(1 if failed else 0)
