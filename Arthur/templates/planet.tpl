{% extends "base.tpl" %}
{% block content %}
{% include "planet_list.tpl" %}
<p />
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
	<tr class="datahigh">
		<th colspan="6">Outgoing fleets <a href="{% url planet planet.x planet.y planet.z %}fleets/">(Show all)</a></th>
	</tr>
	<tr class="header">
		<th>Target</th>
		<th>Alliance</th>
		<th>Fleet</th>
		<th>Ships</th>
		<th>Mission</th>
		<th>Landing Tick</th>
	</tr>
    {% for fleet, planet, alliance in outgoing %}
	<tr class="{{ fleet.mission|lower }}">
		<td><a href="{% url planet planet.x planet.y planet.z %}" class="gray">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
		<td>{{ alliance.name }}</td>
		<td>{{ fleet.fleet_name }}</td>
		<td>{{ fleet.fleet_size }}</td>
		<td>{{ fleet.mission }}</td>
		<td>{{ fleet.landing_tick }}</td>
	</tr>
	{% endfor %}
</table>
</td>
</tr>
</table>
<p />
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
	<tr class="datahigh">
		<th colspan="6">Incoming fleets <a href="{% url planet planet.x planet.y planet.z %}fleets/">(Show all)</a></th>
	</tr>
	<tr class="header">
		<th>Origin</th>
		<th>Alliance</th>
		<th>Fleet</th>
		<th>Ships</th>
		<th>Mission</th>
		<th>Landing Tick</th>
	</tr>
    {% for fleet, planet, alliance in incoming %}
	<tr class="{{ fleet.mission|lower }}">
		<td><a href="{% url planet planet.x planet.y planet.z %}" class="gray">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
		<td>{{ alliance.name }}</td>
		<td>{{ fleet.fleet_name }}</td>
		<td>{{ fleet.fleet_size }}</td>
		<td>{{ fleet.mission }}</td>
		<td>{{ fleet.landing_tick }}</td>
	</tr>
	{% endfor %}
</table>
</td>
</tr>
</table>
{% endblock %}
