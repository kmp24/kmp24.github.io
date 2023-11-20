---
title: Portfolio
layout: collection
permalink: /portfolio/
collection: portfolio
entries_layout: grid
classes: wide
---

{% for item in site.portfolio %}
  {% include archive-single.html type="grid" %}
{% endfor %}