#!/usr/bin/env python3
"""Format check for Huckepack packs (no app needed, standard library only).

Level packs (no "world"): levels go to places of the Huckepack map.
World packs ("world" present): own map image, places, paths and courses.
The full check is huckepack-lint in the app repository; this script catches the common mistakes.

    python3 tools/check_format.py packs/*/pack.json
"""
import json, os, re, struct, sys

PLACES = {"numbers-hill", "mill", "market", "clock-tower", "syllable-school", "library", "post-office", "farm",
          "weather-station", "crossing", "bus-stop", "tea-house", "zoo", "lighthouse"}
TYPES = {"splitInfo", "relay", "matchPairs", "bothAgree"}
SUBJECTS = {"math", "german", "science", "english"}
FORMATS = {"integer", "euroCents", "time", "minutes"}
OPS = {"add", "subtract", "multiply", "divide"}
MINIGAMES = {"ticTacToe", "dotsAndBoxes"}
EUROS = {1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000}
PART = re.compile(r"^[a-z0-9-]+$")
SKILL = re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)+$")
MAX_LEVELS, MAX_BYTES, MAX_IMAGE_BYTES, MAX_PLACES = 40, 512 * 1024, 8 * 1024 * 1024, 60


def image_size(path):
    """Width and height of a PNG or JPEG from its header, or None."""
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:2] == b"\xff\xd8":
            f.seek(2)
            while True:
                marker = f.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    return None
                if marker[1] in (0xD8, 0x01) or 0xD0 <= marker[1] <= 0xD7:
                    continue
                size = f.read(2)
                if len(size) < 2:
                    return None
                length = struct.unpack(">H", size)[0]
                if marker[1] in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    data = f.read(5)
                    h, w = struct.unpack(">HH", data[1:5])
                    return w, h
                f.seek(length - 2, 1)
    return None


def is_text(v):
    return isinstance(v, dict) and isinstance(v.get("de"), str) and v["de"] != "" and all(isinstance(x, str) for x in v.values())


def check_visual(where, v, errors):
    if not isinstance(v, dict) or len(v) != 1:
        errors.append(f"{where}: visual must have exactly one of clock, digitalClock, money")
        return
    (kind, body), = v.items()
    if kind in ("clock", "digitalClock"):
        h, m = (body or {}).get("hour"), (body or {}).get("minute")
        if not (isinstance(h, int) and isinstance(m, int) and 0 <= h <= 23 and 0 <= m <= 59):
            errors.append(f"{where}: {kind} needs hour 0-23 and minute 0-59")
    elif kind == "money":
        cents = (body or {}).get("cents")
        if not (isinstance(cents, list) and 1 <= len(cents) <= 12 and all(c in EUROS for c in cents)):
            errors.append(f"{where}: money.cents needs 1-12 values from {sorted(EUROS)}")
    else:
        errors.append(f"{where}: unknown visual '{kind}'")


