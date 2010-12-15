{% extends "planets.tpl" %}
{% block title %}{{ galaxy.name }} ({{ galaxy.x }}:{{ galaxy.y }}){% endblock %}
{% block sort %}{{ order }}{% endblock %}
{% block sort_growth %}{{ order }}{% endblock %}
{% block content %}
{{ super() }}
<p>&nbsp;</p>

<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header">
        <th colspan="8">
            {{galaxy.x}}:{{galaxy.y}} Random Stats
        </th>
    </tr>
    <tr align="right" class="odd">
        <td width="12%">Total Round Roids:</td><td width="12%">{{stats.trr}}</td>
        <td width="12%">Ticks Roiding:</td><td width="12%">{{stats.roiding}}</td>
        <td width="12%">Highest Position:</td><td width="12%">{{stats.highest}} ({{stats.hightick}})</td>
        <td width="12%">Exiles:</td><td width="12%">{{stats.exiles}}</td>
    </tr>
    <tr align="right" class="odd">
        <td width="12%">Total Lost Roids:</td><td width="12%">{{stats.tlr}}</td>
        <td width="12%">Ticks Roided:</td><td width="12%">{{stats.roided}}</td>
        <td width="12%">Lowest Position:</td><td width="12%">{{stats.lowest}} ({{stats.lowtick}})</td>
        <td width="12%">XP/Roid:</td><td width="12%">{{(stats.xp|float/stats.size)|round(2)}}</td>
    </tr>
</table>

<p>&nbsp;</p>

<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header">
        <th>Rank</th>
        <th>Old</th>
        <th>New</th>
        <th>Current</th>
        <th colspan="8">Recent Planet Movements (View more)</th>
        <th colspan="3"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
        <th></th>
    </tr>
    <tr class="header">
        <th>Score</th>
        
        <th align="right">X:Y &nbsp;Z</th>
        <th align="right">X:Y &nbsp;Z</th>
        <th align="right">X:Y &nbsp;Z</th>
        
        <th>Ruler</th>
        <th>Planet</th>
        <th>Race</th>
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        <th>Ratio</th>
        <th>XP</th>
        
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        
        <th>Tick</th>
    </tr>
    {% for exile in exiles %}
    {% set planet = exile.planet %}
    <tr class="{%if not exile.old %}defend{%elif not exile.new %}attack{%else%}odd{%endif%}">
        <td align="right">{%if planet.active %}{{ planet|rank("score") }}{%endif%}</td>
        
        <td align="right">
        {%if exile.old %}
            <a href="{% url "galaxy", exile.oldx, exile.oldy %}">{{ exile.oldx }}:{{ exile.oldy }}</a>
            &nbsp;{{ exile.oldz }}
        {%else%}<span class="green">New</span>{%endif%}
        </td>
        <td align="right">
        {%if exile.new %}
            <a href="{% url "galaxy", exile.newx, exile.newy %}">{{ exile.newx }}:{{ exile.newy }}</a>
            {%if exile.new == planet.galaxy and exile.newz == planet.z %}
            <a href="{% url "planet", exile.newx, exile.newy, exile.newz %}">&nbsp;{{ exile.newz }}</a>
            {%else%}
            &nbsp;{{ exile.newz }}
            {%endif%}
        {%else%}<span class="red">Deleted</span>{%endif%}
        </td>
        <td align="right">
        {%if exile.new and planet.active and (exile.new != planet.galaxy or exile.newz != planet.z)%}
            <a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a href="{% url "planet", planet.x, planet.y, planet.z %}">&nbsp;{{ planet.z }}</a>
        {%endif%}
        </td>
        
        <td>{{ planet.rulername }}</td>
        <td>{{ planet.planetname }}</td>
        <td class="{{ planet.race }}">{{ planet.race }}</td>
        <td align="right">{{ planet|bashcap("size") }}</td>
        <td align="right">{{ planet|bashcap("value") }}</td>
        <td align="right">{{ planet|bashcap("score") }}</td>
        <td align="right">{{ planet.ratio|round(1) }}</td>
        <td align="right">{{ planet.xp|intcomma }}</td>
        
        <td align="right">{{ planet|growth("size") }}</td>
        <td align="right">{{ planet|growth("value") }}</td>
        <td align="right">{{ planet|growth("score") }}</td>
        
        <td align="right">{{exile.tick}}</td>
    </tr>
    {% endfor %}

</table>

{% endblock %}
