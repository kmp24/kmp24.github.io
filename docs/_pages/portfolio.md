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


<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XPBNYW4N8W"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-XPBNYW4N8W');
</script>