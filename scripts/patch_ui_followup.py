#!/usr/bin/env python3
"""Apply the 2026-09-05 map-first/admin-review follow-up to built assets.

This repository contains compiled output only.  Each replacement is asserted
so an unexpected bundle change fails loudly instead of damaging the site.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "20260905-map-first-review-diff-2"


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


def patch_source_labels() -> None:
    bundle = ROOT / "assets" / "map-experience-admin-2013d629c5.js"
    old = """var Yt=[`現地で確認`,`Googleストリートビュー`,`Googleマップ`,`航空写真・古地図`,`チラシ・広告`,`公式サイト・公式SNS`,`その他のウェブサイト・SNS`,`新聞・雑誌・書籍`,`自分の記憶`,`家族・知人から聞いた`,`その他`];function Xt(e){return typeof e==`string`&&Yt.includes(e)}function Zt(e){return[...new Set(e.filter(Xt))].join(`＋`)}function Qt(e){return e?[...new Set(e.split(/[＋+、,]/).map(e=>e.trim()).filter(Xt))]:[]}"""
    new = """var Yt=[`現地で確認`,`Googleストリートビュー`,`Googleマップ`,`航空写真・古地図`,`チラシ・広告・看板`,`公式サイト・公式SNS`,`その他のウェブサイト・SNS`,`新聞・雑誌・書籍`,`自分の記憶`,`家族・知人などから聞いた`,`その他`];function sourceChoiceNormalize(e){return e===`チラシ・広告`?`チラシ・広告・看板`:e===`家族・知人から聞いた`?`家族・知人などから聞いた`:e}function Xt(e){return typeof e==`string`&&Yt.includes(e)}function Zt(e){return[...new Set(e.map(sourceChoiceNormalize).filter(Xt))].join(`＋`)}function Qt(e){return e?[...new Set(e.split(/[＋+、,]/).map(e=>sourceChoiceNormalize(e.trim())).filter(Xt))]:[]}"""
    replace_once(bundle, old, new)

    legacy = ROOT / "admin" / "index.html"
    replace_once(legacy, '"チラシ・広告"', '"チラシ・広告・看板"')
    replace_once(legacy, '"家族・知人から聞いた"', '"家族・知人などから聞いた"')


def patch_embedded_public_location_picker() -> None:
    bundle = ROOT / "assets" / "map-experience-admin-2013d629c5.js"
    component = r'''function PublicLocationPicker({lat:locationLat,lng:locationLng,onChange:onLocationChange,disabled:isDisabled=!1}){let containerRef=(0,A.useRef)(null),mapRef=(0,A.useRef)(null),leafletRef=(0,A.useRef)(null),tileRef=(0,A.useRef)(null),latestLocation=(0,A.useRef)({lat:locationLat,lng:locationLng}),[mapStyle,setMapStyle]=(0,A.useState)(`gsi`),[center,setCenter]=(0,A.useState)(locationLat!==null&&locationLng!==null?{lat:Number(locationLat),lng:Number(locationLng)}:null);return(0,A.useEffect)(()=>{let cancelled=!1,cleanupGestures=()=>void 0;async function initialize(){if(!containerRef.current||mapRef.current)return;let leaflet=await _n(()=>import(`./leaflet-1-_l5dQP.js`).then(t=>e(t.t(),1)),__vite__mapDeps([0,1]));if(cancelled||!containerRef.current)return;leafletRef.current=leaflet;let hasLocation=latestLocation.current.lat!==null&&latestLocation.current.lng!==null,initialCenter=hasLocation?[Number(latestLocation.current.lat),Number(latestLocation.current.lng)]:[34.7358,137.7604],map=leaflet.map(containerRef.current,{zoomControl:!0,attributionControl:!0,minZoom:8,maxZoom:18,doubleClickZoom:!1}).setView(initialCenter,hasLocation?17:13),base=dn.gsi;tileRef.current=leaflet.tileLayer(base.url,{maxZoom:base.maxZoom,maxNativeZoom:base.maxZoom,subdomains:base.subdomains,attribution:base.attribution,crossOrigin:!0}).addTo(map);let updateCenter=()=>{let value=map.getCenter();setCenter({lat:value.lat,lng:value.lng})};map.on(`moveend`,updateCenter),mapRef.current=map,cleanupGestures=fn(map),updateCenter(),window.setTimeout(()=>map.invalidateSize(),60),window.setTimeout(()=>map.invalidateSize(),240)}return initialize(),()=>{cancelled=!0,cleanupGestures(),mapRef.current?.remove(),mapRef.current=null,leafletRef.current=null,tileRef.current=null}},[]),(0,A.useEffect)(()=>{let map=mapRef.current,leaflet=leafletRef.current;if(!map||!leaflet)return;let base=dn[mapStyle];tileRef.current?.remove(),tileRef.current=leaflet.tileLayer(base.url,{maxZoom:base.maxZoom,maxNativeZoom:base.maxZoom,subdomains:base.subdomains,attribution:base.attribution,crossOrigin:!0}).addTo(map),tileRef.current.bringToBack()},[mapStyle]),(0,A.useEffect)(()=>{latestLocation.current={lat:locationLat,lng:locationLng};let map=mapRef.current;if(!map||locationLat===null||locationLng===null)return;let current=map.getCenter(),lat=Number(locationLat),lng=Number(locationLng);Math.abs(current.lat-lat)<1e-7&&Math.abs(current.lng-lng)<1e-7||(setCenter({lat,lng}),map.setView([lat,lng],Math.max(16,map.getZoom()),{animate:!1}))},[locationLat,locationLng]),(0,Y.jsxs)(`div`,{className:`public-location-picker admin-location-picker`,children:[(0,Y.jsxs)(`div`,{className:`admin-location-toolbar`,children:[(0,Y.jsxs)(`label`,{children:[(0,Y.jsx)(`span`,{children:`位置指定用の地図`}),(0,Y.jsx)(It,{value:mapStyle,onChange:event=>setMapStyle(event.target.value),disabled:isDisabled,children:Object.entries(dn).map(([key,value])=>(0,Y.jsx)(Lt,{value:key,children:value.label},key))})]}),(0,Y.jsx)(`small`,{className:`location-operation-note`,children:`PCはドラッグ・ホイール、スマホは2本指で移動・拡大縮小します。`})]}),(0,Y.jsxs)(`div`,{className:`admin-location-map`,children:[(0,Y.jsx)(`div`,{ref:containerRef,"aria-label":`店舗の場所を合わせる地図`}),(0,Y.jsx)(`div`,{className:`admin-location-crosshair`,"aria-hidden":`true`,children:(0,Y.jsx)(`span`,{})})]}),(0,Y.jsxs)(`div`,{className:`admin-location-footer`,children:[(0,Y.jsxs)(`div`,{children:[(0,Y.jsx)(`strong`,{children:`十字線の交点を店舗の場所に合わせます`}),(0,Y.jsx)(`span`,{children:center?`現在の中心：${center.lat.toFixed(6)}, ${center.lng.toFixed(6)}`:`地図を動かして位置を合わせてください`})]}),(0,Y.jsxs)(X,{type:`button`,size:`sm`,disabled:isDisabled||!center,onClick:()=>center&&onLocationChange(center),children:[(0,Y.jsx)(t,{"aria-hidden":`true`}),` この位置を入力`]})]})]})}'''
    replace_once(bundle, "function sn(", component + "function sn(")

    old_location = r'''(0,Y.jsxs)(`div`,{className:`location-picker-card`,children:[(0,Y.jsxs)(`div`,{children:[(0,Y.jsxs)(`span`,{children:[`地図上の場所 `,(0,Y.jsx)(`b`,{children:`必須`})]}),(0,Y.jsx)(`strong`,{children:a.locationChosen&&a.lat!==null&&a.lng!==null?`場所を選択済み`:`まだ選ばれていません`}),(0,Y.jsx)(`small`,{children:`地図を動かして、中央の十字線を店舗の位置に合わせます`})]}),(0,Y.jsxs)(X,{type:`button`,variant:`outline`,size:`sm`,onClick:s,disabled:l,children:[(0,Y.jsx)(ee,{"aria-hidden":`true`}),a.locationChosen?`場所を合わせ直す`:`地図で場所を合わせる`]})]}),(0,Y.jsxs)(`div`,{className:`contribution-grid location-coordinate-grid`,children:[(0,Y.jsxs)(`label`,{children:[(0,Y.jsx)(`span`,{children:`緯度（自動入力）`}),(0,Y.jsx)(Z,{value:a.lat===null?``:a.lat.toFixed(7),readOnly:!0,tabIndex:-1,placeholder:`地図で場所を合わせると入力されます`})]}),(0,Y.jsxs)(`label`,{children:[(0,Y.jsx)(`span`,{children:`経度（自動入力）`}),(0,Y.jsx)(Z,{value:a.lng===null?``:a.lng.toFixed(7),readOnly:!0,tabIndex:-1,placeholder:`地図で場所を合わせると入力されます`})]})]})'''
    new_location = r'''(0,Y.jsx)(PublicLocationPicker,{lat:a.lat,lng:a.lng,disabled:l,onChange:({lat:e,lng:t})=>o(n=>({...n,lat:e,lng:t,locationChosen:!0}))}),(0,Y.jsxs)(`div`,{className:`contribution-grid location-coordinate-grid`,children:[(0,Y.jsxs)(`label`,{children:[(0,Y.jsx)(`span`,{children:`緯度（自動入力）`}),(0,Y.jsx)(Z,{value:a.lat===null?``:a.lat.toFixed(7),readOnly:!0,tabIndex:-1,placeholder:`地図の「この位置を入力」で反映されます`})]}),(0,Y.jsxs)(`label`,{children:[(0,Y.jsx)(`span`,{children:`経度（自動入力）`}),(0,Y.jsx)(Z,{value:a.lng===null?``:a.lng.toFixed(7),readOnly:!0,tabIndex:-1,placeholder:`地図の「この位置を入力」で反映されます`})]})]})'''
    replace_once(bundle, old_location, new_location)


def patch_public_editor_attribution() -> None:
    bundle = ROOT / "assets" / "map-experience-admin-2013d629c5.js"
    old_merge = r'''U=(0,A.useMemo)(()=>[...vn,...Pe].flatMap(e=>{let t=Me[e.id];if(t?.isDeleted)return[];if(!t)return[e];let n=t.category&&t.category in Q?t.category:e.category,r=t.secondaryCategory===null?e.secondaryCategory:t.secondaryCategory||void 0,i=r&&r!==n&&r in Q?r:void 0;return[{...e,name:t.name??e.name,category:n,secondaryCategory:i,status:t.status??e.status,address:t.address===null?e.address:t.address,lat:t.lat??e.lat,lng:t.lng??e.lng,googleMapsUrl:t.googleMapsUrl===null?e.googleMapsUrl:t.googleMapsUrl||`https://www.google.com/maps/search/?api=1&query=${t.lat??e.lat},${t.lng??e.lng}`,openedYear:t.openedYear===null?e.openedYear:t.openedYear||void 0,closedYear:t.closedYear===null?e.closedYear:t.closedYear||void 0,nextStore:t.nextStore===null?e.nextStore:t.nextStore||void 0,note:t.note===null?e.note:t.note||void 0,source:t.source===null?e.source:t.source||void 0}]}),[Pe,Me])'''
    new_merge = r'''U=(0,A.useMemo)(()=>[...vn,...Pe].flatMap(e=>{let t=Me[e.id],historyEntry=Re.find(t=>t.storeId===e.id),contributor={contributorName:historyEntry?.contributorName??e.contributorName,contributorRole:historyEntry?.contributorRole??e.contributorRole,contributorAction:historyEntry?.action??e.contributorAction??`add`};if(t?.isDeleted)return[];if(!t)return[{...e,...contributor}];let n=t.category&&t.category in Q?t.category:e.category,r=t.secondaryCategory===null?e.secondaryCategory:t.secondaryCategory||void 0,i=r&&r!==n&&r in Q?r:void 0;return[{...e,...contributor,name:t.name??e.name,category:n,secondaryCategory:i,status:t.status??e.status,address:t.address===null?e.address:t.address,lat:t.lat??e.lat,lng:t.lng??e.lng,googleMapsUrl:t.googleMapsUrl===null?e.googleMapsUrl:t.googleMapsUrl||`https://www.google.com/maps/search/?api=1&query=${t.lat??e.lat},${t.lng??e.lng}`,openedYear:t.openedYear===null?e.openedYear:t.openedYear||void 0,closedYear:t.closedYear===null?e.closedYear:t.closedYear||void 0,nextStore:t.nextStore===null?e.nextStore:t.nextStore||void 0,note:t.note===null?e.note:t.note||void 0,source:t.source===null?e.source:t.source||void 0}]}),[Pe,Me,Re])'''
    replace_once(bundle, old_merge, new_merge)

    old_history_effect = r'''(0,A.useEffect)(()=>{if(!Ie)return;let e=new AbortController;return fetch(`${Cn}/api/history?limit=50`,{cache:`no-store`,signal:e.signal}).then(async e=>{if(!e.ok)throw Error(await On(e,`追加・編集履歴を読み込めませんでした`));return e.json()}).then(({history:e})=>ze(e)).catch(e=>{e instanceof DOMException&&e.name===`AbortError`||Ue(e instanceof Error?e.message:`追加・編集履歴を読み込めませんでした`)}).finally(()=>{e.signal.aborted||Ve(!1)}),()=>e.abort()},[Ie])'''
    new_history_effect = r'''(0,A.useEffect)(()=>{let e=new AbortController;return Ve(!0),fetch(`${Cn}/api/history?limit=300`,{cache:`no-store`,signal:e.signal}).then(async e=>{if(!e.ok)throw Error(await On(e,`追加・編集履歴を読み込めませんでした`));return e.json()}).then(({history:e})=>ze(e)).catch(e=>{e instanceof DOMException&&e.name===`AbortError`||Ue(e instanceof Error?e.message:`追加・編集履歴を読み込めませんでした`)}).finally(()=>{e.signal.aborted||Ve(!1)}),()=>e.abort()},[Ie])'''
    replace_once(bundle, old_history_effect, new_history_effect)

    replace_once(
        bundle,
        'children:W.contributorRole===`viewer`?`閲覧者による追加`:`サイト作成者による追加`',
        'children:W.contributorRole===`viewer`?W.contributorAction===`edit`?`閲覧者が編集`:`閲覧者による追加`:W.contributorAction===`edit`?`サイト作成者が編集`:`サイト作成者による追加`',
    )
    replace_once(
        bundle,
        'children:e.contributorRole===`creator`?`サイト作成者`:`閲覧者`',
        'children:e.contributorRole===`creator`?e.action===`edit`?`サイト作成者が編集`:`サイト作成者が追加`:e.action===`edit`?`閲覧者が編集`:`閲覧者が追加`',
    )
    replace_once(bundle, "history:Re,loading:Be", "history:Re.slice(0,50),loading:Be")


def upgrade_history_attribution() -> None:
    """Upgrade an already-patched bundle without rerunning all replacements."""
    bundle = ROOT / "assets" / "map-experience-admin-2013d629c5.js"
    text = bundle.read_text(encoding="utf-8")
    old_url = "${Cn}/api/history?limit=50"
    new_url = "${Cn}/api/history?limit=300"
    if new_url not in text:
        if text.count(old_url) != 1:
            raise RuntimeError("Expected one public history URL to upgrade")
        text = text.replace(old_url, new_url, 1)
    old_prop = "history:Re,loading:Be"
    new_prop = "history:Re.slice(0,50),loading:Be"
    if new_prop not in text:
        if text.count(old_prop) != 1:
            raise RuntimeError("Expected one public history prop to upgrade")
        text = text.replace(old_prop, new_prop, 1)
    bundle.write_text(text, encoding="utf-8")


def bump_followup_cache_version() -> None:
    """Move already-patched entrypoints to the repaired asset cache key."""
    targets = [
        ROOT / "index.html",
        ROOT / "admin" / "dashboard" / "index.html",
        ROOT / "assets" / "map-Cjgx8Hw7.js",
        ROOT / "assets" / "admin-map-42fb4b0090.js",
    ]
    old_version = "20260905-map-first-review-diff"
    for path in targets:
        text = path.read_text(encoding="utf-8")
        if VERSION in text:
            continue
        if old_version not in text:
            raise RuntimeError(f"No follow-up cache key found in {path.relative_to(ROOT)}")
        path.write_text(text.replace(old_version, VERSION), encoding="utf-8")


def patch_admin_map_first_and_submission_diffs() -> None:
    bundle = ROOT / "assets" / "admin-map-42fb4b0090.js"
    helper_anchor = "function Y({label:e,value:t})"
    helper = r'''function submissionChanges(e,t){let r=t.find(t=>t.id===e.targetStoreId);if(!r)return[];let i=e=>e==null||e===``?`未登録`:String(e),a=e=>e&&n[e]?n[e].label:i(e),o=e=>e&&Ie[e]?Ie[e]:i(e),s=(t,n)=>Object.prototype.hasOwnProperty.call(e,t)?e[t]:n,c=[{field:`店名`,before:r.name,after:s(`proposedName`,r.name),format:i},{field:`カテゴリ`,before:r.category,after:s(`proposedCategory`,r.category),format:a},{field:`状態`,before:r.status,after:s(`proposedStatus`,r.status),format:o},{field:`住所`,before:r.address,after:s(`proposedAddress`,r.address),format:i},{field:`緯度`,before:r.lat,after:s(`proposedLat`,r.lat),format:e=>e==null||e===``?`未登録`:Number(e).toFixed(6)},{field:`経度`,before:r.lng,after:s(`proposedLng`,r.lng),format:e=>e==null||e===``?`未登録`:Number(e).toFixed(6)},{field:`GoogleマップURL`,before:r.googleMapsUrl,after:s(`proposedGoogleMapsUrl`,r.googleMapsUrl),format:i},{field:`開店時期`,before:r.openedYear,after:s(`proposedOpenedYear`,r.openedYear),format:i},{field:`閉店・移転時期`,before:r.closedYear,after:s(`proposedClosedYear`,r.closedYear),format:i},{field:`その後の店舗`,before:r.nextStore,after:s(`proposedNextStore`,r.nextStore),format:i},{field:`補足`,before:r.note,after:s(`proposedNote`,r.note),format:i},{field:`情報源`,before:r.source,after:s(`source`,r.source),format:i}];return c.map(e=>({...e,before:e.format(e.before),after:e.format(e.after)})).filter(e=>e.before!==e.after)}function submissionDiffView(e,t){let n=submissionChanges(e,t);return(0,z.jsxs)(`div`,{className:`admin-submission-change-block`,children:[(0,z.jsx)(`p`,{className:`admin-subsection-title`,children:`変更された内容`}),(0,z.jsx)(`div`,{className:`admin-submission-diff-summary`,children:n.length?(0,z.jsx)(`ul`,{className:`admin-submission-changes`,children:n.map((e,t)=>(0,z.jsxs)(`li`,{children:[(0,z.jsx)(`span`,{children:e.field}),(0,z.jsx)(`del`,{children:e.before}),(0,z.jsx)(`b`,{children:`→`}),(0,z.jsx)(`ins`,{children:e.after})]},`${e.field}-${t}`))}):(0,z.jsx)(`p`,{children:`現在の公開内容との差はありません。`})})]})}'''
    replace_once(bundle, helper_anchor, helper + helper_anchor)

    submission_anchor = r'''e.kind!==`remove`&&(0,z.jsxs)(`div`,{children:[(0,z.jsx)(`p`,{className:`admin-subsection-title`,children:`投稿された内容`}),'''
    submission_replacement = r'''e.kind!==`remove`&&(0,z.jsxs)(`div`,{children:[e.kind===`edit`&&submissionDiffView(e,w.stores),(0,z.jsx)(`p`,{className:`admin-subsection-title`,children:e.kind===`edit`?`修正依頼の入力内容`:`投稿された内容`}),'''
    replace_once(bundle, submission_anchor, submission_replacement)

    old_router = "function He(){return(0,z.jsx)(X,{})}"
    new_router = "function He(){let[e,t]=(0,R.useState)(()=>window.sessionStorage.getItem(G)?`map`:`login`),[n,r]=(0,R.useState)(null);return e===`login`?(0,z.jsx)(X,{loginOnly:!0,onAuthenticated:()=>t(`map`)}):e===`dashboard`?(0,z.jsx)(X,{initialStoreId:n,onLogout:()=>{r(null),t(`login`)},onBackToMap:()=>{r(null),t(`map`)}}):(0,z.jsx)(_,{adminMode:!0,onOpenAdmin:()=>{r(null),t(`dashboard`)},onEditAdminStore:e=>{r(e),t(`dashboard`)},onAddAdminStore:()=>{r(`new`),t(`dashboard`)}})}"
    replace_once(bundle, old_router, new_router)
    replace_once(bundle, "管理メニューを開く", "管理者用の地図を開く")

    legacy = ROOT / "admin" / "index.html"
    replace_once(legacy, ">管理メニューを開く</button>", ">管理者用の地図を開く</button>")
    replace_once(
        legacy,
        '$("loginButton").textContent="管理メニューを開く"',
        '$("loginButton").textContent="管理者用の地図を開く"',
    )

    map_bundle = ROOT / "assets" / "map-experience-admin-2013d629c5.js"
    replace_once(map_bundle, "`管理画面`]}", "`管理メニュー`]}")


def patch_styles() -> None:
    css = ROOT / "assets" / "map-experience-B04n2wOs.css"
    append_once(
        css,
        "BEGIN map-first-review-diff overrides 2026-09-05",
        r'''
/* BEGIN map-first-review-diff overrides 2026-09-05 */
/* The dashboard returns to the public-style administrator map. */
.admin-header-actions > :first-child{display:inline-flex!important}

/* Keep the location picker inside the submission form and make its gesture note unmistakable. */
.public-location-picker{margin-top:4px}
.public-location-picker .location-operation-note{
  display:block!important;
  color:#6f1f19!important;
  background:#fff3cf;
  border:2px solid #d65a27;
  border-radius:9px;
  padding:8px 10px;
  font-size:14px!important;
  font-weight:900;
  line-height:1.55!important;
  box-shadow:0 2px 0 rgba(101,45,22,.08);
}
.public-location-picker .admin-location-map>div:first-child{height:300px}

/* Show pending correction differences in the same before/after style as history. */
.admin-submission-change-block{margin:12px 0 14px}
.admin-submission-diff-summary{background:#fff9ea;border:1px solid #e2c879;border-radius:12px;padding:10px}
.admin-submission-diff-summary>p{margin:0;color:#685b38;font-weight:700}
.admin-submission-changes{list-style:none;margin:0;padding:0;display:grid;gap:8px}
.admin-submission-changes li{display:grid;grid-template-columns:minmax(88px,.65fr) minmax(0,1fr) auto minmax(0,1fr);align-items:start;gap:8px;font-size:12px}
.admin-submission-changes li>span{font-weight:900;color:#574c3b}
.admin-submission-changes del{color:#8c3b35;overflow-wrap:anywhere}
.admin-submission-changes ins{color:#1f6f50;font-weight:800;text-decoration:none;overflow-wrap:anywhere}
.admin-submission-changes b{color:#9a7a25}

@media(max-width:680px){
  .public-location-picker .admin-location-map>div:first-child{height:250px}
  .public-location-picker .location-operation-note{font-size:14px!important}
  .admin-submission-changes li{grid-template-columns:1fr auto 1fr}
  .admin-submission-changes li>span{grid-column:1/-1}
}
/* END map-first-review-diff overrides 2026-09-05 */
''',
    )


def patch_cache_busters() -> None:
    targets = [
        ROOT / "index.html",
        ROOT / "admin" / "dashboard" / "index.html",
        ROOT / "assets" / "map-Cjgx8Hw7.js",
        ROOT / "assets" / "admin-map-42fb4b0090.js",
    ]
    for path in targets:
        text = path.read_text(encoding="utf-8")
        count = text.count("20260904-direct-dashboard")
        if count == 0:
            raise RuntimeError(f"No cache-buster found in {path.relative_to(ROOT)}")
        path.write_text(
            text.replace("20260904-direct-dashboard", VERSION), encoding="utf-8"
        )


def main() -> None:
    patch_source_labels()
    patch_embedded_public_location_picker()
    patch_public_editor_attribution()
    patch_admin_map_first_and_submission_diffs()
    patch_styles()
    patch_cache_busters()
    print("Patched map-first admin flow, review diffs, embedded picker, and labels")


if __name__ == "__main__":
    main()
