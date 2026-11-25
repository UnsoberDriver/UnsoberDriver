#!/usr/bin/env python3
"""Regenerate the profile pin cards as local SVGs with a 1px white border."""

from __future__ import annotations

import pathlib
import re
import urllib.request

REPOS = ["Portfolio", "NexusHub", "Home-Kitchen-Club", "NoteKeep", "DropZone"]
OUT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "cards"
BASE = "https://github-readme-stats.vercel.app/api/pin/"


def fetch(repo: str) -> str:
    url = (
        f"{BASE}?username=UnsoberDriver&repo={repo}"
        "&theme=dark&border_radius=10&bg_color=ffffff00&border_color=ffffff"
        "&cache_seconds=86400"
    )
    request = urllib.request.Request(url, headers={"User-Agent": "profile-cards-update"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def thicken_border(svg: str) -> str:
    viewbox = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    if not viewbox:
        raise ValueError("missing viewBox")
    width, height = int(viewbox.group(1)), int(viewbox.group(2))

    pattern = r'(<rect\s+data-testid="card-bg"\s+)[^>]*?(/?>)'
    replacement = (
        r"\1"
        f'x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="10"'
        ' stroke-width="1" stroke="#ffffff" stroke-opacity="0.75"'
        r"\2"
    )
    patched, count = re.subn(pattern, replacement, svg, count=1)
    if count != 1:
        raise ValueError("card-bg rect not found")
    return patched


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for repo in REPOS:
        svg = thicken_border(fetch(repo))
        (OUT_DIR / f"{repo}.svg").write_text(svg, encoding="utf-8")
        print(f"updated {repo}.svg")


if __name__ == "__main__":
    main()
