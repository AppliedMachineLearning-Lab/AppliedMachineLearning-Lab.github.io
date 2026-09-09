#!/usr/bin/env python3
"""Regenerate _data/publications.yml from DBLP, keeping manual edits intact.

Every AML Lab paper lists Rafet Sifa as a co-author, so his DBLP record is used
as the lab's publication feed. Run with no arguments:

    python3 scripts/fetch_publications.py

Data comes from DBLP's SPARQL endpoint rather than the per-author XML export,
because in September 2026 DBLP put its main site (the XML export and the search
API included) behind an Anubis proof-of-work bot check, which no unattended
script can pass. sparql.dblp.org serves the same knowledge graph unchallenged.

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
import urllib.parse
import urllib.request
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
SPARQL_URL = "https://sparql.dblp.org/sparql"
REC_PREFIX = "https://dblp.org/rec/"
USER_AGENT = "AMLLab-Publications-Bot/1.0 (+https://appliedmachinelearning-lab.github.io)"

# DBLP appends a four-digit suffix to homonymous author names ("Kang Liu 0001").
HOMONYM_SUFFIX = re.compile(r"\s+\d{4}$")
# Some venue labels carry the proceedings volume for multi-volume conferences
# ("ECIR (3)"). "(Findings)" and "(Industry)" are meaningful and must survive.
VOLUME_SUFFIX = re.compile(r"\s*\(\d+\)$")
# Separators for packing ordered author names into one GROUP_CONCAT string.
# Chosen so they cannot occur inside a DBLP author name.
AUTHOR_SEP, ORDINAL_SEP = "@@", "~~"

QUERY = f"""
PREFIX dblp: <https://dblp.org/rdf/schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?pub ?year ?type
       (SAMPLE(?t) AS ?title) (SAMPLE(?bt) AS ?bibtex) (SAMPLE(?v) AS ?venue)
       (SAMPLE(?d) AS ?doi) (SAMPLE(?dp) AS ?docpage)
       (SAMPLE(?vol) AS ?volume) (SAMPLE(?toc) AS ?tocpage)
       (SAMPLE(?sch) AS ?school) (SAMPLE(?pby) AS ?publisher)
       (GROUP_CONCAT(CONCAT(STR(?ord), "{ORDINAL_SEP}", ?name);
                     separator="{AUTHOR_SEP}") AS ?authors)
WHERE {{
  ?pub dblp:authoredBy <https://dblp.org/pid/{DBLP_PID}> ;
       dblp:title ?t ;
       dblp:yearOfPublication ?year ;
       a ?type .
  FILTER(?type != dblp:Publication)
  FILTER(xsd:integer(STR(?year)) >= {START_YEAR})
  OPTIONAL {{ ?pub dblp:bibtexType ?bt }}
  OPTIONAL {{ ?pub dblp:publishedIn ?v }}
  OPTIONAL {{ ?pub dblp:doi ?d }}
  OPTIONAL {{ ?pub dblp:primaryDocumentPage ?dp }}
  OPTIONAL {{ ?pub dblp:publishedInJournalVolume ?vol }}
  OPTIONAL {{ ?pub dblp:listedOnTocPage ?toc }}
  OPTIONAL {{ ?pub dblp:thesisAcceptedBySchool ?sch }}
  OPTIONAL {{ ?pub dblp:publishedBy ?pby }}
  ?pub dblp:hasSignature ?sig .
  ?sig dblp:signatureOrdinal ?ord ;
       dblp:signatureDblpName ?name .
}}
GROUP BY ?pub ?year ?type
"""


def fetch(attempts: int = 4) -> dict:
    """Run the SPARQL query, backing off on the endpoint's transient errors."""
    body = urllib.parse.urlencode({"query": QUERY}).encode()
    request = urllib.request.Request(
        SPARQL_URL,
        data=body,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/sparql-results+json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                raw = response.read()
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                # A bot-check or maintenance page arrives as HTML with status 200,
                # so a bad body has to be treated as a failure in its own right.
                snippet = raw[:200].decode("utf-8", "replace").replace("\n", " ")
                raise RuntimeError(f"expected JSON, got: {snippet}")
        except (urllib.error.URLError, TimeoutError, RuntimeError) as exc:
            if attempt == attempts:
                raise
            delay = 5 * 2 ** (attempt - 1)
            print(f"  {exc} — retrying in {delay}s", file=sys.stderr)
            time.sleep(delay)
    raise RuntimeError("unreachable")


def clean_title(raw: str) -> str:
    raw = re.sub(r"\s+", " ", raw).strip()
    return raw[:-1].strip() if raw.endswith(".") else raw


def normalize_title(raw: str) -> str:
    """Key for matching a preprint against its published version."""
    return re.sub(r"[^a-z0-9]", "", raw.lower())


def authors_of(packed: str) -> list[str]:
    """Unpack the "<ordinal>~~<name>@@..." blob into author order."""
    people = []
    for item in packed.split(AUTHOR_SEP):
        ordinal, _, name = item.partition(ORDINAL_SEP)
        if not name:
            continue
        try:
            rank = int(ordinal)
        except ValueError:
            rank = 999
        people.append((rank, HOMONYM_SUFFIX.sub("", name.strip())))
    return [name for _, name in sorted(people)]


def parse(payload: dict) -> list[dict]:
    peer_reviewed: list[dict] = []
    preprints: list[dict] = []

    for row in payload["results"]["bindings"]:
        def value(name: str) -> str:
            return row.get(name, {}).get("value", "").strip()

        title = clean_title(value("title"))
        key = value("pub").removeprefix(REC_PREFIX)
        if not title or not key:
            continue

        rdf_type = value("type").rsplit("#", 1)[-1]
        is_thesis = value("bibtex").endswith("Phdthesis")
        is_preprint = rdf_type == "Informal"
        kind = {
            "Inproceedings": "inproceedings",
            "Article": "article",
            "Informal": "preprint",
            "Book": "phdthesis" if is_thesis else "book",
        }.get(rdf_type, "inproceedings")

        # CoRR records carry the arXiv id in the journal volume ("abs/2601.14039").
        arxiv_id = value("volume").removeprefix("abs/") if is_preprint else ""

        if is_preprint:
            venue = "arXiv"
        elif is_thesis:
            venue = value("school")
        elif kind == "book":
            # Books read better with their publisher: "Cognitive Technologies, Springer".
            venue = ", ".join(p for p in (value("venue"), value("publisher")) if p)
        else:
            venue = VOLUME_SUFFIX.sub("", value("venue"))

        # DBLP's TOC page plus the record key is the human-facing record link.
        toc = value("tocpage")
        dblp_link = f"{toc}.html#{key.rsplit('/', 1)[-1]}" if toc else ""

        if arxiv_id:
            url = f"https://arxiv.org/abs/{arxiv_id}"
        else:
            url = value("doi") or value("docpage") or dblp_link

        publication = {
            "key": key,
            "title": title,
            "authors": authors_of(value("authors")),
            "year": int(value("year")),
            "venue": venue,
            "type": kind,
            "url": url,
            "dblp": dblp_link,
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
        f"# Source: sparql.dblp.org, author pid {DBLP_PID} (papers from {START_YEAR} onwards)",
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
    print(f"Querying {SPARQL_URL} for pid {DBLP_PID}")
    publications = merge(parse(fetch()), load_existing(OUTPUT))
    if not publications:
        print("Refusing to write an empty publication list.", file=sys.stderr)
        return 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(to_yaml(publications), encoding="utf-8")
    print(f"Wrote {len(publications)} publications to {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
