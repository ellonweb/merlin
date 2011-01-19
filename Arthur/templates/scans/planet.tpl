{% extends "planet_intelintitle.tpl" %}
{% block extra_title %}
    {%if user|intel%}
    <tr class="datahigh">
        <th colspan="{{cols}}">
            <a href="{% url "iplanet", planet.x, planet.y, planet.z %}">Intel</a>
        </th>
    </tr>
    {%endif%}
{% endblock %}
{% block content %}
{{ super() }}
<p>&nbsp;</p>

    <table cellspacing="1" cellpadding="3" width="240" class="black">
        <tr class="datahigh"><th colspan="2">All scans of {{ planet.x }}:{{ planet.y }}:{{ planet.z }}</th></tr>
        <tr class="header">
            <th width="25%">Tick</th>
            <th width="75%">Scans</th>
        </tr>
        
        {% for tick, scans in group %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="right"><a href ="{% url "scan_tick", tick %}">{{ tick }}</a></td>
            <td>
                {% for scan in scans %}
                    <a href="{% url "scan_id", scan.tick, scan.pa_id %}"
                    onclick="return linkshift(event, '{{ scan.link|url }}');">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
        </tr>
        {% endfor %}
    </table>
{% endblock %}
