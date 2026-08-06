---
layout: default
title: Publications
description: Peer-reviewed papers and preprints from the AML Lab
---

# Publications

A list of the lab's research output since its inception. The list is generated automatically
from [dblp]({{ site.dblp_author_url }}) and refreshed weekly, so it may lag a few days
behind the most recent acceptances.

{% comment %}
  Entries flagged `superseded: true` stay in the data file as a record of the
  decision, but are hidden here. That is how a preprint is retired once the
  published version appears under a different title.
{% endcomment %}
{% assign publications = site.data.publications | where_exp: "p", "p.superseded != true" %}
{% assign years = publications | map: "year" | uniq | sort | reverse %}

<div class="pub-summary">
  <strong>{{ publications | size }}</strong> publications
  &middot; <a href="{{ site.dblp_author_url }}">dblp</a>
  &middot; <a href="{{ site.scholar_author_url }}">Google Scholar</a>
</div>

<nav class="pub-yearnav">
  {% for year in years %}<a href="#y{{ year }}">{{ year }}</a>{% endfor %}
</nav>

{% comment %}
  The data file is already sorted by year, then by kind of publication (thesis,
  book, paper, preprint), so each year renders in a single pass.
{% endcomment %}
{% for year in years %}
  {% assign in_year = publications | where: "year", year %}

<h2 id="y{{ year }}" class="pub-year">{{ year }}<span class="pub-count">{{ in_year | size }}</span></h2>

<ul class="pub-list">
  {% for publication in in_year %}{% include publication.html publication=publication %}{% endfor %}
</ul>
{% endfor %}
