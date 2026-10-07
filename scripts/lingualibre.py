#!/usr/bin/env python3
"""Pronunciation of single French words by native speakers, from Lingua Libre.

    scripts/lingualibre.py fetch <mot> ...   download an mp3 of each word into
                                            content/audio/lingualibre/ and print a
                                            dictation item for exercise.yaml

Recordings live on Wikimedia Commons as "LL-Q150 (fra)-<speaker>-<word>.wav".
The license is set per speaker; only CC0, CC BY and CC BY-SA recordings are
taken. Commons serves an mp3 transcode, which is what gets stored.
"""
import json
import pathlib
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
AUDIO = ROOT / "content" / "audio" / "lingualibre"
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "francais-course/1.0 (personal French course; https://github.com/)"}
OPEN = re.compile(r"^(CC0|CC BY(-SA)? \d\.\d|Public domain)$", re.I)


def api(**params):
    params.update(action="query", format="json")
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def candidates(word):
    """File titles recorded for exactly this word, best-known speakers first."""
    res = api(list="search", srnamespace=6, srlimit=50,
              srsearch=f'intitle:"LL-Q150 (fra)" intitle:"-{word}.wav"')
    # Exactly "<speaker>-<word>.wav": a plain suffix match would also take compounds
    # such as "mot-valise" for "valise".
    exact = re.compile(r"^File:LL-Q150 \(fra\)-[^-]+-" + re.escape(word) + r"\.wav$", re.I)
    return [h["title"] for h in res["query"]["search"] if exact.match(h["title"])]


def info(title):
    res = api(titles=title, prop="videoinfo", viprop="url|extmetadata|derivatives")
    page = next(iter(res["query"]["pages"].values()))
    v = page["videoinfo"][0]
    meta = v["extmetadata"]
    mp3 = next((d["src"] for d in v.get("derivatives", []) if d["type"].startswith("audio/mpeg")), None)
    return {
        "license": re.sub(r"<[^>]+>", "", meta.get("LicenseShortName", {}).get("value", "")).strip(),
        "mp3": mp3,
        "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_")),
    }


def fetch(words):
    AUDIO.mkdir(parents=True, exist_ok=True)
    for word in words:
        for title in candidates(word):
            i = info(title)
            if not i["mp3"] or not OPEN.match(i["license"]):
                continue
            # LL-Q150 (fra)-Speaker-mot.wav → speaker between the language tag and the word
            speaker = title[len("File:LL-Q150 (fra)-"):-len(f"-{word}.wav")]
            ascii_name = unicodedata.normalize("NFKD", f"{word}-{speaker}").encode("ascii", "ignore").decode()
            name = re.sub(r"[^A-Za-z0-9.-]+", "_", ascii_name) + ".mp3"
            dst = AUDIO / name
            if not dst.exists():
                req = urllib.request.Request(i["mp3"], headers=UA)
                with urllib.request.urlopen(req, timeout=60) as r:
                    dst.write_bytes(r.read())
            src = {"title": f"Lingua Libre — {word}", "url": i["page"], "author": speaker, "license": i["license"]}
            print(f"  - audio: audio/lingualibre/{name}")
            print(f"    audio_source: {json.dumps(src, ensure_ascii=False)}")
            print(f"    answers: [{json.dumps(word, ensure_ascii=False)}]")
            print(f"    explain: \"TODO\"")
            break
        else:
            print(f"# {word}: no openly licensed recording found", file=sys.stderr)


def main():
    if sys.argv[1:2] == ["fetch"] and len(sys.argv) > 2:
        fetch(sys.argv[2:])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
