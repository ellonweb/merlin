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
{% endblock %}
