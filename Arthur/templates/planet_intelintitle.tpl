{% from 'macros.tpl' import alliancelink with context %}
{% extends "planets.tpl" %}
{% block title %}
    <a href="{% url "planet", planet.x, planet.y planet.z %}">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a>
    {% if user|intel %}
        {% if planet.intel and planet.intel.nick %}
            <i>{{ planet.intel.nick }}</i>
            {% if planet.alliance %}
                /
            {% endif %}
        {% endif %}
        {% if planet.intel and planet.alliance %}
            <a {{alliancelink(planet.alliance.name)}}>
            <i>{{ planet.alliance.name }}</i>
            </a>
        {% endif %}
    {% endif %}
{% endblock %}
{% block intel_head %}{% endblock %}
{% block intel_subhead %}{% endblock %}
{% block intel_content %}{% endblock %}
{% block sort %}{{ order }}{% endblock %}
{% block sort_growth %}{{ order }}{% endblock %}
