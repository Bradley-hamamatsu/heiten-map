#!/usr/bin/env python3
"""Align the public/admin editing workflows in the deployed static bundles.

The repository contains build output only, so these changes are applied as
small, asserted replacements.  Every replacement must match exactly once;
otherwise the script stops instead of silently corrupting a bundle.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260904-direct-dashboard"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"Expected one match in {path.relative_to(ROOT)}, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return
    path.write_text(text.rstrip() + "\n" + block.strip() + "\n", encoding="utf-8")


def patch_location_maps() -> None:
    path = ROOT / "assets" / "map-experience-admin-2013d629c5.js"
    old = (
        "var dn={gsi:{label:`地理院地図`,url:`https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png`,"
        "maxZoom:18,subdomains:void 0,attribution:`地理院タイル`},google:{label:`Google標準`,"
        "url:`https://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}`,maxZoom:20,"
        "subdomains:[`mt0`,`mt1`,`mt2`,`mt3`],attribution:`© Google`},aerial:{label:`航空写真`,"
        "url:`https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}`,maxZoom:20,"
        "subdomains:[`mt0`,`mt1`,`mt2`,`mt3`],attribution:`© Google`},hybrid:{label:`航空写真＋道路`,"
        "url:`https://{s}.google.com/vt/lyrs=y&x={x}&y={y}&z={z}`,maxZoom:20,"
        "subdomains:[`mt0`,`mt1`,`mt2`,`mt3`],attribution:`© Google`}};"
    )
    new = (
        "var dn={gsi:{label:`地理院地図`,url:`https://cyberjapandata.gsi.go.jp/xyz/std/{z}/{x}/{y}.png`,"
        "maxZoom:18,subdomains:void 0,attribution:`地理院タイル`},aerial:{label:`地理院航空写真`,"
        "url:`https://cyberjapandata.gsi.go.jp/xyz/seamlessphoto/{z}/{x}/{y}.jpg`,maxZoom:18,"
        "subdomains:void 0,attribution:`地理院タイル`}};"
    )
    replace_once(path, old, new)


def patch_public_entry() -> None:
    path = ROOT / "assets" / "map-Cjgx8Hw7.js"
    replace_once(
        path,
        'from"./map-experience-Ch2l2pu3.js"',
        f'from"./map-experience-admin-2013d629c5.js?v={VERSION}"',
    )

    path = ROOT / "index.html"
    replace_once(
        path,
        '<script type="module" crossorigin src="/heiten-map/assets/map-I2eqy3_5.js"></script>',
        f'<script type="module" crossorigin src="/heiten-map/assets/map-Cjgx8Hw7.js?v={VERSION}"></script>',
    )
    replace_once(
        path,
        '<link rel="modulepreload" crossorigin href="/heiten-map/assets/ui-CWbszX17.js">',
        '<link rel="modulepreload" crossorigin href="/heiten-map/assets/ui-BD2vJvMe.js">',
    )
    replace_once(
        path,
        '<link rel="modulepreload" crossorigin href="/heiten-map/assets/preload-helper-D5JbzDgk.js">',
        f'<link rel="modulepreload" crossorigin href="/heiten-map/assets/map-experience-admin-2013d629c5.js?v={VERSION}">',
    )
    replace_once(
        path,
        '<link rel="stylesheet" crossorigin href="/heiten-map/assets/preload-helper-MbmbZ9XP.css">',
        f'<link rel="stylesheet" crossorigin href="/heiten-map/assets/map-experience-B04n2wOs.css?v={VERSION}">',
    )


def patch_admin_dashboard() -> None:
    path = ROOT / "assets" / "admin-map-42fb4b0090.js"
    replace_once(
        path,
        'from"./map-experience-admin-2013d629c5.js"',
        f'from"./map-experience-admin-2013d629c5.js?v={VERSION}"',
    )
    replace_once(path, "管理者用の地図を開く", "管理メニューを開く")
    old_router = (
        "function He(){let[e,t]=(0,R.useState)(`map`),[n,r]=(0,R.useState)(null);"
        "return e===`login`?(0,z.jsx)(X,{loginOnly:!0,onAuthenticated:()=>t(`map`)}):"
        "e===`dashboard`?(0,z.jsx)(X,{initialStoreId:n,onLogout:()=>{r(null),t(`map`)},"
        "onBackToMap:()=>{r(null),t(`map`)}}):(0,z.jsx)(_,{adminMode:!0,onOpenAdmin:()=>{r(null),"
        "t(`dashboard`)},onEditAdminStore:e=>{r(e),t(`dashboard`)},onAddAdminStore:()=>{r(`new`),"
        "t(`dashboard`)}})}"
    )
    replace_once(path, old_router, "function He(){return(0,z.jsx)(X,{})}")

    path = ROOT / "admin" / "dashboard" / "index.html"
    replace_once(
        path,
        '<script type="module" crossorigin src="/heiten-map/assets/admin-map-42fb4b0090.js"></script>',
        f'<script type="module" crossorigin src="/heiten-map/assets/admin-map-42fb4b0090.js?v={VERSION}"></script>',
    )
    replace_once(
        path,
        '<link rel="modulepreload" crossorigin href="/heiten-map/assets/map-experience-admin-2013d629c5.js">',
        f'<link rel="modulepreload" crossorigin href="/heiten-map/assets/map-experience-admin-2013d629c5.js?v={VERSION}">',
    )
    replace_once(
        path,
        '<link rel="stylesheet" crossorigin href="/heiten-map/assets/map-experience-B04n2wOs.css">',
        f'<link rel="stylesheet" crossorigin href="/heiten-map/assets/map-experience-B04n2wOs.css?v={VERSION}">',
    )

    css = ROOT / "assets" / "map-experience-B04n2wOs.css"
    append_once(
        css,
        "BEGIN direct-admin-dashboard overrides 2026-09-04",
        """
/* BEGIN direct-admin-dashboard overrides 2026-09-04 */
/* The retired administrator-map screen is no longer a navigation target. */
.admin-header-actions > :first-child{display:none!important}
/* END direct-admin-dashboard overrides 2026-09-04 */
""",
    )


def patch_legacy_admin_login() -> None:
    path = ROOT / "admin" / "index.html"
    replace_once(path, ">管理者用の地図を開く</button>", ">管理メニューを開く</button>")
    old_success = """    data=await apiGet(candidate);
    key=candidate;
    sessionStorage.setItem(KEY_NAME,key);
    show($(\"loginView\"),false);
    show($(\"mapView\"),true);
    await initMainMap();
    renderMarkers();
    updateStatus();"""
    new_success = """    await apiGet(candidate);
    key=candidate;
    sessionStorage.setItem(KEY_NAME,key);
    location.replace(\"./dashboard/\");"""
    replace_once(path, old_success, new_success)
    replace_once(
        path,
        '$("loginButton").textContent="管理者用の地図を開く"',
        '$("loginButton").textContent="管理メニューを開く"',
    )


def main() -> None:
    patch_location_maps()
    patch_public_entry()
    patch_admin_dashboard()
    patch_legacy_admin_login()
    print("Patched public/admin workflows and GSI-only location maps")


if __name__ == "__main__":
    main()
