{% extends "base.tpl" %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}
    <table align="center" cellpadding="3" cellspacing="1" width="900">
        <tr><td class="menuheader" colspan="7" align="center" height="15">
            Attack {{ attack.id }} LT: {{ attack.landtick }} {{ attack.comment }}
        </td></tr>
        <tr>
            <td class="one" nowrap="nowrap" width="7%"><b>Coords</b></td>
            <td class="one" nowrap="nowrap" width="5%"><b>Race</b></td>
            <td class="one" nowrap="nowrap" width="5%"><b>Size</b></td>
            <td class="one" nowrap="nowrap" width="8%"><b>Value</b></td>
            <td class="one" nowrap="nowrap" width="8%"><b>Score</b></td>
            <td class="one" nowrap="nowrap" width="6%"><b>Scans</b></td>
            <td class="one" nowrap="nowrap" width="61%"><b>Bookings</b></td>
        </tr>
        
        {% for planet, scans, bookings in group %}
        <tr>
            <td class="two center"><a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
            <td class="two {{ planet.race }}">{{ planet.race }}</td>
            <td class="two right"> {{ planet.size }} </td>
            <td class="two right"> {{ planet.value|intcomma }} </td>
            <td class="two right"> {{ planet.score|intcomma }} </td>
            <td class="two left">
                {% for scan in scans %}
                    <a href="#{{ scan.pa_id }}"
                    onclick="return linkshift(event, '{{ scan.link }}');">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
            <td class="two left">
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
