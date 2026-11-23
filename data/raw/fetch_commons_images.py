#!/usr/bin/env python3
"""
Download heritage images from Wikimedia Commons with licence + author metadata.
Run LOCALLY (needs internet).  pip install requests

Examples
  python fetch_commons_images.py --category "Museums in Kangla" --depth 1 --out media/images
  python fetch_commons_images.py --search "Kangla Imphal" --search "Lai Haraoba" --max-files 150

Only files with a free licence (CC*, public domain, PD*) are downloaded by default.
Output: <out>/*.jpg plus images_manifest.csv (title, file page URL, licence, author, size, local path).
Always keep the manifest: it is your provenance + attribution record.
"""
import argparse, csv, html, os, re, time
import requests

API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "heritage-kg-research/0.1 (set-your-contact-email@example.com)"}
FREE = re.compile(r"^(cc[ -]|cc0|public domain|pd[ -]|pd$|attribution)", re.I)
IMG_MIME = {"image/jpeg", "image/png", "image/webp"}


def strip_html(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def get(params):
    p = {"format": "json", "formatversion": "2", **params}
    r = requests.get(API, params=p, headers=HEADERS, timeout=30)
    r.raise_for_status()
    time.sleep(0.5)  # be polite
    return r.json()


IMGINFO = {"prop": "imageinfo", "iiprop": "url|mime|size|extmetadata", "iiurlwidth": 1024}


def pages_from(data):
    q = data.get("query", {})
    pages = q.get("pages", [])
    return pages if isinstance(pages, list) else list(pages.values())


def category_files(cat, depth, seen=None):
    """Yield file pages (with imageinfo) from a category and sub-categories up to `depth`."""
    seen = seen if seen is not None else set()
    if cat in seen:
        return
    seen.add(cat)
    cont = {}
    while True:
        d = get({"action": "query", "generator": "categorymembers", "gcmtitle": f"Category:{cat}",
                 "gcmtype": "file", "gcmlimit": 50, **IMGINFO, **cont})
        for p in pages_from(d):
            yield p
        if "continue" in d:
            cont = d["continue"]
        else:
            break
    if depth > 0:
        cont = {}
        while True:
            d = get({"action": "query", "list": "categorymembers", "cmtitle": f"Category:{cat}",
                     "cmtype": "subcat", "cmlimit": 50, **cont})
            for m in d.get("query", {}).get("categorymembers", []):
                yield from category_files(m["title"].replace("Category:", "", 1), depth - 1, seen)
            if "continue" in d:
                cont = d["continue"]
            else:
                break


def search_files(term, limit):
    cont = {}
    got = 0
    while got < limit:
        d = get({"action": "query", "generator": "search", "gsrsearch": term, "gsrnamespace": 6,
                 "gsrlimit": 50, **IMGINFO, **cont})
        for p in pages_from(d):
            yield p
            got += 1
        if "continue" in d:
            cont = d["continue"]
        else:
            break


def to_record(page):
    """Convert an API page dict into a manifest record, or None if unusable."""
    ii = (page.get("imageinfo") or [None])[0]
    if not ii or ii.get("mime") not in IMG_MIME:
        return None
    md = ii.get("extmetadata", {})
    val = lambda k: strip_html(md.get(k, {}).get("value", ""))
    licence = val("LicenseShortName")
    return {
        "title": page.get("title", ""),
        "file_page_url": ii.get("descriptionurl", ""),
        "download_url": ii.get("thumburl") or ii.get("url", ""),
        "original_url": ii.get("url", ""),
        "mime": ii.get("mime", ""),
        "width": ii.get("width", ""), "height": ii.get("height", ""),
        "licence": licence, "licence_url": val("LicenseUrl"),
        "author": val("Artist"), "credit": val("Credit"),
        "description": val("ImageDescription")[:300],
        "is_free_licence": bool(FREE.match(licence)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--category", action="append", default=[])
    ap.add_argument("--search", action="append", default=[])
    ap.add_argument("--depth", type=int, default=1)
    ap.add_argument("--max-files", type=int, default=200)
    ap.add_argument("--out", default="media/images")
    ap.add_argument("--allow-nonfree", action="store_true", help="also download files without a recognised free licence (NOT recommended)")
    ap.add_argument("--dry-run", action="store_true", help="write manifest only, do not download images")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    streams = [category_files(c, a.depth) for c in a.category] + [search_files(s, a.max_files) for s in a.search]
    rows, seen = [], set()
    for stream in streams:
        for page in stream:
            if len(rows) >= a.max_files:
                break
            rec = to_record(page)
            if not rec or rec["title"] in seen:
                continue
            seen.add(rec["title"])
            if not rec["is_free_licence"] and not a.allow_nonfree:
                continue
            fname = re.sub(r"[^A-Za-z0-9._-]+", "_", rec["title"].replace("File:", ""))[:120]
            rec["local_path"] = os.path.join(a.out, fname)
            if not a.dry_run:
                try:
                    r = requests.get(rec["download_url"], headers=HEADERS, timeout=60)
                    r.raise_for_status()
                    open(rec["local_path"], "wb").write(r.content)
                    time.sleep(0.5)
                except Exception as e:
                    print("skip", rec["title"], e)
                    continue
            rows.append(rec)
            print(f"[{len(rows)}] {rec['title']}  ({rec['licence']})")

    if rows:
        path = os.path.join(a.out, "images_manifest.csv")
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
        print("manifest:", path, "| files:", len(rows))
    else:
        print("No usable files found.")


if __name__ == "__main__":
    main()
