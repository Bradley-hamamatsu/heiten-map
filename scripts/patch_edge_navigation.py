#!/usr/bin/env python3
"""Disable accidental browser back/forward edge swipes on the public map."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260905-edge-swipe-guard"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"Expected one match in {path.relative_to(ROOT)}, found {count}"
        )
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n" + block.strip() + "\n", encoding="utf-8")


def patch_public_html() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    if '<body class="public-map-page">' not in text:
        if text.count("<body>") != 1:
            raise RuntimeError("Expected one public body element")
        text = text.replace("<body>", '<body class="public-map-page">', 1)
    old_version = "20260905-map-first-review-diff-2"
    if VERSION not in text:
        if text.count(old_version) < 2:
            raise RuntimeError("Expected public asset cache keys were not found")
        text = text.replace(old_version, VERSION)
    path.write_text(text, encoding="utf-8")


def patch_public_entry() -> None:
    path = ROOT / "assets" / "map-Cjgx8Hw7.js"
    append_once(
        path,
        "installEdgeSwipeGuard",
        r'''
function installEdgeSwipeGuard(){let start=null,edgeWidth=32;document.addEventListener(`touchstart`,event=>{if(event.touches.length!==1){start=null;return}let touch=event.touches[0],side=touch.clientX<=edgeWidth?`left`:touch.clientX>=window.innerWidth-edgeWidth?`right`:null;start=side?{x:touch.clientX,y:touch.clientY,side}:null},{passive:!0,capture:!0});document.addEventListener(`touchmove`,event=>{if(!start||event.touches.length!==1)return;let touch=event.touches[0],dx=touch.clientX-start.x,dy=touch.clientY-start.y,inward=start.side===`left`&&dx>0||start.side===`right`&&dx<0;if(inward&&Math.abs(dx)>8&&Math.abs(dx)>Math.abs(dy)*1.1)event.preventDefault()},{passive:!1,capture:!0});let reset=()=>{start=null};document.addEventListener(`touchend`,reset,{passive:!0,capture:!0}),document.addEventListener(`touchcancel`,reset,{passive:!0,capture:!0})}installEdgeSwipeGuard();
''',
    )
    text = path.read_text(encoding="utf-8")
    old_version = "20260905-map-first-review-diff-2"
    if VERSION not in text:
        if text.count(old_version) != 1:
            raise RuntimeError("Expected public entry cache key was not found")
        path.write_text(text.replace(old_version, VERSION, 1), encoding="utf-8")


def patch_public_styles() -> None:
    path = ROOT / "assets" / "map-experience-B04n2wOs.css"
    append_once(
        path,
        "BEGIN public edge-swipe guard 2026-09-05",
        r'''
/* BEGIN public edge-swipe guard 2026-09-05 */
body.public-map-page,
body.public-map-page #root,
body.public-map-page .map-shell{
  overscroll-behavior-x:none;
  overscroll-behavior-inline:none;
}
/* END public edge-swipe guard 2026-09-05 */
''',
    )


def main() -> None:
    patch_public_html()
    patch_public_entry()
    patch_public_styles()
    print("Patched public edge-swipe navigation guard")


if __name__ == "__main__":
    main()
