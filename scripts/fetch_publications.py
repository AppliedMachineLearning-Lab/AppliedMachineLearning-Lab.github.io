#!/usr/bin/env python3
"""Regenerate _data/publications.yml from DBLP, keeping manual edits intact.

Every AML Lab paper lists Rafet Sifa as a co-author, so his DBLP author page is
used as the lab's publication feed. Run with no arguments:

    python3 scripts/fetch_publications.py

Hand-editing the generated file is supported in two ways:

* ``manual: true`` freezes an entry. It is never overwritten, and it survives
  even if DBLP drops or renames the record. Use this to correct a mangled title
  or to add a paper DBLP does not index (give it a unique ``key`` of your own).
* ``oa_url:`` and the other PRESERVED_FIELDS are carried over on every refresh
  without freezing the rest of the entry, so an open access link added by hand
  sticks while the metadata keeps updating.

Entries are matched across runs by their ``key`` (the DBLP record key), falling
back to the normalised title when the key is not found. The fallback exists
because DBLP re-keys a paper when it graduates from a CoRR preprint to a
published record, and hand edits must follow the paper across that rename.

Note that the whole file is rewritten each run, so YAML comments are not kept.
"""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required to read existing manual edits: pip install pyyaml")

# Rafet Sifa's DBLP author ID. Find it in the "export" links on a DBLP author page.
DBLP_PID = "122/7972"
START_YEAR = 2023

# Hand-edited fields that survive a refresh without freezing the whole entry.
# `superseded: true` hides an entry from the page; it stays in this file so the
# decision is not silently re-made every week when DBLP hands the record back.
PRESERVED_FIELDS = ("oa_url", "superseded")
# Within a year: theses, then books, then papers, then preprints. Anything
# unrecognised sorts with the papers.
TYPE_ORDER = {"phdthesis": 0, "book": 1, "inproceedings": 2, "article": 2, "preprint": 3}
DEFAULT_TYPE_ORDER = 2
# Canonical key order in the output; any other key an editor adds is kept and
# written after these, so the file never silently loses hand-added data.
FIELD_ORDER = (
    "key",
    "title",
    "authors",
    "year",
    "venue",
    "type",
    "url",
    "dblp",
    "oa_url",
    "superseded",
    "manual",
)

OUTPUT = Path(__file__).resolve().parent.parent / "_data" / "publications.yml"
DBLP_URL = f"https://dblp.org/pid/{DBLP_PID}.xml"
USER_AGENT = "AMLLab-Publications-Bot/1.0 (+https://appliedmachinelearning-lab.github.io)"

# DBLP appends a four-digit suffix to homonymous author names ("Kang Liu 0001").
HOMONYM_SUFFIX = re.compile(r"\s+\d{4}$")
# Booktitles carry the proceedings volume for multi-volume conferences ("ECIR (3)").
# "(Findings)" and "(Industry)" are meaningful and must survive.
VOLUME_SUFFIX = re.compile(r"\s*\(\d+\)$")


def fetch(url: str, attempts: int = 4) -> bytes:
    """GET url, backing off on the 429s DBLP hands out to impatient clients."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            retryable = getattr(exc, "code", None) in (429, 500, 502, 503, 504)
            if attempt == attempts or not (retryable or isinstance(exc, (urllib.error.URLError, TimeoutError))):
                raise
            delay = 5 * 2 ** (attempt - 1)
            print(f"  {exc} — retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
    raise RuntimeError("unreachable")


def text_of(element: ET.Element | None) -> str:
    """Flatten an element's text, dropping the inline <i>/<sub> markup DBLP uses."""
    if element is None:
        return ""
    return re.sub(r"\s+", " ", "".join(element.itertext())).strip()


def clean_title(raw: str) -> str:
    return raw.rstrip(".").strip() if raw.endswith(".") else raw


def normalize_title(raw: str) -> str:
    """Key for matching a preprint against its published version."""
    return re.sub(r"[^a-z0-9]", "", raw.lower())


