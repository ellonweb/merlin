{% extends "base.tpl" %}
{% block content %}
    <table cellspacing="1" cellpadding="3" width="600" class="black">
        <tr class="datahigh"><th colspan="6">
            {% block title scoped %}Scans belonging to this group:{% endblock %}
        </th></tr>
        <tr class="header">
            <th width="10%">Coords</th>
            <th width="10%">Race</th>
            <th width="10%">Size</th>
            <th width="20%">Value</th>
            <th width="20%">Score</th>
            <th width="30%">Scans</th>
        </tr>
        
        {% for planet, scans in group %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
            <td class="center {{ planet.race }}">{{ planet.race }}</td>
            <td class="right"> {{ planet.size|intcomma }} </td>
            <td class="right"> {{ planet.value|intcomma }} </td>
            <td class="right"> {{ planet.score|intcomma }} </td>
            <td>
                {% for scan in scans %}
                    <a href="{% block url scoped %}#{{ scan.pa_id }}{% endblock %}"
                    onclick="return linkshift(event, '{{ scan.link }}');">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
        </tr>
        {% endfor %}
    </table>
    
    {% for scan in scans %}
    <p>&nbsp;</p>
    {% include "scans/scan.tpl" %}
    {% endfor %}
{% endblock %}