def check_task(where, t, errors):
    kind = t.get("type")
    if kind not in TYPES:
        errors.append(f"{where}: unknown type '{kind}'")
        return
    if not t.get("id"):
        errors.append(f"{where}: task without id")
    skills = t.get("skills")
    if not skills or not isinstance(skills, list):
        errors.append(f"{where}: no skills")
    elif not all(isinstance(s, str) and SKILL.match(s) for s in skills):
        errors.append(f"{where}: malformed skill id (a.b.c, lowercase, digits, hyphens)")
    if t.get("difficulty", 2) not in (1, 2, 3):
        errors.append(f"{where}: difficulty must be 1, 2 or 3")

    def need_text(*keys):
        for k in keys:
            if not is_text(t.get(k)):
                errors.append(f"{where}: '{k}' must be a text with 'de'")

    fmt = t.get("answerFormat")
    if fmt is not None and fmt not in FORMATS:
        errors.append(f"{where}: unknown answerFormat '{fmt}'")
    for key in ("clueVisual", "questionVisual"):
        if key in t:
            check_visual(f"{where}.{key}", t[key], errors)

    if kind == "splitInfo":
        need_text("clue", "prompt")
        a = t.get("answer")
        if not isinstance(a, int) or isinstance(a, bool) or a < 0:
            errors.append(f"{where}: answer must be an integer >= 0")
        elif fmt == "time" and not 0 <= a < 1440:
            errors.append(f"{where}: time answer must be minutes since midnight (0-1439)")
    elif kind == "relay":
        need_text("first", "second")
        a = t.get("firstAnswer")
        if not isinstance(a, int) or isinstance(a, bool) or a < 0:
            errors.append(f"{where}: firstAnswer must be an integer >= 0")
        op = t.get("operation") or {}
        if op.get("op") not in OPS or not isinstance(op.get("operand"), int):
            errors.append(f"{where}: operation needs op ({', '.join(sorted(OPS))}) and an integer operand")
        elif op["op"] == "divide" and (op["operand"] == 0 or (isinstance(a, int) and a % op["operand"] != 0)):
            errors.append(f"{where}: relay division must be exact")
        if isinstance(t.get("second"), dict) and not all("{x}" in str(v) for v in t["second"].values()):
            errors.append(f"{where}: 'second' needs {{x}} in every language")
        if isinstance(a, int) and isinstance(op.get("operand"), int) and op.get("op") in OPS:
            r = {"add": lambda: a + op["operand"], "subtract": lambda: a - op["operand"],
                 "multiply": lambda: a * op["operand"],
                 "divide": lambda: a // op["operand"] if op["operand"] else 0}[op["op"]]()
            if r < 0:
                errors.append(f"{where}: second answer would be negative ({r}); kids cannot type that")
            if fmt == "time" and not (0 <= a < 1440 and 0 <= r < 1440):
                errors.append(f"{where}: with answerFormat time both answers must be 0-1439")
    elif kind == "matchPairs":
        need_text("prompt")
        pairs = t.get("pairs")
        if not isinstance(pairs, list) or not 2 <= len(pairs) <= 6:
            errors.append(f"{where}: matchPairs needs 2-6 pairs")
        else:
            for i, p in enumerate(pairs):
                for side in ("left", "right"):
                    if not is_text(p.get(side)):
                        errors.append(f"{where}.pairs[{i}]: '{side}' must be a text with 'de'")
                    if f"{side}Visual" in p:
                        check_visual(f"{where}.pairs[{i}].{side}Visual", p[f"{side}Visual"], errors)
            if len({json.dumps(p.get("left"), sort_keys=True) for p in pairs}) != len(pairs) or \
               len({json.dumps(p.get("right"), sort_keys=True) for p in pairs}) != len(pairs):
                errors.append(f"{where}: matchPairs halves must be unique")
    elif kind == "bothAgree":
        need_text("question")
        opts = t.get("options")
        if not isinstance(opts, list) or not 2 <= len(opts) <= 4:
            errors.append(f"{where}: bothAgree needs 2-4 options")
        else:
            ids = [o.get("id") for o in opts]
            if len(set(ids)) != len(ids) or not all(ids):
                errors.append(f"{where}: option ids must be non-empty and unique")
            if t.get("correct") not in ids:
                errors.append(f"{where}: 'correct' must be the id of one option")
            for o in opts:
                if not is_text(o.get("text")):
                    errors.append(f"{where}: option '{o.get('id')}' needs a text with 'de'")
                if "visual" in o:
                    check_visual(f"{where}.option {o.get('id')}", o["visual"], errors)


def check_world(path, p, levels, courses, errors):
    w = p["world"]
    if not isinstance(w, dict):
        errors.append("world must be an object")
        return
    base = os.path.dirname(os.path.abspath(path))
    img = w.get("image")
    if not isinstance(img, dict):
        errors.append("world needs an 'image' (file, width, height)")
    else:
        f = str(img.get("file", ""))
        if not f or "/" in f or f.startswith(".") or not f.lower().endswith((".jpg", ".jpeg", ".png")):
            errors.append("image.file must be a .jpg or .png file name next to pack.json")
        iw, ih = img.get("width"), img.get("height")
        if not (isinstance(iw, int) and isinstance(ih, int) and 512 <= iw <= 8192 and 512 <= ih <= 8192):
            errors.append("image width and height must be 512-8192 px")
        full = os.path.join(base, f)
        if f and os.path.isfile(full):
            if os.path.getsize(full) > MAX_IMAGE_BYTES:
                errors.append(f"image {f} is larger than 8 MB")
            size = image_size(full)
            if size is None:
                errors.append(f"image {f} is not a readable JPEG or PNG")
            elif isinstance(iw, int) and isinstance(ih, int) and tuple(size) != (iw, ih):
                errors.append(f"image {f} is {size[0]}x{size[1]} px but pack.json says {iw}x{ih}")
        elif f:
            errors.append(f"image {f} not found next to pack.json")

    nodes = w.get("nodes")
    if not isinstance(nodes, list) or not 1 <= len(nodes) <= MAX_PLACES:
        errors.append(f"world needs 1-{MAX_PLACES} places")
        return
    ids = [n.get("id") for n in nodes]
    if len(set(ids)) != len(ids) or not all(ids):
        errors.append("place ids must be non-empty and unique")
    # Levels a place may enter or require: those without 'place' (bands cannot).
    plain = {l["id"] for l in levels if not l.get("place")}
    node_levels = set()
    for n in nodes:
        nid = n.get("id")
        for axis in ("x", "y"):
            v = n.get(axis)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not 0 <= v <= 1:
                errors.append(f"place '{nid}': {axis} must be a number between 0 and 1")
        if "requires" in n and not isinstance(n["requires"], list):
            errors.append(f"place '{nid}': 'requires' must be a list")
        if "title" in n and not is_text(n["title"]):
            errors.append(f"place '{nid}': title needs 'de'")
        if n.get("level") is not None and n.get("miniGame") is not None:
            errors.append(f"place '{nid}': has level and miniGame")
        if n.get("miniGame") is not None and n["miniGame"] not in MINIGAMES:
            errors.append(f"place '{nid}': unknown miniGame '{n['miniGame']}'")
        lv = n.get("level")
        if lv is not None:
            node_levels.add(nid)
            if lv not in plain:
                errors.append(f"place '{nid}': level '{lv}' is not a level of this pack without 'place'")
        for r in n.get("requires", []) if isinstance(n.get("requires"), list) else []:
            if r not in plain:
                errors.append(f"place '{nid}': required level '{r}' is not a level of this pack without 'place'")
    if w.get("start") not in ids:
        errors.append("start must be the id of a place")
    for pa in w.get("paths", []):
        if not (isinstance(pa, list) and len(pa) == 2 and all(x in ids for x in pa)):
            errors.append(f"bad path {pa}: needs two place ids")
    for l in levels:
        place = l.get("place")
        if place is not None and place not in node_levels:
            errors.append(f"{l['id']}: place '{place}' is not a place of this world that has a level")


def check(path):
    errors = []
    raw = open(path, "rb").read()
    if len(raw) > MAX_BYTES:
        errors.append("larger than 512 KB")
    p = json.loads(raw)
    pid = p.get("id", "")
    parts = pid.split(".")
    if len(parts) < 3 or not all(PART.match(x) for x in parts):
        errors.append(f"pack id '{pid}' must look like de.author.name")
    folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
    if folder != pid:
        errors.append(f"folder '{folder}' must be named like the pack id '{pid}'")
    for key in ("version", "title", "author", "licence", "levels"):
        if key not in p:
            errors.append(f"missing '{key}'")
    if not isinstance(p.get("version"), int) or p.get("version", 0) < 1:
        errors.append("version must be an integer >= 1")
    if not is_text(p.get("title")):
        errors.append("title needs 'de'")
    if "description" in p and not is_text(p["description"]):
        errors.append("description needs 'de'")
    for name in p.get("skills", {}):
        if not SKILL.match(name):
            errors.append(f"skill name '{name}' is malformed")
    courses = set()
    for c in p.get("courses", []):
        cid = c.get("id", "")
        if not PART.match(cid) or len(cid) > 40 or cid in SUBJECTS:
            errors.append(f"course id '{cid}' malformed or built-in")
        if cid in courses:
            errors.append(f"duplicate course '{cid}'")
        courses.add(cid)
        if not is_text(c.get("title")):
            errors.append(f"course '{cid}': title needs 'de'")

    levels = p.get("levels", [])
    if not 1 <= len(levels) <= MAX_LEVELS:
        errors.append(f"1-{MAX_LEVELS} levels")
    is_world = "world" in p
    level_ids = [l.get("id") for l in levels]
    if len(set(level_ids)) != len(level_ids):
        errors.append("duplicate level ids")
    for l in levels:
        lid = l.get("id", "")
        if not lid.startswith(pid + "/") or len(lid) <= len(pid) + 1:
            errors.append(f"level id '{lid}' must start with '{pid}/'")
        if not is_text(l.get("title")):
            errors.append(f"{lid}: title needs 'de'")
        if not is_world and l.get("place") not in PLACES:
            errors.append(f"{lid}: unknown place '{l.get('place')}'")
        subject = l.get("subject")
        if subject not in SUBJECTS and subject not in courses:
            errors.append(f"{lid}: subject '{subject}' is neither built-in ({', '.join(sorted(SUBJECTS))}) nor in 'courses'")
        if l.get("schemaVersion", 1) != 1:
            errors.append(f"{lid}: schemaVersion must be 1")
        g = l.get("grade")
        if not isinstance(g, int) or isinstance(g, bool) or not 1 <= g <= 13:
            errors.append(f"{lid}: grade must be 1-13")
        tasks = l.get("tasks", [])
        if not tasks:
            errors.append(f"{lid}: no tasks")
        ids = [t.get("id") for t in tasks]
        if len(ids) != len(set(ids)):
            errors.append(f"{lid}: duplicate task ids")
        if tasks and not any(t.get("difficulty", 2) < 3 for t in tasks):
            errors.append(f"{lid}: every task has difficulty 3; Leicht/Normal would play nothing")
        for t in tasks:
            check_task(f"{lid}/{t.get('id')}", t, errors)
    if is_world:
        check_world(path, p, levels, courses, errors)
    return errors


failed = False
for path in sys.argv[1:]:
    try:
        errs = check(path)
    except Exception as e:
        errs = [f"{type(e).__name__}: {e}"]
    for e in errs:
        print(f"✗ {path}: {e}")
    if errs:
        failed = True
    else:
        print(f"✓ {path}")
sys.exit(1 if failed else 0)
