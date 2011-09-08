{% from 'macros.tpl' import planetlink, galaxyscanslink, alliancelink with context %}
{% extends "planets.tpl" %}
{% block header %}
    <tr class="header"><th colspan="{{cols}}">Planet Info</th></tr>
{% endblock %}
{% block title %}
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.rulername|e}}</a>
        <i>of</i>
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.planetname}}</a>
    (<a {{galaxyscanslink(planet.galaxy)}}>{{ planet.x }}:{{ planet.y }}</a>
    <a {{planetlink(planet)}}>{{ planet.z }}</a>)
    <span class="{{planet.race}}">{{planet.race}}</span>
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
{% block extra_title %}
    {%if user|scans%}
    <tr class="datahigh">
        <th colspan="{{cols}}">
            <a href="{% url "planet_scans", planet.x, planet.y, planet.z %}">Scans</a>
        </th>
    </tr>
    {%endif%}
{% endblock %}
{% block intel_head %}{% endblock %}
{% block intel_subhead %}{% endblock %}
{% block intel_content %}{% endblock %}
{% block sort %}{{ order }}{% endblock %}
{% block sort_growth %}{{ order }}{% endblock %}
