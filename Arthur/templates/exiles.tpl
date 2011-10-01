{% from 'macros.tpl' import planetlink with context %}
{% macro exiletable(exiles) %}
<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header">
        <th>Rank</th>
        <th>Old</th>
        <th>New</th>
        <th>Current</th>
        <th colspan="8">{{caller()}}</th>
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
    {% set planet = exile.history %}
    {% set current = exile.planet %}
    {% set newiscurrent = exile.new and current.active and current.x == planet.x and current.y == planet.y and current.z == planet.z %}
    {% set newbutnotcurrent = exile.new and current.active and not newiscurrent %}
    <tr class="{%if not exile.old %}new{%elif not exile.new %}deleted{%else%}{{loop.cycle('odd', 'even')}}{%endif%}{%if not current.active%} nolongerexists{%endif%}">
        <td align="right">{%if planet.active %}{{ planet|rank("score") }}{%endif%}</td>
        
        <td align="right">
        {%if exile.old %}
            <a href="{% url "galaxy", exile.oldx, exile.oldy %}">{{ exile.oldx }}:{{ exile.oldy }}</a>
            &nbsp;{{ exile.oldz }}
        {%else%}<span class="new">New</span>{%endif%}
        </td>
        <td align="right"{%if newiscurrent%} class="datahigh"{%endif%}>
        {%if exile.new %}
            <a href="{% url "galaxy", exile.newx, exile.newy %}">{{ exile.newx }}:{{ exile.newy }}</a>
            {%if newiscurrent %}
            <a href="{% url "planet", exile.newx, exile.newy, exile.newz %}">&nbsp;{{ exile.newz }}</a>
            {%else%}
            &nbsp;{{ exile.newz }}
            {%endif%}
        {%else%}<span class="deleted">Deleted</span>{%endif%}
        </td>
        <td align="right"{%if newbutnotcurrent%} class="datahigh"{%endif%}>
        {%if newbutnotcurrent%}
            <a href="{% url "galaxy", current.x, current.y %}">{{ current.x }}:{{ current.y }}</a>
            <a href="{% url "planet", current.x, current.y, current.z %}">&nbsp;{{ current.z }}</a>
        {%endif%}
        </td>
        
        <td>{{ planet.rulername|e }}</td>
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
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="16">Pages:
            {% for p in pages %}
            {% if p != page %}<a href="{% url "exilesp", p %}">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}
            {% endfor %}
        </td>
    </tr>
    {% endif %}

</table>
{% endmacro %}
{% extends "base.tpl" %}
{% block content %}
<form onsubmit="tracker(); return false;">
    <script type="text/javascript">
        function tracker() {
            var x = parseInt(document.getElementById("x").value);
            var y = parseInt(document.getElementById("y").value);
            var z = parseInt(document.getElementById("z").value);
            var type = document.getElementById('type').value;
            if (isNaN(z))
                z = 0;
            if (isNaN(x) || isNaN(y) || isNaN(z) || x <= 0 || y <= 0 || z < 0)
                return false;
            var url = "/exiles/" + type + "/" + x + "." + y + (z ? "." + z : "") + "/";
            document.location = url;
        }
    </script>
<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="header"><th colspan="2">Planet Movement Tracker</th></tr>
    <tr class="data" height="40">
        <td class="datahigh" width="90" align="center"><i>Options:</i></td>
        <td class="odd" align="center">
            <table cellpadding="3"><tr>
                <td width="85" align="left"><select name="type" id="type">
                        <option value="through"{%if through%} selected="selected"{%endif%}>In / Out</option>
                        <option value="of"{%if not through%} selected="selected"{%endif%}>Current</option>
                    </select></td>
                <td align="right">
                    <input type="text" id="x" name="x" value="{%if planet%}{{planet.x}}{%elif galaxy%}{{galaxy.x}}{%endif%}" size="2" /> :
                    <input type="text" id="y" name="y" value="{%if planet%}{{planet.y}}{%elif galaxy%}{{galaxy.y}}{%endif%}" size="2" /> :
                    <input type="text" id="z" name="z" value="{%if planet%}{{planet.z}}{%endif%}" size="2" /></td>
                <td width="75" align="center"><input type="submit" value=" Show "></td>
                <td width="110">&nbsp;</td>
            </tr></table>
        </td>
    </tr>
</table>
</form>

<p>&nbsp;</p>

{% call exiletable(exiles) %}
    {% if through is not defined %}
    Recent
    {% elif through %}
    {% elif not through -%}
        {% if galaxy is defined %}      <a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a>
        {%- elif planet is defined %}    <a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
                                            <a {{planetlink(planet)}}>{{ planet.z }}</a>
        {%- endif %}'s
    {% endif %}
    Planet Movements
    {% if through is not defined %}
    {% elif through %} Through
        {% if galaxy is defined %}      <a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a>
        {% elif planet is defined %}    <a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
                                            <a {{planetlink(planet)}}>{{ planet.z }}</a>
        {% endif %}
    {% elif not through -%}
    {% endif %}
{% endcall %}
{% endblock %}
