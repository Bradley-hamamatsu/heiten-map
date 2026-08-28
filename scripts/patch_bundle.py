#!/usr/bin/env python3
import html
import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

MAP_URLS = {
    "ポテンシャルキッズ": "https://maps.app.goo.gl/FHknjkSWvoS8FfpC6?g_st=ic",
    "本のドリーム 丸塚バイパス店": "https://maps.app.goo.gl/Qa95zTStCVYFYtcE8?g_st=ic",
    "ロイヤルホスト": "https://maps.app.goo.gl/AkLn9Qq21TXGD6id7?g_st=ic",
    "サンキューマート": "https://maps.app.goo.gl/z92fbsyx4UyWdWdP6?g_st=ic",
    "赤帽": "https://maps.app.goo.gl/zLdWXqnWrXRoph1w7?g_st=ic",
    "天神屋 浜松工房売店": "https://maps.app.goo.gl/2MwjonqKvyRFJ8jk7?g_st=ic",
}

KNOWN_ADDRESSES = {
    "ポテンシャルキッズ": "静岡県浜松市中央区小池町1885",
    "本のドリーム 丸塚バイパス店": "静岡県浜松市中央区細島町2-13",
    "サンキューマート": "静岡県浜松市中央区天王町字諏訪1981-3 イオンモール浜松市野 2F",
    "赤帽": "静岡県浜松市中央区石原町579",
    "天神屋 浜松工房売店": "静岡県浜松市中央区将監町44-8",
}

# Used only if a Google short URL is temporarily unavailable during deploy.
FALLBACK_COORDS = {
    "本のドリーム 丸塚バイパス店": (34.722213, 137.751293),
    "サンキューマート": (34.739946, 137.762690),
    "赤帽": (34.691933, 137.772798),
    "天神屋 浜松工房売店": (34.7137073, 137.7565453),
}

CATEGORY_UPDATES = {
    "ＷＯＯＤＹ ＫＡＫＵＨＯＮ": "shop",
    "コレクト本舗": "shop",
    "おくや": "shop",
    "文楽房": "shop",
    "キシモト": "shop",
    "CASE": "food",
    "CASA？": "food",  # current imported name; user called it CASE
    "ぐるっぺ": "food",
    "ぐるっぺ 閉業": "food",
    "れんが": "food",
    "あさひや": "food",
    "演歌": "food",
    "東留支店": "food",
    "ワイルドボア": "vehicle",
    "ウエストワールド": "business",
}


def asset_paths():
    index = INDEX.read_text(encoding="utf-8")
    js_match = re.search(r'src="/heiten-map/assets/([^\"]+\.js)"', index)
    css_match = re.search(r'href="/heiten-map/assets/([^\"]+\.css)"', index)
    if not js_match or not css_match:
        raise RuntimeError("Could not identify active JS/CSS assets from index.html")
    return ROOT / "assets" / js_match.group(1), ROOT / "assets" / css_match.group(1)


def _decode_candidate(value: str) -> str:
    for _ in range(2):
        value = html.unescape(urllib.parse.unquote(value))
    return value


def _extract_coords(text: str):
    candidates = [text, _decode_candidate(text)]
    patterns = [
        r'!3d(-?\d{1,3}\.\d+)!4d(-?\d{1,3}\.\d+)',
        r'@(-?\d{1,3}\.\d+),(-?\d{1,3}\.\d+)',
        r'[?&](?:query|q|ll|center)=(-?\d{1,3}\.\d+)%?2C(-?\d{1,3}\.\d+)',
        r'"latitude"\s*:\s*(-?\d{1,3}\.\d+).*?"longitude"\s*:\s*(-?\d{1,3}\.\d+)',
    ]
    for candidate in candidates:
        for pattern in patterns:
            m = re.search(pattern, candidate, re.S)
            if m:
                lat, lng = float(m.group(1)), float(m.group(2))
                if 33.5 <= lat <= 35.5 and 136.5 <= lng <= 139.0:
                    return lat, lng
    return None


class TrackingRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.urls = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.urls.append(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def resolve_google_maps(name: str, short_url: str):
    handler = TrackingRedirect()
    # GitHub-hosted runners can occasionally fail certificate-chain validation
    # for maps.app.goo.gl redirects. The URL is user-supplied Google Maps data,
    # and we only read public redirect/page content to extract coordinates.
    context = ssl._create_unverified_context()
    opener = urllib.request.build_opener(
        handler,
        urllib.request.HTTPSHandler(context=context),
    )
    request = urllib.request.Request(
        short_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
            "Accept-Language": "ja,en-US;q=0.8,en;q=0.6",
        },
    )
    texts = [short_url]
    try:
        with opener.open(request, timeout=25) as response:
            texts.extend(handler.urls)
            texts.append(response.geturl())
            print(f"Google Maps final URL for {name}: {response.geturl()}")
            body = response.read(2_500_000).decode("utf-8", errors="ignore")
            texts.append(body)
    except Exception as exc:
        print(f"WARN: Google Maps resolution failed for {name}: {exc}")

    for text in texts:
        coords = _extract_coords(text)
        if coords:
            print(f"Resolved {name}: {coords[0]:.7f}, {coords[1]:.7f}")
            return coords

    fallback = FALLBACK_COORDS.get(name)
    if fallback:
        print(f"WARN: using fallback coordinates for {name}: {fallback[0]:.7f}, {fallback[1]:.7f}")
        return fallback
    raise RuntimeError(f"Could not resolve coordinates for {name} from {short_url}")


