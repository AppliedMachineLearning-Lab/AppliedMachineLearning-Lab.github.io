---
layout: default
title: Applied Machine Learning Lab
---
<link rel="icon" type="image/x-icon" href="/assets/aml_lab_tight.ico" />

![AML Lab Team](/assets/team_rafet.jpg)

Welcome to the web page of the Applied Machine Learning (AML) Lab at the University of Bonn. Led by Prof. Dr. Rafet Sifa, the Applied Machine Learning Lab focuses on addressing the challenges of implementing machine learning models in real-world settings while developing novel methods for pattern analysis and representation learning. The lab's primary area of investigation is based on constructing hybrid, interpretable, and resource-aware learning systems with practical applications in text mining, behavioral analytics, and medical informatics.

At AML Lab, we have made it our mission to bridge the gap between cutting-edge technology and everyday challenges.

If you want to reach out to us, please write to:

`amllab[at]bit.uni-bonn.de`

## Latest Updates

{% assign latest = site.posts.first %}
{% if latest %}
<article class="post-card">
  <h2 class="post-card-title"><a href="{{ latest.url | relative_url }}">{{ latest.title }}</a></h2>
  <div class="post-meta">
    <time datetime="{{ latest.date | date_to_xmlschema }}">{{ latest.date | date: "%B %-d, %Y" }}</time>
    {% if latest.author %} &middot; {{ latest.author }}{% endif %}
    {% if latest.categories.size > 0 %}
      &middot; {% for cat in latest.categories %}<span class="post-tag">{{ cat }}</span>{% unless forloop.last %} {% endunless %}{% endfor %}
    {% endif %}
  </div>
  <div class="post-excerpt">
    {{ latest.excerpt | strip_html | truncatewords: 60 }}
  </div>
  <a href="{{ latest.url | relative_url }}" class="read-more-link">Read more &rarr;</a>
</article>
{% endif %}

[Find more news here...](/news/)
