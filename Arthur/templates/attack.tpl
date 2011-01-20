{% from 'macros.tpl' import planetlink, galaxyscanslink, alliancelink with context %}
{% extends "base.tpl" %}
{% set cols = 9 %}
{% if user|intel %}{% set cols = cols + 2 %}{% endif %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}
    <table cellpadding="3" cellspacing="1" width="95%" class="black">
        <tr class="datahigh"><th colspan="{{cols}}">
            Attack {{ attack.id }} LT: {{ attack.landtick }} {{ attack.comment }}
        </th></tr>
        <tr class="header">
            <th>Coords</th>
            <th>Race</th>
            <th>Size</th>
            <th>Value</th>
            <th>Score</th>
            <th>Scans</th>
            <th>Bookings</th>
            <th><a href="" onclick="toggleGrowth();return false;">Size</a></th>
            <th><a href="" onclick="toggleGrowth();return false;">Value</a></th>
            {% if user|intel %}
            <th>Alliance</th>
            <th>Nick</th>
            {% endif %}
        </tr>
        
        {% for planet, scans, bookings in group %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a {{galaxyscanslink(planet.galaxy)}}>{{ planet.x }}:{{ planet.y }}</a> <a {{planetlink(planet)}}>{{ planet.z }}</a></td>
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
                        <b><i>
                        <a href="{% url "unbook", attack.id, planet.x, planet.y, planet.z, lt %}">{{ target.user.name }}</a>
                        </i></b>
                    {%- elif target %}
                        <b><i>
                        {{ target.user.name }}
                        </i></b>
                    {%- elif target == false %}
                        unclaimed
                    {%- elif target is none %}
                        <a href="{% url "book", attack.id, planet.x, planet.y, planet.z, lt %}">book</a>
                    {%- endif -%}
                    )
                {% endfor %}
            <td align="right">{{ planet|growth("size") }}</td>
            <td align="right">{{ planet|growth("value") }}</td>
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