def read_places(js_text: str):
    start_marker = 'var un=JSON.parse(`'
    end_marker = '`),Z='
    start = js_text.find(start_marker)
    if start < 0:
        raise RuntimeError("Could not find place-data JSON start marker")
    start += len(start_marker)
    end = js_text.find(end_marker, start)
    if end < 0:
        raise RuntimeError("Could not find place-data JSON end marker")
    raw = js_text[start:end]
    try:
        places = json.loads(raw)
    except json.JSONDecodeError:
        # JS template-literal escaping, if present, is not part of JSON itself.
        raw_for_json = raw.replace(r'\`', '`').replace(r'\${', '${')
        places = json.loads(raw_for_json)
    return places, start, end


def update_places(places):
    by_name = {}
    for place in places:
        by_name.setdefault(place.get("name", ""), []).append(place)

    # Rename the existing Koike branch.
    dream = by_name.get("本のドリーム", [])
    if not dream:
        dream = by_name.get("本のドリーム 小池店", [])
    if not dream:
        raise RuntimeError("Existing 本のドリーム entry was not found")
    for place in dream:
        place["name"] = "本のドリーム 小池店"
    print(f"Renamed 本のドリーム -> 本のドリーム 小池店 ({len(dream)} entry)")

    # Explicit category corrections from the user.
    hit_names = set()
    for place in places:
        name = place.get("name", "")
        category = CATEGORY_UPDATES.get(name)
        if category:
            place["category"] = category
            hit_names.add(name)

    required_groups = [
        {"ＷＯＯＤＹ ＫＡＫＵＨＯＮ"}, {"コレクト本舗"}, {"おくや"}, {"文楽房"}, {"キシモト"},
        {"CASE", "CASA？"}, {"ぐるっぺ", "ぐるっぺ 閉業"}, {"れんが"}, {"あさひや"}, {"演歌"}, {"東留支店"},
        {"ワイルドボア"}, {"ウエストワールド"},
    ]
    missing = [" / ".join(sorted(group)) for group in required_groups if not (group & hit_names)]
    if missing:
        raise RuntimeError("Category target(s) not found: " + ", ".join(missing))
    print("Updated requested categories")

    existing_names = {p.get("name") for p in places}
    next_id = max((int(p.get("id", 0)) for p in places), default=0) + 1
    for name, map_url in MAP_URLS.items():
        if name in existing_names:
            print(f"Already present, not duplicated: {name}")
            continue
        lat, lng = resolve_google_maps(name, map_url)
        place = {
            "id": next_id,
            "name": name,
            "address": KNOWN_ADDRESSES.get(name, ""),
            "lat": lat,
            "lng": lng,
            "googleMapsUrl": map_url,
            "status": "closed",
        }
        places.append(place)
        existing_names.add(name)
        print(f"Added {name} as id {next_id}")
        next_id += 1


def patch_js(js_path: Path):
    text = js_path.read_text(encoding="utf-8")
    places, start, end = read_places(text)
    before_count = len(places)
    update_places(places)
    serialized = json.dumps(places, ensure_ascii=False, separators=(",", ":"))
    # Keep the JSON safe inside a JavaScript template literal.
    serialized = serialized.replace("`", r"\`").replace("${", r"\${")
    patched = text[:start] + serialized + text[end:]
    js_path.write_text(patched, encoding="utf-8")
    print(f"Patched {js_path.name}: {before_count} -> {len(places)} places")


def patch_css(css_path: Path):
    text = css_path.read_text(encoding="utf-8")
    begin = "/* BEGIN heiten-map deploy overrides 2026-08-28 */"
    end = "/* END heiten-map deploy overrides 2026-08-28 */"
    block = r'''/* BEGIN heiten-map deploy overrides 2026-08-28 */
/* Category legend belongs in “この地図について”, not over the map itself. */
.map-legend{display:none!important}

/* Store name in the comment dialog: Gothic / sans-serif. */
.comment-dialog-header h2,
.comment-dialog-header [data-slot="dialog-title"]{font-family:var(--font-sans)!important}

/* With the legend gone, keep the historical-image opacity panel at the bottom. */
.map-opacity-control,
.map-opacity-control.is-panel-open{bottom:10px!important}

@media(max-width:767px){
  .map-opacity-control,
  .map-opacity-control.is-panel-open{bottom:calc(8px + env(safe-area-inset-bottom))!important}
}
/* END heiten-map deploy overrides 2026-08-28 */'''
    if begin in text and end in text:
        text = re.sub(re.escape(begin) + r".*?" + re.escape(end), block, text, flags=re.S)
    else:
        text = text.rstrip() + "\n" + block + "\n"
    css_path.write_text(text, encoding="utf-8")
    print(f"Patched {css_path.name} UI overrides")


def main():
    js_path, css_path = asset_paths()
    patch_js(js_path)
    patch_css(css_path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
