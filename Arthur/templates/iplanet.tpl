{% extends "planet_intelintitle.tpl" %}
{% block content %}
{{ super() }}
<p>&nbsp;</p>

<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th>Latest Unit Scan</th>
    </tr>
    <tr><td>{% include "scans/scan.tpl" %}</td></tr>
    <tr class="datahigh">
        <th><a href="{% url "planet_scans", planet.x, planet.y, planet.z %}">More scans</a></th>
    </tr>
</table>
<p>&nbsp;</p>

<table cellspacing="1" cellpadding="3" width="700" class="black">
    <tr class="datahigh">
        <th colspan="6">Outgoing fleets <a href="{% url "fplanet", planet.x, planet.y, planet.z %}">(Show all)</a></th>
    </tr>
    <tr class="header">
        <th width="10%">Target</th>
        <th width="15%">Alliance</th>
        <th width="35%">Fleet</th>
        <th width="15%">Ships</th>
        <th width="10%">Mission</th>
        <th width="15%">Landing Tick</th>
    </tr>
    {% for fleet, planet, alliance in outgoing %}
    <tr class="{{ fleet.mission|lower }}">
        <td class="center"><a href="{% url "planet", planet.x, planet.y, planet.z %}" class="gray">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a> </td>
        <td class="center"> {{ alliance.name }} </td>
        <td class="left"> {{ fleet.fleet_name }} </td>
        <td class="right"> {{ fleet.fleet_size|intcomma }} </td>
        <td class="center"> {{ fleet.mission }} </td>
        <td class="center"> {{ fleet.landing_tick }} </td>
    </tr>
    {% endfor %}
</table>
<p>&nbsp;</p>
<table cellspacing="1" cellpadding="3" width="700" class="black">
    <tr class="datahigh">
        <th colspan="6">Incoming fleets <a href="{% url "fplanet", planet.x, planet.y, planet.z %}">(Show all)</a></th>
    </tr>
    <tr class="header">
        <th width="10%">Origin</th>
        <th width="15%">Alliance</th>
        <th width="35%">Fleet</th>
        <th width="15%">Ships</th>
        <th width="10%">Mission</th>
        <th width="15%">Landing Tick</th>
    </tr>
    {% for fleet, planet, alliance in incoming %}
    <tr class="{{ fleet.mission|lower }}">
        <td class="center"> <a href="{% url "planet", planet.x, planet.y, planet.z %}" class="gray">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a> </td>
        <td class="center"> {{ alliance.name }} </td>
        <td class="left"> {{ fleet.fleet_name }} </td>
        <td class="right"> {{ fleet.fleet_size|intcomma }} </td>
        <td class="center"> {{ fleet.mission }} </td>
        <td class="center"> {{ fleet.landing_tick }} </td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
