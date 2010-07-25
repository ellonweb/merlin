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

<p>&nbsp;</p>

<table>

    <tr class="datahigh">
        <th colspan="6">
            My Recent Requests
        </th>
    </tr>
    <tr class="header">
      <th colspan="2">
        Request
      </th>
      <th colspan="4">
        Result
      </th>
    </tr>
    <tr class="header">
        <th>Coords</th>
        <th>Scan Type</th>
        <th>Link</th>
        <th>Tick</th>
        <th>Scanned  by</th>
        <th>Planetarion Url</th>
    </tr>
    {% for req in userrequests %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center">{{ req.target.x }}:{{ req.target.y }}:{{ req.target.z }}</td>
        <td><a href="{{ req.link }}">{{ req.type }}</a></td>
        {% if req.scan %}
          <td class="center"><a href="{% url "scan_id", req.scan.tick, req.scan.pa_id %}"
                    onclick="return linkshift(event, '{{ req.scan.link }}');">{{ req.scan.scantype }}</a></td>
          <td class="center">{{ req.scan.tick }}</td>
          <td class="center">{{ req.scan.scanner.name }}</td>
          <td class="center"><a href="{{ req.scan.link }}" target="_blank">{{ req.scan.pa_id }}</a></td>
        {% endif %}
    </tr>
    {% endfor %}
</table>

{% endblock %}