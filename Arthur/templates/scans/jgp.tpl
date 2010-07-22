<table cellspacing="1" cellpadding="3" width="700" class="black">
{% with planet = scan.planet %}
    {% include "scans/header.tpl" %}
    
    <tr class="header">
        <th width="8%">Target</th>
        <th width="40%">Fleet</th>
        <th width="6%">Race</th>
        <th width="7%">Value</th>
        <th width="5%">ETA</th>
        <th class="right" width="34%">Ships <span class="red">(H)</span>/<span class="green">(F)</span></th>
    </tr>
    
    <tr class="datahigh">
        <td class="center">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td> </td>
        <td class="right">
            <span class="red">{{ scan.total_hostile|intcomma }} ({{ scan.total_hostile_fleets }})</span>
            /
            <span class="green">{{ scan.total_friendly|intcomma }} ({{ scan.total_friendly_fleets }})</span>
        </td>
    </tr>
    
    {% for fleet in scan.fleets %}
    {% with owner = fleet.owner %}
    <tr class="{{ fleet.mission|lower }}">
        <td></td>
        <td nowrap="nowrap">
            {% if fleet.mission|lower == "attack" %}-{% elif fleet.mission|lower == "defend" %}+{% elif fleet.mission|lower == "return"%}~{% endif %}
            {{ fleet.fleet_name }}
            (<a href="{% url "planet", owner.x, owner.y, owner.z %}">{{ owner.x }}:{{ owner.y }}:{{ owner.z }}</a>)
        </td>
        <td class="{{ owner.race }} center"> {{ owner.race }} </td>
        <td class="right"> {{ (owner.score/1000000.0)|round(1) }}M </td>
        <td class="center"> {{ fleet.eta }} </td>
        <td class="right"> {{ fleet.fleet_size|intcomma }}</td>
    </tr>
    {% endwith %}
    {% endfor %}
    
    
    
    <tr class="header">
        <th colspan="6">Overview for each ETA with incoming</th>
    </tr>
    <tr class="datahigh">
        <th> </th>
        <th> Combat Tick </th>
        <th> </th>
        <th> </th>
        <th> ETA </th>
        <th class="right">
        Ships <span class="red">(H)</span>/<span class="green">(F)</span>
        </th>
    </tr>
    
    {% for lt in scan.fleet_overview() %}
    <tr class="{{ loop.cycle('odd', 'even') }} center">
        <td> </td>
        <td> Tick: {{ lt[0] }} </td>
        <td> </td>
        <td> </td>
        <td> {{ lt[1] }} </td>
        <td class="right">
            <span class="red"> {{ lt[3] }} ({{ lt[2] }}) </span>
            /
            <span class="green"> {{ lt[5] }} ({{ lt[4] }}) </span>
        </td>
    </tr>
    {% endfor %}
    
{% endwith %}
</table>
