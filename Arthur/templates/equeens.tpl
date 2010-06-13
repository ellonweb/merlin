{% extends "base.tpl" %}
{% block content %}
{% load humanize %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="4">
            eQueens
        </th>
    </tr>
    <tr class="header">
        <th>#</th>
        <th>User</th>
        <th>Planet</th>
        <th>ePenis</th>
    </tr>
    {% for member, planet, epenis in queens %}
    <tr class="{% cycle 'odd' 'even' %}">
        <td>{{ epenis.rank }}</td>
        <td>{{ member.name }}</td>
        <td>{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</td>
        <td>{{ epenis.penis|intcomma }}</td>
    </tr>
    {% endfor %}
</table>
</td>
</tr>
</table>
{% endblock %}
