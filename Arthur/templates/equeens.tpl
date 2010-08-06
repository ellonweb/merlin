{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th colspan="4">
            eQueens
        </th>
    </tr>
    <tr class="header">
        <th width="20">#</th>
        <th width="70">User</th>
        <th width="60">Planet</th>
        <th width="65">ePenis</th>
    </tr>
    {% for member, p, epenis in queens %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="right">{{ epenis.rank }}</td>
        <td class="center"><a href="{% url "dashboard", member.name %}">{{ member.name }}</a></td>
        <td class="center"><a href="{% url "planet", p.x, p.y, p.z %}">{{ p.x }}:{{ p.y }}:{{ p.z }}</a></td>
        <td class="right">{{ epenis.penis|intcomma }}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
