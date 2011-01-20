{% from 'macros.tpl' import planetscanslink, alliancelink with context %}
{% extends "base.tpl" %}
{% set cols = 6 %}
{% if user|intel %}{% set cols = cols + 2 %}{% endif %}
{% block content %}
    <table cellspacing="1" cellpadding="3" class="black">
        <tr class="datahigh"><th colspan="{{cols}}">
            {% block title scoped %}Scans belonging to this group:{% endblock %}
        </th></tr>
        <tr class="header">
            <th width="60">Coords</th>
            <th width="60">Race</th>
            <th width="60">Size</th>
            <th width="120">Value</th>
            <th width="120">Score</th>
            <th>Scans</th>
            {% if user|intel %}
            <th>Alliance</th>
            <th>Nick</th>
            {% endif %}
        </tr>
        
        {% for planet, scans in group %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a {{planetscanslink(planet)}}>{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
            <td class="center {{ planet.race }}">{{ planet.race }}</td>
            <td class="right"> {{ planet.size|intcomma }} </td>
            <td class="right"> {{ planet.value|intcomma }} </td>
            <td class="right"> {{ planet.score|intcomma }} </td>
            <td>
                {% for scan in scans %}
                    <a href="{% block url scoped %}#{{ scan.pa_id }}{% endblock %}"
                    onclick="return linkshift(event, '{{ scan.link|url }}');">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
            {% if user|intel %}
            <td>{%if planet.intel and planet.alliance %}<a {{alliancelink(planet.alliance.name)}}>{{ planet.alliance.name }}</a>{% endif %}</td>
            <td>{%if planet.intel.nick %}{{ planet.intel.nick }}{% endif %}</td>
            {% endif %}
        </tr>
        {% endfor %}
    </table>
    
    {% for scan in scans %}
    <p>&nbsp;</p>
    {% include "scans/scan.tpl" %}
    {% endfor %}
{% endblock %}
