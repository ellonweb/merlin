{% from 'macros.tpl' import alliancelink with context %}
{% from 'history.tpl' import halliance %}
{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="60%" class="black">
    <tr class="header"><th colspan="7">Alliance Info</th></tr>
    <tr class="datahigh">
        <th align="center" colspan="7">
            <a class="{%if user|intel and alliance.name == name %}myplanet{%else%}gray{%endif%}" {{alliancelink(alliance)}}>{{alliance.name}}</a>
        </th>
    </tr>
    <tr class="header">
        <td colspan="7" height="6"/>
    </tr>
    <tr class="datahigh">
        <td width="20%">&nbsp;</td>
        <td width="15%">&nbsp;</td>
        <td width="15%">Rank</td>
        <td width="15%" nowrap="">Highest Rank</td>
        <td width="15%" nowrap="">Lowest Rank</td>
        <td width="20%" nowrap="" align="center" colspan="2">Today's Growth</td>
    </tr>
    
    <tr class="odd" align="right">
        <td nowrap="">Size:</td>
        <td>{{alliance.size|intcomma}}</td>
        <td>{{alliance|rank("size")}}</td>
        <td>{{alliance.size_highest_rank}} (PT{{alliance.size_highest_rank_tick}})</td>
        <td>{{alliance.size_lowest_rank}} (PT{{alliance.size_lowest_rank_tick}})</td>
        <td>{{alliance.size_growth|change(alliance.size_growth)}}</td>
        <td>{{alliance.size_growth_pc|round(1)|change(alliance.size_growth_pc)}}</td>
    </tr>
    <tr class="datahigh" align="right">
        <td nowrap="">Score:</td>
        <td>{{alliance.score|intcomma}}</td>
        <td>{{alliance|rank("score")}}</td>
        <td>{{alliance.score_highest_rank}} (PT{{alliance.score_highest_rank_tick}})</td>
        <td>{{alliance.score_lowest_rank}} (PT{{alliance.score_lowest_rank_tick}})</td>
        <td>{{alliance.score_growth|change(alliance.score_growth)}}</td>
        <td>{{alliance.score_growth_pc|round(1)|change(alliance.score_growth_pc)}}</td>
    </tr>
    <tr class="even" align="right">
        <td nowrap="">Points:</td>
        <td>{{alliance.points|intcomma}}</td>
        <td>{{alliance|rank("points")}}</td>
        <td>{{alliance.points_highest_rank}} (PT{{alliance.points_highest_rank_tick}})</td>
        <td>{{alliance.points_lowest_rank}} (PT{{alliance.points_lowest_rank_tick}})</td>
        <td>{{alliance.points_growth|change(alliance.points_growth)}}</td>
        <td>{{alliance.points_growth_pc|round(1)|change(alliance.points_growth_pc)}}</td>
    </tr>
    <tr class="odd" align="right">
        <td nowrap="">Average Size:</td>
        <td>{{alliance.size_avg|intcomma}}</td>
        <td>{{alliance|rank("size_avg")}}</td>
        <td>{{alliance.size_avg_highest_rank}} (PT{{alliance.size_avg_highest_rank_tick}})</td>
        <td>{{alliance.size_avg_lowest_rank}} (PT{{alliance.size_avg_lowest_rank_tick}})</td>
        <td>{{alliance.size_avg_growth|change(alliance.size_avg_growth)}}</td>
        <td>{{alliance.size_avg_growth_pc|round(1)|change(alliance.size_avg_growth_pc)}}</td>
    </tr>
    <tr class="even" align="right">
        <td nowrap="">Average Score:</td>
        <td>{{alliance.score_avg|intcomma}}</td>
        <td>{{alliance|rank("score_avg")}}</td>
        <td>{{alliance.score_avg_highest_rank}} (PT{{alliance.score_avg_highest_rank_tick}})</td>
        <td>{{alliance.score_avg_lowest_rank}} (PT{{alliance.score_avg_lowest_rank_tick}})</td>
        <td>{{alliance.score_avg_growth|change(alliance.score_avg_growth)}}</td>
        <td>{{alliance.score_avg_growth_pc|round(1)|change(alliance.score_avg_growth_pc)}}</td>
    </tr>
    <tr class="odd" align="right">
        <td nowrap="">Average Points:</td>
        <td>{{alliance.points_avg|intcomma}}</td>
        <td>{{alliance|rank("points_avg")}}</td>
        <td>{{alliance.points_avg_highest_rank}} (PT{{alliance.points_avg_highest_rank_tick}})</td>
        <td>{{alliance.points_avg_lowest_rank}} (PT{{alliance.points_avg_lowest_rank_tick}})</td>
        <td>{{alliance.points_avg_growth|change(alliance.points_avg_growth)}}</td>
        <td>{{alliance.points_avg_growth_pc|round(1)|change(alliance.points_avg_growth_pc)}}</td>
    </tr>
    <tr class="even" align="right">
        <td nowrap="">Total Round Roids:</td>
        <td>{{alliance.totalroundroids|intcomma}}</td>
        <td>{{alliance|rank("totalroundroids")}}</td>
        <td></td>
        <td></td>
        <td>{{alliance.totalroundroids_growth|change(alliance.totalroundroids_growth)}}</td>
        <td>{{alliance.totalroundroids_growth_pc|round(1)|change(alliance.totalroundroids_growth_pc)}}</td>
    </tr>
    <tr class="odd" align="right">
        <td nowrap="">Total Lost Roids:</td>
        <td>{{alliance.totallostroids|intcomma}}</td>
        <td>{{alliance|rank("totallostroids")}}</td>
        <td></td>
        <td></td>
        <td>{{alliance.totallostroids_growth|change(alliance.totallostroids_growth)}}</td>
        <td>{{alliance.totallostroids_growth_pc|round(1)|change(alliance.totallostroids_growth_pc)}}</td>
    </tr>
    <tr class="header">
        <td colspan="7" height="6"/>
    </tr>
    <tr class="even" align="right">
        <td></td>
        <td>Members:</td>
        <td>{{alliance|members}}</td>
        <td>Ratio:</td>
        <td>{{alliance.ratio|round(2)}}</td>
        <td colspan="2"></td>
    </tr>
</table>

<p>&nbsp;</p>

{% call halliance(alliance, history) %}Last 12 Ticks (<a href="{%url "halliance", alliance.name, 72%}">View more</a>){% endcall %}
{% endblock %}
