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
    {% for ph, timestamp,
        oldrank,
        sizediff, sizediffvalue,
        valuediff, valuediffwsizevalue,
        resvalue, shipvalue,
        xpdiff, xpvalue,
        scorediff in history %}
    <tr class="{% if loop.first %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}" align="right">
        <td>{{ph.tick}}</td>
        <td>{{ph|hrank("score",oldrank)}}</td>
        <td>{{ph.size|intcomma}}</td>
        <td>{%if sizediff %}{{sizediff|intcomma|change(sizediff, "Value: "+sizediffvalue|intcomma)}}{%endif%}</td>
        <td>{{ph.value|intcomma}}</td>
        <td>{%if valuediff and sizediff %}
            {{valuediff|intcomma|change(valuediff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma + " (Roid Value: "+sizediffvalue|intcomma+")")}}
            {%elif valuediff %}
            {{valuediff|intcomma|change(valuediff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}
            {%endif%}</td>
        <td>{%if sizediff %}{{valuediffwsizevalue|intcomma|change(valuediffwsizevalue, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}{%endif%}</td>
        <td>{{ph.score|intcomma}}</td>
        <td>{%if scorediff %}{{scorediff|intcomma|change(scorediff)}}{%endif%}</td>
        <td>{{ph.xp|intcomma}}</td>
        <td>{%if xpdiff %}{{xpdiff|intcomma|change(xpdiff, xpvalue|intcomma+" points.")}}{%endif%}</td>
        <td>{{timestamp|date("D d/m H:i")}}</td>
    </tr>
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
    {% for gh, timestamp,
        oldrank, membersdiff,
        sizediff, sizediffvalue,
        valuediff, valuediffwsizevalue,
        resvalue, shipvalue,
        xpdiff, xpvalue,
        scorediff, realscorediff in history %}
    <tr class="{% if loop.first %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}" align="right">
        <td>{{gh.tick}}</td>
        <td>{{gh|hrank("score",oldrank)}}</td>
        <td>{{gh.members}}</td>
        <td>{%if membersdiff %}{{membersdiff|change(membersdiff)}}{%endif%}</td>
        <td>{{gh.size|intcomma}}</td>
        <td>{%if sizediff %}{{sizediff|intcomma|change(sizediff, "Value: "+sizediffvalue|intcomma)}}{%endif%}</td>
        <td>{{gh.value|intcomma}}</td>
        <td>{%if valuediff and sizediff %}
            {{valuediff|intcomma|change(valuediff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma + " (Roid Value: "+sizediffvalue|intcomma+")")}}
            {%elif valuediff %}
            {{valuediff|intcomma|change(valuediff, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}
            {%endif%}</td>
        <td>{%if sizediff %}{{valuediffwsizevalue|intcomma|change(valuediffwsizevalue, "Resources: "+resvalue|intcomma +" / Ships: "+shipvalue|intcomma)}}{%endif%}</td>
        <td>{{gh.real_score|intcomma}}</td>
        <td>{%if realscorediff and sizediff %}
            {{realscorediff|intcomma|change(realscorediff, sizediffvalue|intcomma+" from roids. "+valuediffwsizevalue|intcomma+" from value. "+xpvalue|intcomma+" from XP.")}}
            {%elif realscorediff %}
            {{realscorediff|intcomma|change(realscorediff, valuediffwsizevalue|intcomma+" from value. "+xpvalue|intcomma+" from XP.")}}
            {%endif%}
            </td>
        <td>{{gh.score|intcomma}}</td>
        <td>{%if scorediff %}{{scorediff|intcomma|change(scorediff)}}{%endif%}</td>
        <td>{{gh.xp|intcomma}}</td>
        <td>{%if xpdiff %}{{xpdiff|intcomma|change(xpdiff, xpvalue|intcomma+" points.")}}{%endif%}</td>
        <td>{{timestamp|date("D d/m H:i")}}</td>
    </tr>
    {% endfor %}
</table>
{% endmacro %}
