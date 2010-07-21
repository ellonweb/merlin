{% extends "base.tpl" %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}
    <table cellpadding="3" cellspacing="1" width="900" class="black">
        <tr class="datahigh"><th colspan="7">
            Attack {{ attack.id }} LT: {{ attack.landtick }} {{ attack.comment }}
        </th></tr>
        <tr class="header">
            <th width="7%">Coords</th>
            <th width="5%">Race</th>
            <th width="5%">Size</th>
            <th width="8%">Value</th>
            <th width="8%">Score</th>
            <th width="6%">Scans</th>
            <th width="61%">Bookings</th>
        </tr>
        
        {% for planet, scans, bookings in group %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
            <td class="center {{ planet.race }}">{{ planet.race }}</td>
            <td class="right"> {{ planet.size|intcomma }} </td>
            <td class="right"> {{ planet.value|intcomma }} </td>
            <td class="right"> {{ planet.score|intcomma }} </td>
            <td>
                {% for scan in scans %}
                    <a href="#{{ scan.pa_id }}"
                    onclick="return linkshift(event, '{{ scan.link }}');">{{ scan.scantype }}</a>
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
        </tr>
        {% endfor %}
    </table>
    
    {% for scan in scans %}
    <p>&nbsp;</p>
    {% include "scans/scan.tpl" %}
    {% endfor %}
{% endblock %}
