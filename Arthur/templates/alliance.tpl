{% extends "planets.tpl" %}
{% block title %}{{ alliance.name }} (<a href="{% url "alliance_history", alliance.name %}">History</a>){% endblock %}
{% block intel_head %}<th>Intel</th>{% endblock %}
{% block intel_subhead %}<th>Nick</th>{% endblock %}
{% block intel_content %}<td>{%if nick %}{{ nick }}{% endif %}</td>{% endblock %}
