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
IMAGES = ROOT / "assets" / "images.css"
OUT = ROOT / "index.html"
MARKER = "/*IMAGES*/"

page = PAGE.read_text(encoding="utf-8")
if MARKER not in page:
    sys.exit("marker %s missing from %s" % (MARKER, PAGE))

available = dict(
    re.findall(r"(--[a-z0-9-]+):\s*(url\(data:image/[a-z]+;base64,[A-Za-z0-9+/=]+\));",
               IMAGES.read_text(encoding="utf-8"))
)

used = sorted({m for m in re.findall(r"var\((--[a-z0-9-]+)\)", page) if m in available})
missing = sorted({m for m in re.findall(r"var\((--(?:img|city|gal|av|fri)-[a-z0-9-]+)\)", page)} - set(available))
if missing:
    sys.exit("page references images not in assets/images.css: " + ", ".join(missing))

block = ":root{" + "".join("%s:%s;" % (k, available[k]) for k in used) + "}"
OUT.write_text(page.replace(MARKER, block), encoding="utf-8")

unused = sorted(set(available) - set(used))
print("embedded %d images (%d skipped as unused)" % (len(used), len(unused)))
print("wrote %s (%.1f MB)" % (OUT.name, OUT.stat().st_size / 1e6))
