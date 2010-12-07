{% extends "planets.tpl" %}
{% block title %}
    {{ planet.x }}:{{ planet.y }}:{{ planet.z }}
    {% if user|intel %}
        {% if planet.intel and planet.intel.nick %}
            <i>{{ planet.intel.nick }}</i>
            {% if planet.alliance %}
                /
            {% endif %}
        {% endif %}
        {% if planet.intel and planet.alliance %}
            <i>{{ planet.alliance.name }}</i>
        {% endif %}
    {% endif %}
{% endblock %}
{% block intel_head %}{% endblock %}
{% block intel_subhead %}{% endblock %}
{% block intel_content %}{% endblock %}
{% block sort %}{{ order }}{% endblock %}
{% block sort_growth %}{{ order }}{% endblock %}
