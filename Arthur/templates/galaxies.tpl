{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="0">Galaxy listing</th>
    </tr>
    <tr class="header">
        <th colspan="5">Rank</th>
        <th colspan="6">&nbsp;</th>
        <th colspan="3">Growth</th>
    </tr>
    <tr class="header">
        <th>#</th>
        <th><a href="{% url "galaxies", "score", page|default(1) %}">Score</a></th>
        <th><a href="{% url "galaxies", "value", page|default(1) %}">Value</a></th>
        <th><a href="{% url "galaxies", "size", page|default(1) %}">Size</a></th>
        <th><a href="{% url "galaxies", "xp", page|default(1) %}">XP</a></th>
        
        <th align="right">X:Y</th>
        <th>Name</th>
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        <th>XP</th>
        
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        
    </tr>
    {% for galaxy, gh in galaxies %}
    <tr class="{% if galaxy == user.planet.galaxy %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td>{{ loop.index + offset }}</td>
        <td align="right">{{ galaxy.score_rank }}{% if gh %} {{ galaxy.score_rank|growth_rank_image(gh.score_rank) }}{% endif %}</td>
        <td align="right">{{ galaxy.value_rank }}{% if gh %} {{ galaxy.value_rank|growth_rank_image(gh.value_rank) }}{% endif %}</td>
        <td align="right">{{ galaxy.size_rank }}{% if gh %} {{ galaxy.size_rank|growth_rank_image(gh.size_rank) }}{% endif %}</td>
        <td align="right">{{ galaxy.xp_rank }}{% if gh %} {{ galaxy.xp_rank|growth_rank_image(gh.xp_rank) }}{% endif %}</td>
        
        <td align="right"><a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a></td>
        <td><a class="{% if galaxy == user.planet.galaxy %}myplanet{% else %}gray{% endif %}" href="{% url "galaxy", galaxy.x, galaxy.y %}">
                {{ galaxy.name }}
        </a></td>
        <td align="right">{{ galaxy.size|intcomma }}</td>
        <td align="right">{{ galaxy.value|intcomma }}</td>
        <td align="right">{{ galaxy.score|intcomma }}</td>
        <td align="right">{{ galaxy.xp|intcomma }}</td>
        
        <td align="right">{% if gh %}{{ galaxy.size|growth_roid(gh.size) }}{% endif %}</td>
        <td align="right">{% if gh %}{{ galaxy.value|growth(gh.value) }}{% endif %}</td>
        <td align="right">{% if gh %}{{ galaxy.score|growth(gh.score) }}{% endif %}</td>
        
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="15">Pages:{% for p in pages %} {% if p != page %}<a href="{% url "galaxies", sort, p %}">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
</table>
{% endblock %}
