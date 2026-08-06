# AppliedMachineLearning-Lab.github.io

This repository contains the website for the Applied Machine Learning (AML) Lab at the University of Bonn.

## Getting Started Locally

Start here: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/testing-your-github-pages-site-locally-with-jekyll

Then:

1. **Install dependencies**:
   ```bash
   bundle config set --local path 'vendor/bundle'
   bundle install
   ```

2. **Run the site locally**:
   ```bash
   bundle exec jekyll serve
   ```

3. **View the site**: Open `http://localhost:4000` in your browser


## Adding a Blog Entry

Create a new file in `_posts/` named `YYYY-MM-DD-your-title.md` with the following front matter:

```markdown
---
layout: post
title: "Your Post Title"
date: YYYY-MM-DD
author: Your Name
categories: [A list of categories]
description: false
---

Your content here...
```

The post will automatically appear on the [/news/](/news/) page. The date in the filename controls the sort order.


## Publications

The list on [/research/publications](/research/publications) is generated from Rafet's DBLP author page, which works as the lab's feed because every lab paper lists him as a co-author. A GitHub Action re-runs `scripts/fetch_publications.py` every Monday and commits `_data/publications.yml` only if something changed, so new papers show up on their own within a week of DBLP indexing them. To pull them in sooner, go to the **Actions** tab -> **Update publications** -> **Run workflow**.

Everything below is done by editing `_data/publications.yml` and committing it to `main`. Your edits are kept on the next refresh, the script merges them back in rather than overwriting the file blindly. Note that YAML comments in that file are *not* preserved, since it gets rewritten on every run.

### Adding a paper

Normally you don't have to: anything on DBLP appears automatically. Only add a paper by hand if DBLP does not index it (a tech report, say). Append an entry with `manual: true` and a `key` of your own that does not look like a DBLP key:

```yaml
- key: "manual/aml/tech-report-2026"
  title: "A Paper DBLP Does Not Know About"
  authors:
    - "Jane Doe"
    - "Rafet Sifa"
  year: 2026
  venue: "AML Lab Technical Report"
  type: "inproceedings"
  url: "https://example.org/the-paper.pdf"
  dblp: ""
  manual: true
```

`type:` controls the badge: `inproceedings` or `article` for a normal venue, `preprint`, `book`, or `phdthesis`. The `venue:` string is shown as the blue tag.

### Adding a PhD thesis

Theses always have to be added by hand. A thesis is single-authored, so Rafet is not a co-author and it never shows up in the DBLP feed the rest of the list comes from. Use `type: "phdthesis"` for the **PhD Thesis** badge, and put the awarding university in `venue:`:

```yaml
- key: "manual/thesis/deusser2026"
  title: "Hybrid Representation Learning for Information Extraction"
  authors:
    - "Tobias Deußer"
  year: 2026
  venue: "University of Bonn"
  type: "phdthesis"
  url: "https://doi.org/10.48565/bonndoc-823"
  dblp: ""
  manual: true
```

Prefer the bonndoc DOI for `url:` over the handle, since it is the stable citation target. Leave `dblp: ""` unless the thesis genuinely has a DBLP record. There is no need for a separate `oa_url` here, because the bonndoc record the title already links to *is* the open access version.

### Correcting a paper

If DBLP has something wrong (a mangled title, a bad link), fix the field in place and add `manual: true` to that entry:

```yaml
- key: "conf/exampleconf/authortitle23"
  title: "The Correct Title"
  ...
  manual: true
```

That freezes the **whole** entry: it is never overwritten again, and it stays on the page even if DBLP later drops the record. The trade-off is that it also stops receiving legitimate updates, so use it only where DBLP is actually wrong. If a frozen paper is later re-indexed under a new DBLP key — which happens when a preprint gets published — the workflow log warns you, and you will need to update the entry by hand.

### Hiding a superseded preprint

When a preprint is published, the fetch script normally drops the preprint automatically. That only works when both records carry the same title. If the published version renames the paper, both show up and you get the same work listed twice. Set `superseded: true` on the **preprint** to hide it:

```yaml
- key: "journals/corr/abs-2311-15679"
  title: "Model-agnostic Body Part Relevance Assessment for Pedestrian Detection"
  ...
  superseded: true
```

The entry stays in the file, so the decision is not quietly re-made the next time DBLP hands the record back, but it no longer appears on the page or in any of the counts. Like `oa_url`, this does not need `manual: true` and does not stop the entry's metadata from refreshing.

### Adding an open access link

Add an `oa_url` pointing at the version in bonndoc or Fraunhofer Publica:

```yaml
- key: "conf/exampleconf/authortitle23"
  ...
  oa_url: "https://bonndoc.ulb.uni-bonn.de/xmlui/handle/20.500.11811/12345"
```

This shows a green **Open Access** badge next to the paper, with the repository named in the tooltip. Do **not** add `manual: true` for this, because `oa_url` is carried over on every refresh on its own, and it follows the paper even if DBLP re-keys it from a preprint to a published record. Adding `manual: true` would needlessly freeze the rest of the metadata as well.

### Running the fetch locally

```bash
pip install pyyaml
python3 scripts/fetch_publications.py
```

This rewrites `_data/publications.yml` in place. The year cut-off and the DBLP author ID are the `START_YEAR` and `DBLP_PID` constants at the top of the script.


## Files

Please *do not* commit files for downloading (like lecture slides or assignments) into this repo. Create a separate repo or use a different hoster for this.
