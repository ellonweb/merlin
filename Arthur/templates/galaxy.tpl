{% from 'history.tpl' import hgalaxy %}
{% extends "planets.tpl" %}
{% block title %}
    <a class="{%if user.planet and galaxy == user.planet.galaxy %}myplanet{%else%}gray{%endif%}" {% url "galaxy", galaxy.x, galaxy.y %}>{{galaxy.name}}</a>
    (<a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a>)
        -
    Real Score: {{galaxy.real_score|intcomma}} ({{galaxy|rank("score")}})
{% endblock %}
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
        <td width="12%">Total Round Roids:</td><td width="12%">{{galaxy.totalroundroids|intcomma}}</td>
        <td width="12%">Ticks Roiding:</td><td width="12%">{{galaxy.ticksroiding}}</td>
        <td width="12%">Highest Position:</td><td width="12%">{{galaxy.score_highest_rank}} (PT{{galaxy.score_highest_rank_tick}})</td>
        <td width="12%">Exiles:</td><td width="12%">{{exilecount}}</td>
    </tr>
    <tr align="right" class="odd">
        <td width="12%">Total Lost Roids:</td><td width="12%">{{galaxy.totallostroids|intcomma}}</td>
        <td width="12%">Ticks Roided:</td><td width="12%">{{galaxy.ticksroided}}</td>
        <td width="12%">Lowest Position:</td><td width="12%">{{galaxy.score_lowest_rank}} (PT{{galaxy.score_lowest_rank_tick}})</td>
        <td width="12%">XP/Roid:</td><td width="12%">{{galaxy.roidxp|round(2)}}</td>
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
        {%if not planet.active %}
        <td align="center" colspan="8"><i>Planet doesn't exist anymore.</i></td>
        {%else%}
        <td align="right">{{ planet|bashcap("size") }}</td>
        <td align="right">{{ planet|bashcap("value") }}</td>
        <td align="right">{{ planet|bashcap("score") }}</td>
        <td align="right">{{ planet.ratio|round(1) }}</td>
        <td align="right">{{ planet.xp|intcomma }}</td>
        
        <td align="right">{{ planet|growth("size") }}</td>
        <td align="right">{{ planet|growth("value") }}</td>
        <td align="right">{{ planet|growth("score") }}</td>
        {%endif%}
        
        <td align="right">{{exile.tick}}</td>
    </tr>
    {% endfor %}

</table>

<p>&nbsp;</p>

{% call hgalaxy(galaxy, history) %}Last 12 Ticks (<a href="{%url "hgalaxy", galaxy.x, galaxy.y, 72%}">View more</a>){% endcall %}
{% endblock %}
