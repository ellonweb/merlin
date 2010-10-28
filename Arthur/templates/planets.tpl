{% extends "base.tpl" %}
{% if planet and not planets %}{% set planets = ((planet, planet.intel.nick, None,),) %}{% endif %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="0">
            {% block title %}Planet listing{% endblock %}
        </th>
    </tr>
    <tr class="header">
        {% if page %}<th></th>{% endif %}
        <th colspan="4">Rank</th>
        <th colspan="8">&nbsp;</th>
        <th class="center" colspan="3"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
        {% block intel_head %}
        {% if user|intel %}
        <th colspan="2">Intel</th>
        {% endif %}
        {% endblock %}
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
        {% for order, width in (("Race",0), ("Size",0,), ("Value",0,), ("Score",0,), ("XP",0,),) -%}
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
        
        {% block intel_subhead %}
        {% if user|intel %}
        <th>Alliance</th>
        <th>Nick</th>
        {% endif %}
        {% endblock %}
    </tr>
    
    {% for planet, nick, alliance in planets %}
    <tr class="{% if planet == user.planet %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        {% if page %}<td>{{ loop.index + offset }}</td>{% endif %}
        <td align="right">{{ planet|rank("score") }}</td>
        <td align="right">{{ planet|rank("value") }}</td>
        <td align="right">{{ planet|rank("size") }}</td>
        <td align="right">{{ planet|rank("xp") }}</td>
        
        <td align="right">
            <a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a href="{% url "planet", planet.x, planet.y, planet.z %}">&nbsp;{{ planet.z }}</a>
        </td>
        <td><a class="{% if planet == user.planet %}myplanet{% else %}gray{% endif %}" href="{% url "planet", planet.x, planet.y, planet.z %}">
                {{ planet.rulername }}
        </a></td>
        <td><a class="{% if planet == user.planet %}myplanet{% else %}gray{% endif %}" href="{% url "planet", planet.x, planet.y, planet.z %}">
                {{ planet.planetname }}
        </a></td>
        <td class="{{ planet.race }}">{{ planet.race }}</td>
        <td align="right">{{ planet.size|intcomma }}</td>
        <td align="right">{{ planet.value|intcomma }}</td>
        <td align="right">{{ planet.score|intcomma }}</td>
        <td align="right">{{ planet.xp|intcomma }}</td>
        
        <td align="right">{{ planet|growth("size") }}</td>
        <td align="right">{{ planet|growth("value") }}</td>
        <td align="right">{{ planet|growth("score") }}</td>
        
        {% block intel_content scoped %}
        {% if user|intel %}
        <td>{%if alliance %}<a href="{% url "alliance_members", alliance %}">{{ alliance }}</a>{% endif %}</td>
        <td>{%if nick %}{{ nick }}{% endif %}</td>
        {% endif %}
        {% endblock %}
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="20">Pages:{% for p in pages %} {% if p != page %}<a href="
            {%- block page scoped %}{% url "planets", race, sort p %}{% endblock -%}
            ">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
    {% if galaxy %}
    <tr class="header">
        <td colspan="19" height="6"/>
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
