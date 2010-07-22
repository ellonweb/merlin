{% extends "base.tpl" %}
{% block content %}
<p>&nbsp;</p>

<table>

<tr class="datahigh">
        <th colspan="4">
            {{ title }}
        </th>
    </tr>
<tr class="header">
        <th>Coords</th>
        <th>Scan Type</th>
        <th>Dists</th>
        <th>Requester</th>
    </tr>
{% for req in requests %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center">{{ req.target.x }}:{{ req.target.y }}:{{ req.target.z }}</td>
        <td><a href="{{ req.paurl }}">{{ req.scanname }}</a></td>
        <td>{{ req.dists or "&nbsp;" }}</td>
        <td class="center">{{ req.user.name }}</td>
    </tr>
    {% endfor %}
</table>

<p>&nbsp;</p>
{% endblock %}