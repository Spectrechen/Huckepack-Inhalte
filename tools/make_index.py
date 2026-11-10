#!/usr/bin/env python3
"""Writes index.json: the catalog the Huckepack app shows in the parent area.

Run after check_format.py succeeded:  python3 tools/make_index.py > index.json
On GitHub this runs automatically after every change on main; nobody needs to edit index.json by hand.
Only the standard library is used.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


entries = []
packs_dir = os.path.join(ROOT, "packs")
for name in sorted(os.listdir(packs_dir)):
    folder = os.path.join(packs_dir, name)
    pack_file = os.path.join(folder, "pack.json")
    if not os.path.isfile(pack_file):
        continue
    with open(pack_file, encoding="utf-8") as f:
        p = json.load(f)
    files = []
    image = (p.get("world") or {}).get("image")
    if image:
        path = os.path.join(folder, image["file"])
        files.append({"name": image["file"], "bytes": os.path.getsize(path), "sha256": sha256(path)})
    levels = p.get("levels", [])
    entries.append({
        "id": p["id"],
        "version": p["version"],
        "title": p["title"],
        "description": p.get("description"),
        "author": p["author"],
        "licence": p["licence"],
        "levels": len(levels),
        "grades": sorted({l["grade"] for l in levels}),
        "subjects": sorted({l["subject"] for l in levels}),
        "courses": [c["title"] for c in p.get("courses", [])],
        "places": len((p.get("world") or {}).get("nodes", [])) if p.get("world") else None,
        "path": "packs/%s/" % name,
        "bytes": os.path.getsize(pack_file),
        "sha256": sha256(pack_file),
        "files": files,
    })

json.dump({"schemaVersion": 1, "packs": entries}, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
sys.stdout.write("\n")
