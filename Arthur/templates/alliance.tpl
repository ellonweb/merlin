{% extends "planets.tpl" %}
{% block title %}{{ alliance.name }} (<a href="{% url "alliance_history", alliance.name %}">History</a>), list of {{ planets|count }} members in intel ({{ alliance.members }} in tag){% endblock %}
{% block intel_head %}<th>Intel</th>{% endblock %}
{% block intel_subhead %}<th>Nick</th>{% endblock %}
{% block intel_content %}<td>{%if nick %}{{ nick }}{% endif %}</td>{% endblock %}
{% block sort %}<a href="{% url "alliance", alliance.name, race|default("all"), order|lower, page|default(1) %}">{{ order }}</a>{% endblock %}
{% block page %}{% url "alliance", alliance.name, race, sort, p %}{% endblock %}
