---
layout: default
title: TradingView Indicators
---

<h1>{{ site.title }}</h1>
<p class="subtitle">{{ site.description }}</p>

{% assign indicators = site.pages | where: "category", "indicator" | sort: "order" %}
{% if indicators.size > 0 %}
<section>
  <h2>Indicator Guides</h2>
  <ul>
    {% for page in indicators %}
    <li>
      <a href="{{ page.url | relative_url }}">{{ page.title }}</a>
      {% if page.description %}
      <p class="description">{{ page.description }}</p>
      {% endif %}
    </li>
    {% endfor %}
  </ul>
</section>
{% endif %}

{% assign strategies = site.pages | where: "category", "strategy" | sort: "order" %}
{% if strategies.size > 0 %}
<section>
  <h2>Strategies</h2>
  <ul>
    {% for page in strategies %}
    <li>
      <a href="{{ page.url | relative_url }}">{{ page.title }}</a>
      {% if page.description %}
      <p class="description">{{ page.description }}</p>
      {% endif %}
    </li>
    {% endfor %}
  </ul>
</section>
{% endif %}

<footer>
  <p>
    Source code and additional indicators are on
    <a href="https://github.com/n8rzz/trading-view-indicators">GitHub</a>.
  </p>
  <p>These indicators are for educational and analysis purposes only.</p>
</footer>
