{% extends "planets.tpl" %}
{% set orders = (
                    ("", "",),
                    ("xyz", "Coords",),
                    ("size", "Size",),
                    ("size_growth", "Size Growth",),
                    ("size_growth_pc", "Size Growth %",),
                    ("value", "Value",),
                    ("value_growth", "Value Growth",),
                    ("value_growth_pc", "Value Growth %",),
                    ("score", "Score",),
                    ("score_growth", "Score Growth",),
                    ("score_growth_pc", "Score Growth %",),
                    ("ratio", "Ratio",),
                    ("xp", "Experience",),
                    ("xp_growth", "Experience Growth",),
                    ("xp_growth_pc", "Experience Growth %",),
                    ("totalroundroids", "[Total Round Roids]",),
                    ("totallostroids", "[Total Lost Roids]",),
                    ("ticksroiding", "[Ticks Roiding]",),
                    ("ticksroided", "[Ticks Roided]",),
                    ("tickroids", "[Tick-Roids]",),
                    ("avroids", "[Av. Roids]",),
                    ("galsize", "[Galaxy] Size",),
                    ("galvalue", "[Galaxy] Value",),
                    ("galscore", "[Galaxy] Score",),
                )
        %}
{% block title %}Search Results{% endblock %}
{% block sort %}{{ order }}{% endblock %}
{% block sort_growth %}{{ order }}{% endblock %}
{% block showsort %}{%for opt, name in orders if sort==opt%}<th>{{name}}</th>{%else%}{{super()}}{%endfor%}{%endblock%}
{% block page %}/search/{{params}}/page:{{p}}/{% endblock %}
{% block content %}
<form method="post" action="/search/">
<input type="hidden" value="search" name="search">
<table cellspacing="1" cellpadding="3" width="700" class="black">
    <tr class="header"><th>Planet Search</th></tr>
    <tr class="odd"><td><table width="100%" cellspacing="0" cellpadding="4">
    <tr>
        <td width="50%" valign="top" rowspan="2"><table width="100%" cellspacing="0" cellpadding="4">
            <tr class="datahigh"><th colspan="2" align="left">Planet Options</th></tr>
            <tr class="data"><td>Planet Name:</td><td align="right"><input type="text" maxlength="30" size="30" value="{{s.planet}}" name="planet"></td></tr>
            <tr class="data"><td>Ruler Name:</td><td align="right"><input type="text" maxlength="30" size="30" value="{{s.ruler}}" name="ruler"></td></tr>
            <tr class="data"><td>Race:</td><td align="right"><table cellspacing="1" cellpadding="0"><tr>
                    <td><span class="Ter">Ter</span></td><td><input type="checkbox" {{s.ter}} value="ter" name="ter"></td>
                    <td><span class="Cat">Cat</span></td><td><input type="checkbox" {{s.cat}} value="cat" name="cat"></td>
                    <td><span class="Xan">Xan</span></td><td><input type="checkbox" {{s.xan}} value="xan" name="xan"></td>
                    <td><span class="Zik">Zik</span></td><td><input type="checkbox" {{s.zik}} value="zik" name="zik"></td>
                    <td><span class="Etd">Etd</span></td><td><input type="checkbox" {{s.etd}} value="etd" name="etd"></td>
                </tr></table></td></tr>
            <tr class="data"><td>Size:</td><td align="right">Min: <input type="text" maxlength="10" size="6" value="{{s.sizemin}}" name="minsize"> Max: <input type="text" maxlength="10" size="6" value="{{s.sizemax}}" name="maxsize"></td></tr>
            <tr class="data"><td>Value:</td><td align="right">Min: <input type="text" maxlength="10" size="6" value="{{s.valuemin}}" name="minvalue"> Max: <input type="text" maxlength="10" size="6" value="{{s.valuemax}}" name="maxvalue"></td></tr>
            <tr class="data"><td>Score:</td><td align="right">Min: <input type="text" maxlength="10" size="6" value="{{s.scoremin}}" name="minscore"> Max: <input type="text" maxlength="10" size="6" value="{{s.scoremax}}" name="maxscore"></td></tr>
            <tr class="data"><td>Rank:</td><td align="right">Min: <input type="text" maxlength="10" size="6" value="{{s.rankmin}}" name="minrank"> Max: <input type="text" maxlength="10" size="6" value="{{s.rankmax}}" name="maxrank"></td></tr>
            <tr class="data"><td>Cluster:</td><td align="right">Min: <input type="text" maxlength="10" size="6" value="{{s.xmin}}" name="minx"> Max: <input type="text" maxlength="10" size="6" value="{{s.xmax}}" name="maxx"></td></tr>
            <tr class="data"><td>Ratio:</td><td align="right">Min: <input type="text" maxlength="10" size="6" value="{{s.ratiomin}}" name="minratio"> Max: <input type="text" maxlength="10" size="6" value="{{s.ratiomax}}" name="maxratio"></td></tr>
            {% if user.planet -%}
            <tr class="data"><td colspan="2" align="center">Exclude planets out of bash limit: <input type="checkbox" {{s.bash}} value="bash" name="bash"></td></tr>
            {%- endif %}
        </table></td>
        <td width="50%" valign="top"><table width="100%" cellspacing="0" cellpadding="4">
            <tr class="datahigh"><th colspan="2" align="left">Galaxy Options</th></tr>
            <tr class="data"><td>Galaxy Name:</td><td align="right"><input name="galaxy" value="{{s.galaxy}}" size="30" maxlength="30" type="text"></td></tr>
            <tr class="data"><td>Galaxy Planets:</td><td align="right">Min: <input name="minplanets" value="{{s.planetsmin}}" size="6" maxlength="10" type="text"> Max: <input name="maxplanets" value="{{s.planetsmax}}" size="6" maxlength="10" type="text"></td></tr>
            <tr class="data"><td>Galaxy Size:</td><td align="right">Min: <input name="mingalsize" value="{{s.galsizemin}}" size="6" maxlength="10" type="text"> Max: <input name="maxgalsize" value="{{s.galsizemax}}" size="6" maxlength="10" type="text"></td></tr>
            <tr class="data"><td>Galaxy Value:</td><td align="right">Min: <input name="mingalvalue" value="{{s.galvaluemin}}" size="6" maxlength="10" type="text"> Max: <input name="maxgalvalue" value="{{s.galvaluemax}}" size="6" maxlength="10" type="text"></td></tr>
            <tr class="data"><td>Galaxy Score:</td><td align="right">Min: <input name="mingalscore" value="{{s.galscoremin}}" size="6" maxlength="10" type="text"> Max: <input name="maxgalscore" value="{{s.galscoremax}}" size="6" maxlength="10" type="text"></td></tr>
            <tr class="data"><td>Galaxy Rank:</td><td align="right">Min: <input name="mingalrank" value="{{s.galrankmin}}" size="6" maxlength="10" type="text"> Max: <input name="maxgalrank" value="{{s.galrankmax}}" size="6" maxlength="10" type="text"></td></tr>
            <tr class="data"><td>Galaxy Ratio:</td><td align="right">Min: <input name="mingalratio" value="{{s.galratiomin}}" size="6" maxlength="10" type="text"> Max: <input name="maxgalratio" value="{{s.galratiomax}}" size="6" maxlength="10" type="text"></td></tr>
        </table></td>
    </tr>
    {%- if user|intel %}
    <tr>
        <td width="50%" valign="top" rowspan="2"><table width="100%" cellspacing="0" cellpadding="4">
            <tr class="datahigh"><th colspan="2" align="left">Intel Options</th></tr>
            <tr class="data"><td>Nick:</td><td align="right"><input type="text" maxlength="30" size="30" value="{{s.nick}}" name="nick"></td></tr>
            <tr class="data"><td>Alliance:</td><td align="right"><input type="text" maxlength="30" size="30" value="{{s.alliance}}" name="alliance"></td></tr>
        </table></td>
    </tr>
    {%- endif %}
    </table></td></tr>
    <tr class="datahigh"><td align="center">
        
        Order by:
        <select name="order1">
            {%- for opt, name in orders -%}
            <option value="{{opt}}"
                {%- if s.order1 == opt %} selected="selected"{% endif -%}
                >{{name}}</option>
            {%- endfor %}
        </select>
        &nbsp;
        <select name="order1o">
            {%- for order in ("asc", "desc",) -%}
            <option value="{{order}}"
                {%- if s.order1o == order %} selected="selected"{% endif -%}
                >{{order|upper}}</option>
            {%- endfor %}
        </select>
        
        then by:
        <select name="order2">
            {%- for opt, name in orders -%}
            <option value="{{opt}}"
                {%- if s.order2 == opt %} selected="selected"{% endif -%}
                >{{name}}</option>
            {%- endfor %}
        </select>
        &nbsp;
        <select name="order2o">
            {%- for order in ("asc", "desc",) -%}
            <option value="{{order}}"
                {%- if s.order2o == order %} selected="selected"{% endif -%}
                >{{order|upper}}</option>
            {%- endfor %}
        </select>
    </td></tr>
    <tr class="even"><td align="center"><input type="submit" value="Submit Query" name="submit"></td></tr>
</table>
</form>

{% if planets %}
<p>&nbsp;</p>
{{ super() }}
{% endif %}

{% endblock %}
