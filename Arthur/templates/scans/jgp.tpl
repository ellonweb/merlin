<table width="700" class="scan">
{% with planet = scan.planet %}
    {% include "scans/header.tpl" %}
    
    <tr height="20">
        <td class="menuheader" height="25" width="10%">Target</td>
        <td class="menuheader" width="35%">Planet</td>
        <td class="menuheader" width="5%">Race</td>
        <td class="menuheader" width="10%">Value</td>
        <td class="menuheader" width="5%">ETA</td>
        <td class="menuheader right" width="40%">Ships <span class="attack">(H)</span>/<span class="defend">(F)</span></td>
    </tr>
    
    <tr>
        <td class="one white">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</td>
        <td class="two"> </td>
        <td class="one"> </td>
        <td class="one"> </td>
        <td class="one"> </td>
        <td class="two right">
            <span class="attack">{{ scan.total_hostile|intcomma }} ({{ scan.total_hostile_fleets }})</span>
            /
            <span class="defend">{{ scan.total_friendly|intcomma }} ({{ scan.total_friendly_fleets }})</span>
        </td>
    </tr>
    
    {% for fleet in scan.fleets %}
    {% with owner = fleet.owner %}
    <tr>
        <td class="one"></td>
        <td class="two {{ fleet.mission|lower }} left" nowrap="nowrap">
            {% if fleet.mission|lower == "attack" %}-{% elif fleet.mission|lower == "defend" %}+{% elif fleet.mission|lower == "return"%}~{% endif %}
            {{ fleet.fleet_name }}
            (<a href="{% url "planet", owner.x, owner.y, owner.z %}">{{ owner.x }}:{{ owner.y }}:{{ owner.z }}</a>)
        </td>
        <td class="one {{ fleet.mission|lower }}"> {{ owner.race }} </td>
        <td class="one {{ fleet.mission|lower }}"> {{ (owner.score/1000000.0)|round(1) }}M </td>
        <td class="one {{ fleet.mission|lower }}"> {{ fleet.eta }} </td>
        <td class="two {{ fleet.mission|lower }} right"> {{ fleet.fleet_size|intcomma }}</td>
    </tr>
    {% endwith %}
    {% endfor %}
    
    
    
    <tr height="20">
        <td class="menuheader" colspan="6" align="center" height="25">Overview for each ETA with incoming</td>
    </tr>
    <tr height="20">
        <td class="menuheader" height="25" width="10%"> </td>
        <td class="menuheader" width="35%"> Combat Tick </td>
        <td class="menuheader" width="5%"> </td>
        <td class="menuheader" width="10%"> </td>
        <td class="menuheader" width="5%"> ETA </td>
        <td class="menuheader right" width="40%">
        Ships <span class="attack">(H)</span>/<span class="defend">(F)</span>
        </td>
    </tr>
    
    {% for lt in scan.fleet_overview() %}
    <tr>
        <td class="one"> </td>
        <td class="two"> Tick: {{ lt[0] }} </td>
        <td class="one"> </td>
        <td class="one"> </td>
        <td class="one"> {{ lt[1] }} </td>
        <td class="two right">
            <span class="attack"> {{ lt[3] }} ({{ lt[2] }}) </span>
            /
            <span class="defend"> {{ lt[5] }} ({{ lt[4] }}) </span>
        </td>
    </tr>
    {% endfor %}
    
{% endwith %}
</table>
