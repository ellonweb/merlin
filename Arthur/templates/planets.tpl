{% extends "base.tpl" %}
{% set cols = 16 %}
{% if page %}{% set cols = cols + 1 %}{% endif %}
{% if user|intel %}{% set cols = cols + 2 %}{% endif %}
{% if showsort %}{% set cols = cols + 1 %}{% endif %}
{% if planet and not planets %}{% set planets = ((planet, planet.intel.nick, None,),) %}{% endif %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="{{cols}}">
            {% block title %}Planet listing{% endblock %}
        </th>
    </tr>
    <tr class="header">
        {% if page %}<th></th>{% endif %}
        <th colspan="4">Rank</th>
        <th colspan="9">&nbsp;</th>
        <th class="center" colspan="3"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
        {% if user|intel %}
        {% block intel_head %}
        <th colspan="2">Intel</th>
        {% endblock %}
        {% endif %}
        {% if showsort %}
        <th></th>
        {% endif %}
    </tr>
    <tr class="header">
        {% if page %}<th>#</th>{% endif %}
        
        <th>Score</th>
        <th>Value</th>
        <th>Size</th>
        <th>XP</th>
        
        <th align="right">{% block xyz %}X:Y &nbsp;Z{% endblock %}</th>
        
        <th>Ruler</th>
        <th>Planet</th>
        {% for order, width in (("Race",0), ("Size",0,), ("Value",0,), ("Score",0,), ("Ratio",0,), ("XP",0,),) -%}
        <th width="{{ width }}">
            {%- block sort scoped -%}
                <a href="{% url "planets", race|default("all"), order|lower, page|default(1) %}">{{ order }}</a>
            {%- endblock -%}
        </th>
        {% endfor %}
        
        {% for order, link in (("Size",0,), ("Value",0,), ("Score",0,),) -%}
        <th width="{{ width }}">
            {%- block sort_growth scoped -%}
                <a href="{% url "planets", race|default("all"), order|lower + "_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "planets", race|default("all"), order|lower + "_growth_pc", page|default(1) %}');">{{ order }}</a>
            {%- endblock -%}
        </th>
        {% endfor %}
        
        {% if user|intel %}
        {% block intel_subhead %}
        <th>Alliance</th>
        <th>Nick</th>
        {% endblock %}
        {% endif %}
        
        {% if showsort %}
        {% block showsort %}
        <th>Order</th>
        {% endblock %}
        {% endif %}
    </tr>
    
    {% for planet, nick, alliance in planets %}
    <tr class="{% if planet == user.planet %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        {% if page %}<td>{{ loop.index + offset }}</td>{% endif %}
        <td align="right">{{ planet|rank("score") }}</td>
        <td align="right">{{ planet|rank("value") }}</td>
        <td align="right">{{ planet|rank("size") }}</td>
        <td align="right">{{ planet|rank("xp") }}</td>
        
        <td align="right"{%if sort=="xyz"%} class="datahigh"{%endif%}>
            <a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a href="{% url "planet", planet.x, planet.y, planet.z %}">&nbsp;{{ planet.z }}</a>
        </td>
        <td><a class="{% if planet == user.planet %}myplanet{% else %}gray{% endif %}" href="{% url "planet", planet.x, planet.y, planet.z %}">
                {{ planet.rulername }}
        </a></td>
        <td><a class="{% if planet == user.planet %}myplanet{% else %}gray{% endif %}" href="{% url "planet", planet.x, planet.y, planet.z %}">
                {{ planet.planetname }}
        </a></td>
        <td class="{%if sort=="race"%}datahigh {%endif%}{{ planet.race }}">{{ planet.race }}</td>
        <td align="right"{%if sort=="size"%} class="datahigh"{%endif%}>{{ planet|bashcap("size") }}</td>
        <td align="right"{%if sort=="value"%} class="datahigh"{%endif%}>{{ planet|bashcap("value") }}</td>
        <td align="right"{%if sort=="score"%} class="datahigh"{%endif%}>{{ planet|bashcap("score") }}</td>
        <td align="right"{%if sort=="ratio"%} class="datahigh"{%endif%}>{{ planet.ratio|round(1) }}</td>
        <td align="right"{%if sort=="xp"%} class="datahigh"{%endif%}>{{ planet.xp|intcomma }}</td>
        
        <td align="right"{%if sort and sort.startswith("size_growth")%} class="datahigh"{%endif%}>{{ planet|growth("size") }}</td>
        <td align="right"{%if sort and sort.startswith("value_growth")%} class="datahigh"{%endif%}>{{ planet|growth("value") }}</td>
        <td align="right"{%if sort and sort.startswith("score_growth")%} class="datahigh"{%endif%}>{{ planet|growth("score") }}</td>
        
        {% block intel_content scoped %}
        {% if user|intel %}
        <td>{%if alliance %}<a href="{% url "alliance_members", alliance %}">{{ alliance }}</a>{% endif %}</td>
        <td>{%if nick %}{{ nick }}{% endif %}</td>
        {% endif %}
        {% endblock %}
        
        {% if showsort %}
        <td align="right" class="datahigh">
        {% if sort in ("totalroundroids","totallostroids","ticksroiding","ticksroided","tickroids",) %}
        {{planet|attr(sort)|intcomma}}
        {% elif sort in ("avroids",) %}
        {{planet|attr(sort)|round|int|intcomma}}
        {% elif sort[3:] in ("score","value","size","xp",) %}
        {{planet.galaxy|attr(sort[3:])|intcomma}}
        {% elif sort[3:] in ("ratio",) %}
        {{planet.galaxy|attr(sort[3:])|round(1)|intcomma}}
        {% elif sort == "planets" %}
        {{planet.galaxy.members}}
        {% endif %}
        </td>
        {% endif %}
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="{{cols}}">Pages:{% for p in pages %} {% if p != page %}<a href="
            {%- block page scoped %}{% url "planets", race, sort p %}{% endblock -%}
            ">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
    {% if galaxy %}
    <tr class="header">
        <td colspan="{{cols}}" height="6"/>
    </tr>
    <tr class="datahigh">
        <td align="right">{{ galaxy|rank("score") }}</td>
        <td align="right">{{ galaxy|rank("value") }}</td>
        <td align="right">{{ galaxy|rank("size") }}</td>
        <td align="right">{{ galaxy|rank("xp") }}</td>
        
        <td align="right">{{ galaxy|members }}</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td align="right">{{ galaxy.size|intcomma }}</td>
        <td align="right">{{ galaxy.value|intcomma }}</td>
        <td align="right">{{ galaxy.score|intcomma }}</td>
        <td align="right">{{ galaxy.ratio|round(1) }}</td>
        <td align="right">{{ galaxy.xp|intcomma }}</td>
        
        <td align="right">{{ galaxy|growth("size") }}</td>
        <td align="right">{{ galaxy|growth("value") }}</td>
        <td align="right">{{ galaxy|growth("score") }}</td>
        
        {% if user|intel %}
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        {% endif %}
    </tr>
    {% endif %}
    
</table>
{% endblock %}
