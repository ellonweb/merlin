{% extends "planets.tpl" %}
{% block title %}{{ alliance.name }} (<a href="{% url "alliance_history", alliance.name %}">History</a>){% endblock %}
