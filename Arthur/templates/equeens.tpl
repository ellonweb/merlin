{% extends "base.tpl" %}
{% block content %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="3">
            eQueens
        </th>
    </tr>
    <tr class="header">
        <th width="100">User</th>
        <th width="100">Planet</th>
        <th width="100">ePenis</th>
    </tr>
    {% for member, planet, epenis in queens %}
    <tr class="{% cycle 'odd' 'even' %}">
        <td>{{ member }}</td>
        <td>{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</td>
        <td>{{ epenis.penis }}</td>
    </tr>
    {% endfor %}
</table>
</td>
</tr>
</table>
{% endblock %}
