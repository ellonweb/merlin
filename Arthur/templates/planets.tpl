{% extends "base.tpl" %}
{% if planet and not planets %}{% set planets = ((planet, ph, planet.intel.nick, None,),) %}{% endif %}
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
        <th colspan="3">Growth</th>
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
        
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        
        {% block intel_subhead %}
        {% if user|intel %}
        <th>Alliance</th>
        <th>Nick</th>
        {% endif %}
        {% endblock %}
    </tr>
    
    {% for planet, ph, nick, alliance in planets %}
    <tr class="{% if planet == user.planet %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        {% if page %}<td>{{ loop.index + offset }}</td>{% endif %}
        <td align="right">{{ planet.score_rank }}{% if ph %} {{ planet.score_rank|growth_rank_image(ph.score_rank) }}{% endif %}</td>
        <td align="right">{{ planet.value_rank }}{% if ph %} {{ planet.value_rank|growth_rank_image(ph.value_rank) }}{% endif %}</td>
        <td align="right">{{ planet.size_rank }}{% if ph %} {{ planet.size_rank|growth_rank_image(ph.size_rank) }}{% endif %}</td>
        <td align="right">{{ planet.xp_rank }}{% if ph %} {{ planet.xp_rank|growth_rank_image(ph.xp_rank) }}{% endif %}</td>
        
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
        
        <td align="right">{% if ph %}{{ planet.size|growth_roid(ph.size) }}{% endif %}</td>
        <td align="right">{% if ph %}{{ planet.value|growth(ph.value) }}{% endif %}</td>
        <td align="right">{% if ph %}{{ planet.score|growth(ph.score) }}{% endif %}</td>
        
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
        <td align="right">{{ galaxy.score_rank }}{% if gh %} {{ galaxy.score_rank|growth_rank_image(gh.score_rank) }}{% endif %}</td>
        <td align="right">{{ galaxy.value_rank }}{% if gh %} {{ galaxy.value_rank|growth_rank_image(gh.value_rank) }}{% endif %}</td>
        <td align="right">{{ galaxy.size_rank }}{% if gh %} {{ galaxy.size_rank|growth_rank_image(gh.size_rank) }}{% endif %}</td>
        <td align="right">{{ galaxy.xp_rank }}{% if gh %} {{ galaxy.xp_rank|growth_rank_image(gh.xp_rank) }}{% endif %}</td>
        
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td align="right">{{ galaxy.size|intcomma }}</td>
        <td align="right">{{ galaxy.value|intcomma }}</td>
        <td align="right">{{ galaxy.score|intcomma }}</td>
        <td align="right">{{ galaxy.xp|intcomma }}</td>
        
        <td align="right">{% if gh %}{{ galaxy.size|growth_roid(gh.size) }}{% endif %}</td>
        <td align="right">{% if gh %}{{ galaxy.value|growth(gh.value) }}{% endif %}</td>
        <td align="right">{% if gh %}{{ galaxy.score|growth(gh.score) }}{% endif %}</td>
        
        {% if user|intel %}
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        {% endif %}
    </tr>
    {% endif %}
    
</table>
{% endblock %}
