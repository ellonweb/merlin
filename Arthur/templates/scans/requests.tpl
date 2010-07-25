{% extends "base.tpl" %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}

{% include "scans/request.tpl" %}
<p>&nbsp;</p>

<table>

<tr class="datahigh">
        <th colspan="4">
            Active requests
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
        <td><a href="{{ req.link }}">{{ req.type }}</a></td>
        <td>i:{{ req.target.intel.dists }}/r:{{ req.dists }}</td>
        <td class="center">{{ req.user.name }}</td>
    </tr>
    {% endfor %}
</table>

{% endblock %}