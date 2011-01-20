{% from 'macros.tpl' import planetlink, alliancelink with context %}
{% extends "base.tpl" %}
{% set cols = 7 %}
{% if user|intel %}{% set cols = cols + 2 %}{% endif %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}
    <table cellpadding="3" cellspacing="1" class="black">
        <tr class="datahigh"><th colspan="{{cols}}">
            Attack {{ attack.id }} LT: {{ attack.landtick }} {{ attack.comment }}
        </th></tr>
        <tr class="header">
            <th width="60">Coords</th>
            <th width="60">Race</th>
            <th width="60">Size</th>
            <th width="120">Value</th>
            <th width="120">Score</th>
            <th>Scans</th>
            <th>Bookings</th>
            {% if user|intel %}
            <th>Alliance</th>
            <th>Nick</th>
            {% endif %}
        </tr>
        
        {% for planet, scans, bookings in group %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a {{planetlink(planet)}}>{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
            <td class="center {{ planet.race }}">{{ planet.race }}</td>
            <td class="right"> {{ planet.size|intcomma }} </td>
            <td class="right"> {{ planet.value|intcomma }} </td>
            <td class="right"> {{ planet.score|intcomma }} </td>
            <td>
                {% for scan in scans %}
                    <a href="#{{ scan.pa_id }}"
                    onclick="return linkshift(event, '{{ scan.link|url }}');">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
            <td>
                {% for lt, target in bookings %}
                    (
                    {{- lt - tick }}/{{ lt }}
                    {%- if target and target.user == user %}
                        <a href="{% url "unbook", attack.id, planet.x, planet.y, planet.z, lt %}">{{ target.user.name }}</a>
                    {%- elif target %}
                        {{ target.user.name }}
                    {%- elif target == false %}
                        unclaimed
                    {%- elif target is none %}
                        <a href="{% url "book", attack.id, planet.x, planet.y, planet.z, lt %}">book</a>
                    {%- endif -%}
                    )
                {% endfor %}
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
