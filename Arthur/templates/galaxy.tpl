{% extends "planets.tpl" %}
{% block title %}{{ galaxy.name }} ({{ galaxy.x }}:{{ galaxy.y }}){% endblock %}
{% block sort %}{{ order }}{% endblock %}
{% block sort_growth %}{{ order }}{% endblock %}