def dblp_link(entry: ET.Element) -> str:
    """DBLP's <url> is relative to the site root ("db/conf/...#key")."""
    url = text_of(entry.find("url"))
    return f"https://dblp.org/{url}" if url else ""


def best_link(entry: ET.Element) -> str:
    """Prefer a DOI, then any other publisher link, then the DBLP record."""
    links = [text_of(ee) for ee in entry.findall("ee") if text_of(ee)]
    for link in links:
        if "doi.org" in link:
            return link
    if links:
        return links[0]
    return dblp_link(entry)


def venue_of(entry: ET.Element) -> str:
    if entry.tag == "inproceedings":
        return VOLUME_SUFFIX.sub("", text_of(entry.find("booktitle")))
    if entry.tag == "article":
        journal = text_of(entry.find("journal"))
        # The template already tags these as preprints, so "arXiv" alone reads better.
        return "arXiv" if journal == "CoRR" else journal
    if entry.tag == "book":
        parts = [text_of(entry.find("series")), text_of(entry.find("publisher"))]
        return ", ".join(part for part in parts if part)
    if entry.tag == "phdthesis":
        # Theses are single-authored, so they only reach DBLP's feed for Rafet's
        # own; lab members' theses have to be added by hand with manual: true.
        return text_of(entry.find("school"))
    return ""


def parse(xml: bytes) -> list[dict]:
    root = ET.fromstring(xml)
    peer_reviewed: list[dict] = []
    preprints: list[dict] = []

    for record in root.findall("r"):
        for entry in record:
            year = entry.findtext("year")
            if not year or int(year) < START_YEAR:
                continue

            title = clean_title(text_of(entry.find("title")))
            if not title:
                continue

            is_preprint = entry.get("publtype") == "informal"
            arxiv_id = ""
            if is_preprint:
                # CoRR entries store the arXiv id in <volume> as "abs/2601.14039".
                arxiv_id = text_of(entry.find("volume")).removeprefix("abs/")

            publication = {
                "key": entry.get("key", ""),
                "title": title,
                "authors": [
                    HOMONYM_SUFFIX.sub("", text_of(author))
                    for author in entry.findall("author")
                ],
                "year": int(year),
                "venue": venue_of(entry),
                "type": "preprint" if is_preprint else entry.tag,
                "url": f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else best_link(entry),
                "dblp": dblp_link(entry),
            }
            (preprints if is_preprint else peer_reviewed).append(publication)

    # A preprint that later appeared at a venue would otherwise be listed twice.
    published_titles = {normalize_title(p["title"]) for p in peer_reviewed}
    unique_preprints = [
        p for p in preprints if normalize_title(p["title"]) not in published_titles
    ]
    dropped = len(preprints) - len(unique_preprints)

    print(
        f"  DBLP: {len(peer_reviewed)} peer-reviewed, {len(unique_preprints)} preprints "
        f"({dropped} superseded preprints dropped)"
    )
    return peer_reviewed + unique_preprints


def load_existing(path: Path) -> list[dict]:
    if not path.exists():
        return []
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    return [entry for entry in loaded if isinstance(entry, dict)]


