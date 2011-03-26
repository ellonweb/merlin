{% macro hplanet(planet, history) %}
<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header">
        <th colspan="12">{{caller()}}</th>
    </tr>
    <tr class="header">
        <th>Tick</th>
        <th>Rank</th>
        <th colspan="2">Size</th>
        <th colspan="3">Value</th>
        <th colspan="2">Score</th>
        <th colspan="2">Experience</th>
        <th>Date / Time</th>
    </tr>
    {% for ph,
        sizediffvalue,
        valuediffwsizevalue,
        resvalue, shipvalue,
        xpvalue in history %}
    <tr class="{% if loop.first %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}" align="right">
        <td>{{ph.tick}}</td>
        <td>{{ph|hrank("score",ph.srankdiff)}}</td>
        <td>{{ph.size|intcomma}}</td>
        <td>{%if ph.rdiff %}{{ph.rdiff|intcomma|change(ph.rdiff, "Value: "+sizediffvalue|intcomma)}}{%endif%}</td>
        <td>{{ph.value|intcomma}}</td>
        <td>{%if ph.vdiff and ph.rdiff %}
            {{ph.vdiff|intcomma|change(ph.vdiff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma + " (Roid Value: "+sizediffvalue|intcomma+")")}}
            {%elif ph.vdiff %}
            {{ph.vdiff|intcomma|change(ph.vdiff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}
            {%endif%}</td>
        <td>{%if ph.rdiff %}{{valuediffwsizevalue|intcomma|change(valuediffwsizevalue, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}{%endif%}</td>
        <td>{{ph.score|intcomma}}</td>
        <td>{%if ph.sdiff %}{{ph.sdiff|intcomma|change(ph.sdiff)}}{%endif%}</td>
        <td>{{ph.xp|intcomma}}</td>
        <td>{%if ph.xdiff %}{{ph.xdiff|intcomma|change(ph.xdiff, xpvalue|intcomma+" points.")}}{%endif%}</td>
        <td>{%if not loop.first%}{{ph.timestamp|date("D d/m H:i")}}{%else%}<strong class="red">NOW</strong>{%endif%}</td>
    </tr>
    {% if ph.timestamp.hour == 0 and not loop.last %}
    <tr class="header">
        <td colspan="12" height="6"/>
    </tr>
    {% endif %}
    {% endfor %}
</table>
{% endmacro %}

{% macro hgalaxy(galaxy, history) %}
<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header">
        <th colspan="16">{{caller()}}</th>
    </tr>
    <tr class="header">
        <th>Tick</th>
        <th>Rank</th>
        <th colspan="2">Planets</th>
        <th colspan="2">Size</th>
        <th colspan="3">Value</th>
        <th colspan="2">Real Score</th>
        <th colspan="2">Score</th>
        <th colspan="2">Experience</th>
        <th>Date / Time</th>
    </tr>
    {% for gh,
        sizediffvalue,
        valuediffwsizevalue,
        resvalue, shipvalue,
        xpvalue in history %}
    <tr class="{% if loop.first %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}" align="right">
        <td>{{gh.tick}}</td>
        <td>{{gh|hrank("score",gh.srankdiff)}}</td>
        <td>{{gh.members}}</td>
        <td>{%if gh.mdiff %}{{gh.mdiff|change(gh.mdiff)}}{%endif%}</td>
        <td>{{gh.size|intcomma}}</td>
        <td>{%if gh.rdiff %}{{gh.rdiff|intcomma|change(gh.rdiff, "Value: "+sizediffvalue|intcomma)}}{%endif%}</td>
        <td>{{gh.value|intcomma}}</td>
        <td>{%if gh.vdiff and gh.rdiff %}
            {{gh.vdiff|intcomma|change(gh.vdiff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma + " (Roid Value: "+sizediffvalue|intcomma+")")}}
            {%elif gh.vdiff %}
            {{gh.vdiff|intcomma|change(gh.vdiff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}
            {%endif%}</td>
        <td>{%if gh.rdiff %}{{valuediffwsizevalue|intcomma|change(valuediffwsizevalue, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}{%endif%}</td>
        <td>{{gh.real_score|intcomma}}</td>
        <td>{%if gh.rsdiff and gh.rdiff %}
            {{gh.rsdiff|intcomma|change(gh.rsdiff, sizediffvalue|intcomma+" from roids. "+valuediffwsizevalue|intcomma+" from value. "+xpvalue|intcomma+" from XP.")}}
            {%elif gh.rsdiff %}
            {{gh.rsdiff|intcomma|change(gh.rsdiff, valuediffwsizevalue|intcomma+" from value. "+xpvalue|intcomma+" from XP.")}}
            {%endif%}
            </td>
        <td>{{gh.score|intcomma}}</td>
        <td>{%if gh.sdiff %}{{gh.sdiff|intcomma|change(gh.sdiff)}}{%endif%}</td>
        <td>{{gh.xp|intcomma}}</td>
        <td>{%if gh.xdiff %}{{gh.xdiff|intcomma|change(gh.xdiff, xpvalue|intcomma+" points.")}}{%endif%}</td>
        <td>{%if not loop.first%}{{gh.timestamp|date("D d/m H:i")}}{%else%}<strong class="red">NOW</strong>{%endif%}</td>
    </tr>
    {% if gh.timestamp.hour == 0 and not loop.last %}
    <tr class="header">
        <td colspan="16" height="6"/>
    </tr>
    {% endif %}
    {% endfor %}
</table>
{% endmacro %}

{% macro halliance(galaxy, history) %}
<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header">
        <th colspan="17">{{caller()}}</th>
    </tr>
    <tr class="header">
        <th>Tick</th>
        <th>Rank</th>
        <th colspan="2">Members</th>
        <th colspan="2">Av. Size</th>
        <th colspan="2">Av. Score</th>
        <th colspan="2">Av. Points</th>
        <th colspan="2">Size</th>
        <th colspan="2">Score</th>
        <th colspan="2">Points</th>
        <th>Date / Time</th>
    </tr>
    {% for ah,
        sizediffvalue,
        scorediffwsizevalue in history %}
    <tr class="{% if loop.first %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}" align="right">
        <td>{{ah.tick}}</td>
        <td>{{ah|hrank("score",ah.srankdiff)}}</td>
        <td>{{ah.members}}</td>
        <td>{%if ah.mdiff %}{{ah.mdiff|change(ah.mdiff)}}{%endif%}</td>
        <td>{{ah.size_avg|intcomma}}</td>
        <td>{%if ah.ravgdiff %}{{ah.ravgdiff|intcomma|change(ah.ravgdiff)}}{%endif%}</td>
        <td>{{ah.score_avg|intcomma}}</td>
        <td>{%if ah.savgdiff %}{{ah.savgdiff|intcomma|change(ah.savgdiff)}}{%endif%}</td>
        <td>{{ah.points_avg|intcomma}}</td>
        <td>{%if ah.pavgdiff %}{{ah.pavgdiff|intcomma|change(ah.pavgdiff)}}{%endif%}</td>
        <td>{{ah.size|intcomma}}</td>
        <td>{%if ah.rdiff %}{{ah.rdiff|intcomma|change(ah.rdiff, "Value: "+sizediffvalue|intcomma)}}{%endif%}</td>
        <td>{{ah.score|intcomma}}</td>
        <td>{%if ah.sdiff and ah.rdiff %}
            {{ah.sdiff|intcomma|change(ah.sdiff, sizediffvalue|intcomma+" from roids. "+scorediffwsizevalue|intcomma+" from value or XP.")}}
            {%elif ah.sdiff %}
            {{ah.sdiff|intcomma|change(ah.sdiff, scorediffwsizevalue|intcomma+" from value or XP.")}}
            {%endif%}
            </td>
        <td>{{ah.points|intcomma}}</td>
        <td>{%if ah.pdiff %}{{ah.pdiff|intcomma|change(ah.pdiff)}}{%endif%}</td>
        <td>{%if not loop.first%}{{ah.timestamp|date("D d/m H:i")}}{%else%}<strong class="red">NOW</strong>{%endif%}</td>
    </tr>
    {% if ah.timestamp.hour == 0 and not loop.last %}
    <tr class="header">
        <td colspan="17" height="6"/>
    </tr>
    {% endif %}
    {% endfor %}
</table>
{% endmacro %}
