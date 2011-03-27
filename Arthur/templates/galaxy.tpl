{% from 'macros.tpl' import galaxyscanslink with context %}
{% from 'history.tpl' import hgalaxy %}
{% from 'exiles.tpl' import exiletable with context %}
{% extends "planets.tpl" %}
{% block title %}
    <a class="{%if user.planet and galaxy == user.planet.galaxy %}myplanet{%else%}gray{%endif%}" {{galaxyscanslink(galaxy)}}>{{galaxy.name}}</a>
    (<a {{galaxyscanslink(galaxy)}}>{{ galaxy.x }}:{{ galaxy.y }}</a>)
        -
    Real Score: {{galaxy.real_score|intcomma}} ({{galaxy|rank("score")}})
{% endblock %}
{% block extra_title %}
    {%if user|scans%}
    <tr class="datahigh">
        <th colspan="{{cols}}">
            <a href="{% url "galaxy_scans", galaxy.x, galaxy.y %}">Scans</a>
        </th>
    </tr>
    {%endif%}
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
        <td width="12%">Exiles:</td><td width="12%">{{galaxy.exile_count}}</td>
    </tr>
    <tr align="right" class="odd">
        <td width="12%">Total Lost Roids:</td><td width="12%">{{galaxy.totallostroids|intcomma}}</td>
        <td width="12%">Ticks Roided:</td><td width="12%">{{galaxy.ticksroided}}</td>
        <td width="12%">Lowest Position:</td><td width="12%">{{galaxy.score_lowest_rank}} (PT{{galaxy.score_lowest_rank_tick}})</td>
        <td width="12%">XP/Roid:</td><td width="12%">{{galaxy.roidxp|round(2)}}</td>
    </tr>
</table>

<p>&nbsp;</p>

{% call exiletable(exiles) %}Recent Planet Movements <a href="{% url "galaxy_exiles", galaxy.x, galaxy.y %}">(View more)</a>{% endcall %}

<p>&nbsp;</p>

{% call hgalaxy(galaxy, history) %}Last 12 Ticks (<a href="{%url "hgalaxy", galaxy.x, galaxy.y, 72%}">View more</a>){% endcall %}
{% endblock %}