def merge(fresh: list[dict], existing: list[dict]) -> list[dict]:
    """Overlay hand-edits from the current file onto freshly fetched metadata.

    Entries are matched on the DBLP key, falling back to the normalised title.
    The fallback matters because a paper's key changes when it graduates from a
    CoRR preprint to a published record ("journals/corr/abs-2602-11444" becomes
    "conf/ecir/ChopraSS26"). Without it, hand-added fields would be dropped on
    the floor exactly when a paper is accepted.
    """
    by_key: dict[str, int] = {}
    by_title: dict[str, int] = {}
    for index, entry in enumerate(existing):
        if entry.get("key"):
            by_key.setdefault(entry["key"], index)
        title = normalize_title(entry.get("title", ""))
        if title:
            by_title.setdefault(title, index)

    merged: list[dict] = []
    consumed: set[int] = set()
    frozen = 0
    migrated = 0

    for publication in fresh:
        index = by_key.get(publication["key"])
        if index is None:
            index = by_title.get(normalize_title(publication["title"]))
        if index in consumed:  # already claimed by an earlier fresh entry
            index = None

        previous = None
        if index is not None:
            consumed.add(index)
            previous = existing[index]
            if previous.get("key") and previous["key"] != publication["key"]:
                migrated += 1
                print(
                    f"  Key changed: {previous['key']} -> {publication['key']}\n"
                    f"    {publication['title'][:70]}",
                    file=sys.stderr,
                )
                if previous.get("manual"):
                    print(
                        "    ^ entry is manual:true and stays frozen at the old "
                        "metadata; update it by hand if you want the new record.",
                        file=sys.stderr,
                    )

        if previous and previous.get("manual"):
            merged.append(previous)
            frozen += 1
            continue

        if previous:
            for field in PRESERVED_FIELDS:
                if previous.get(field):
                    publication[field] = previous[field]
        merged.append(publication)

    # Unmatched manual entries: papers added by hand, or records DBLP has since
    # dropped. Anything else that vanished is simply not re-added.
    kept_offline = [
        entry
        for index, entry in enumerate(existing)
        if index not in consumed and entry.get("manual")
    ]
    merged.extend(kept_offline)
    frozen += len(kept_offline)

    dropped = len(existing) - len(consumed) - len(kept_offline)
    print(
        f"  Merge: {frozen} manual entries preserved, {migrated} keys migrated, "
        f"{dropped} stale entries removed, {len(merged)} total"
    )

    # Newest year first, then by kind of publication. Venue and title are only
    # tiebreakers, there to keep the ordering stable across runs so the cron job
    # commits nothing when DBLP hasn't changed.
    merged.sort(
        key=lambda p: (
            -int(p.get("year", 0)),
            TYPE_ORDER.get(p.get("type", ""), DEFAULT_TYPE_ORDER),
            str(p.get("venue", "")).lower(),
            str(p.get("title", "")).lower(),
        )
    )
    return merged


def scalar(value) -> str:
    """Render a scalar. JSON strings are valid YAML double-quoted strings."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return json.dumps(value, ensure_ascii=False)


def to_yaml(publications: list[dict]) -> str:
    """Emit YAML by hand so the field order and quoting stay diff-friendly."""
    lines = [
        "# Generated by scripts/fetch_publications.py from DBLP — refreshed weekly.",
        f"# Source: https://dblp.org/pid/{DBLP_PID}.html (papers from {START_YEAR} onwards)",
        "#",
        "# Hand edits: set `manual: true` on an entry to freeze it (never overwritten,",
        "# and kept even if DBLP drops it). `oa_url:` is preserved on every refresh",
        "# without freezing the entry. Comments in this file are NOT preserved.",
        "#",
        "# Entries are matched by `key`, falling back to the title, so hand edits",
        "# follow a paper when DBLP re-keys it from a preprint to a published record.",
        "",
    ]
    for publication in publications:
        extra = [key for key in publication if key not in FIELD_ORDER]
        keys = [key for key in FIELD_ORDER if key in publication] + sorted(extra)
        prefix = "- "
        for key in keys:
            value = publication[key]
            if isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                lines.extend(f"    - {scalar(item)}" for item in value)
            else:
                lines.append(f"{prefix}{key}: {scalar(value)}")
            prefix = "  "
    return "\n".join(lines) + "\n"


def main() -> int:
    print(f"Fetching {DBLP_URL}")
    publications = merge(parse(fetch(DBLP_URL)), load_existing(OUTPUT))
    if not publications:
        print("Refusing to write an empty publication list.", file=sys.stderr)
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(to_yaml(publications), encoding="utf-8")
    print(f"Wrote {len(publications)} publications to {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
