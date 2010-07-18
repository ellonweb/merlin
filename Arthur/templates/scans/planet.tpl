{% extends "base.tpl" %}
{% block content %}
{% include "planet_list.tpl" %}
<p>&nbsp;</p>

    <table align="center" cellpadding="3" cellspacing="1" width="240">
        <tr><td class="menuheader" colspan="2" align="center" height="15">All scans of {{ planet.x }}:{{ planet.y }}:{{ planet.z }}</td></tr>
        <tr>
            <td class="two" nowrap="nowrap" width="25%">Tick</td>
            <td class="one" nowrap="nowrap" width="75%"><b>Scans</b></td>
        </tr>
        
        {% for tick, scans in group %}
        <tr>
            <td class="one left"><a href ="{% url "scan_tick", tick %}">PT: {{ tick }}</a></td>
            <td class="two left">
                {% for scan in scans %}
                    <a href="{% url "scan_id", scan.tick, scan.pa_id %}"
                    onclick="return linkshift(event, '{{ scan.link }}');">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
        </tr>
        {% endfor %}
    </table>
{% endblock %}
