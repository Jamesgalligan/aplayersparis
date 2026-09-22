#!/usr/bin/env python3
"""Inline the photography into src/page.html and write a standalone index.html.

Only the image custom properties actually referenced by the page are
embedded, so unused photos never reach the shipped file.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
PAGE = ROOT / "src" / "page.html"
IMAGE_FILES = [ROOT / "assets" / "images.css", ROOT / "assets" / "people.css"]
OUT = ROOT / "index.html"
MARKER = "/*IMAGES*/"
LIB_MARKER = "/*LIBPHONENUMBER*/"
LIB = ROOT / "vendor" / "libphonenumber-max.js"

page = PAGE.read_text(encoding="utf-8")
if MARKER not in page:
    sys.exit("marker %s missing from %s" % (MARKER, PAGE))

available = {}
for f in IMAGE_FILES:
    if f.exists():
        available.update(
            re.findall(r"(--[a-z0-9-]+):\s*(url\(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+\));",
                       f.read_text(encoding="utf-8"))
        )

used = sorted({m for m in re.findall(r"var\((--[a-z0-9-]+)\)", page) if m in available})
missing = sorted({m for m in re.findall(r"var\((--(?:img|city|gal|av|fri|p)-[a-z0-9-]+)\)", page)} - set(available))
if missing:
    sys.exit("page references images not found in assets/: " + ", ".join(missing))

block = ":root{" + "".join("%s:%s;" % (k, available[k]) for k in used) + "}"
out = page.replace(MARKER, block)

if LIB_MARKER in out:
    if not LIB.exists():
        sys.exit("missing %s" % LIB)
    out = out.replace(LIB_MARKER, LIB.read_text(encoding="utf-8"))
    print("inlined libphonenumber (%.0f KB)" % (LIB.stat().st_size / 1024))

OUT.write_text(out, encoding="utf-8")

unused = sorted(set(available) - set(used))
print("embedded %d images (%d skipped as unused)" % (len(used), len(unused)))
print("wrote %s (%.1f MB)" % (OUT.name, OUT.stat().st_size / 1e6))
