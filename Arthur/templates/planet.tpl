{% from 'macros.tpl' import planetlink, alliancelink with context %}
{% from 'history.tpl' import hplanet %}
{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header"><th colspan="10">Planet Info</th></tr>
    <tr class="datahigh">
        <th align="center" colspan="10">
            <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.rulername}}</a>
                <i>of</i>
            <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.planetname}}</a>
            (<a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a {{planetlink(planet)}}>{{ planet.z }}</a>)
            <span class="{{planet.race}}">{{planet.race}}</span>
        </th>
    </tr>
    {%if user|intel%}
    <tr class="datahigh">
        <th align="center" colspan="10">
            <a href="{% url "iplanet", planet.x, planet.y, planet.z %}">
            Intel{%if planet.intel and (planet.intel.nick or planet.alliance)%}:{%endif%}
            </a>
            {% if planet.intel and planet.intel.nick %}
                <i>{{ planet.intel.nick }}</i>
                {% if planet.alliance %}
                    /
                {% endif %}
            {% endif %}
            {% if planet.intel and planet.alliance %}
                <a {{alliancelink(planet.alliance.name)}}>
                <i>{{ planet.alliance.name }}</i>
                </a>
            {% endif %}
        </th>
    </tr>
    {%endif%}
    <tr class="header">
        <td colspan="10" height="6"/>
    </tr>
    <tr class="datahigh">
        <td width="10%">&nbsp;</td>
        <td width="10%">&nbsp;</td>
        <td width="10%" nowrap="">Rank /{{update.planets}}</td>
        <td width="10%" nowrap="">Cluster Rank /{{planet.galaxy.cluster.members}}</td>
        <td width="10%" nowrap="">Galaxy Rank /{{planet.galaxy.members}}</td>
        <td width="10%" nowrap=""><span class="{{planet.race}}">{{planet.race}}</span> Rank /{{update[planet.race|lower]}}</td>
        <td nowrap="">Highest Rank</td>
        <td nowrap="">Lowest Rank</td>
        <td width="20%" nowrap="" align="center" colspan="2">Today's Growth</td>
    </tr>
    
    <tr class="odd" align="right">
        <td nowrap="">Size:</td>
        <td>{{planet.size|intcomma}}</td>
        <td>{{planet|rank("size")}}</td>
        <td>{{planet|rank("cluster_size")}}</td>
        <td>{{planet|rank("galaxy_size")}}</td>
        <td>{{planet|rank("race_size")}}</td>
        <td>{{planet.size_highest_rank}} (PT{{planet.size_highest_rank_tick}})</td>
        <td>{{planet.size_lowest_rank}} (PT{{planet.size_lowest_rank_tick}})</td>
        <td>{{planet.size_growth|change(planet.size_growth)}}</td>
        <td>{{planet.size_growth_pc|change(planet.size_growth_pc)}}</td>
    </tr>
    <tr class="even" align="right">
        <td nowrap="">Value:</td>
        <td>{{planet.value|intcomma}}</td>
        <td>{{planet|rank("value")}}</td>
        <td>{{planet|rank("cluster_value")}}</td>
        <td>{{planet|rank("galaxy_value")}}</td>
        <td>{{planet|rank("race_value")}}</td>
        <td>{{planet.value_highest_rank}} (PT{{planet.value_highest_rank_tick}})</td>
        <td>{{planet.value_lowest_rank}} (PT{{planet.value_lowest_rank_tick}})</td>
        <td>{{planet.value_growth|change(planet.value_growth)}}</td>
        <td>{{planet.value_growth_pc|change(planet.value_growth_pc)}}</td>
    </tr>
    <tr class="datahigh" align="right">
        <td nowrap="">Score:</td>
        <td>{{planet.score|intcomma}}</td>
        <td>{{planet|rank("score")}}</td>
        <td>{{planet|rank("cluster_score")}}</td>
        <td>{{planet|rank("galaxy_score")}}</td>
        <td>{{planet|rank("race_score")}}</td>
        <td>{{planet.score_highest_rank}} (PT{{planet.score_highest_rank_tick}})</td>
        <td>{{planet.score_lowest_rank}} (PT{{planet.score_lowest_rank_tick}})</td>
        <td>{{planet.score_growth|change(planet.score_growth)}}</td>
        <td>{{planet.score_growth_pc|change(planet.score_growth_pc)}}</td>
    </tr>
    <tr class="even" align="right">
        <td nowrap="">XP:</td>
        <td>{{planet.xp|intcomma}}</td>
        <td>{{planet|rank("xp")}}</td>
        <td>{{planet|rank("cluster_xp")}}</td>
        <td>{{planet|rank("galaxy_xp")}}</td>
        <td>{{planet|rank("race_xp")}}</td>
        <td>{{planet.xp_highest_rank}} (PT{{planet.xp_highest_rank_tick}})</td>
        <td>{{planet.xp_lowest_rank}} (PT{{planet.xp_lowest_rank_tick}})</td>
        <td>{{planet.xp_growth|change(planet.xp_growth)}}</td>
        <td>{{planet.xp_growth_pc|change(planet.xp_growth_pc)}}</td>
    </tr>
    <tr class="odd" align="right">
        <td nowrap="">Total Round Roids:</td>
        <td>{{planet.totalroundroids|intcomma}}</td>
        <td>{{planet|rank("totalroundroids")}}</td>
        <td>{{planet|rank("cluster_totalroundroids")}}</td>
        <td>{{planet|rank("galaxy_totalroundroids")}}</td>
        <td>{{planet|rank("race_totalroundroids")}}</td>
        <td></td>
        <td></td>
        <td>{{planet.totalroundroids_growth|change(planet.totalroundroids_growth)}}</td>
        <td>{{planet.totalroundroids_growth_pc|change(planet.totalroundroids_growth_pc)}}</td>
    </tr>
    <tr class="even" align="right">
        <td nowrap="">Total Lost Roids:</td>
        <td>{{planet.totallostroids|intcomma}}</td>
        <td>{{planet|rank("totallostroids")}}</td>
        <td>{{planet|rank("cluster_totallostroids")}}</td>
        <td>{{planet|rank("galaxy_totallostroids")}}</td>
        <td>{{planet|rank("race_totallostroids")}}</td>
        <td></td>
        <td></td>
        <td>{{planet.totallostroids_growth|change(planet.totallostroids_growth)}}</td>
        <td>{{planet.totallostroids_growth_pc|change(planet.totallostroids_growth_pc)}}</td>
    </tr>
    <tr class="header">
        <td colspan="10" height="6"/>
    </tr>
    <tr class="odd" align="right">
        <td></td>
        <td></td>
        <td>Ticks Roiding:</td>
        <td>{{planet.ticksroiding}}</td>
        <td>Exiles:</td>
        <td>(View) {{planet.exile_count()}}</td>
        <td>XP per Roid:</td>
        <td>{{(planet.xp|float/planet.size)|round(2)}}</td>
        <td>Tick-Roids:</td>
        <td>{{planet.tickroids|intcomma}}</td>
    </tr>
    <tr class="even" align="right">
        <td></td>
        <td></td>
        <td>Ticks Roided:</td>
        <td>{{planet.ticksroided}}</td>
        <td>Idle:</td>
        <td></td>
        <td>Ratio:</td>
        <td>{{planet.ratio|round(2)}}</td>
        <td>Av. Roids:</td>
        <td>{{planet.avroids|int|intcomma}}</td>
    </tr>
</table>

<p>&nbsp;</p>

{% call hplanet(planet, history) %}Last 12 Ticks (<a href="{%url "hplanet", planet.x, planet.y, planet.z, 72%}">View more</a>){% endcall %}
{% endblock %}
