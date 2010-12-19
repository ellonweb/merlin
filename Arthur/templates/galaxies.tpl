{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="95%" class="black">
    <tr class="datahigh">
        <th colspan="17">Galaxy listing</th>
    </tr>
    <tr class="header">
        <th colspan="5">Rank</th>
        <th colspan="9">&nbsp;</th>
        <th class="center" colspan="3"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
    </tr>
    <tr class="header">
        <th>#</th>
        <th>Score</th>
        <th>Value</th>
        <th>Size</th>
        <th>XP</th>
        
        <th align="right">X:Y</th>
        <th>Name</th>
        <th><a href="{% url "galaxies", "size", page|default(1) %}">Size</a></th>
        <th><a href="{% url "galaxies", "value", page|default(1) %}">Value</a></th>
        <th><a href="{% url "galaxies", "real_score", page|default(1) %}">Real Score</a></th>
        <th><a href="{% url "galaxies", "score", page|default(1) %}">Score</a></th>
        <th><a href="{% url "galaxies", "planets", page|default(1) %}">Plan</a></th>
        <th><a href="{% url "galaxies", "ratio", page|default(1) %}">Ratio</a></th>
        <th><a href="{% url "galaxies", "xp", page|default(1) %}">XP</a></th>
        
        <th><a href="{% url "galaxies", "size_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "galaxies", "size_growth_pc", page|default(1) %}');">Size</a></th>
        <th><a href="{% url "galaxies", "value_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "galaxies", "value_growth_pc", page|default(1) %}');">Value</a></th>
        <th><a href="{% url "galaxies", "score_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "galaxies", "score_growth_pc", page|default(1) %}');">Score</a></th>
        
    </tr>
    {% for galaxy in galaxies %}
    <tr class="{% if galaxy == user.planet.galaxy %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td>{{ loop.index + offset }}</td>
        <td align="right">{{ galaxy|rank("score") }}</td>
        <td align="right">{{ galaxy|rank("value") }}</td>
        <td align="right">{{ galaxy|rank("size") }}</td>
        <td align="right">{{ galaxy|rank("xp") }}</td>
        
        <td align="right"><a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a></td>
        <td><a class="{% if galaxy == user.planet.galaxy %}myplanet{% else %}gray{% endif %}" href="{% url "galaxy", galaxy.x, galaxy.y %}">
                {{ galaxy.name }}
        </a></td>
        <td align="right"{%if sort=="size"%} class="datahigh"{%endif%}>{{ galaxy.size|intcomma }}</td>
        <td align="right"{%if sort=="value"%} class="datahigh"{%endif%}>{{ galaxy.value|intcomma }}</td>
        <td align="right"{%if sort=="real_score"%} class="datahigh"{%endif%}>{{ galaxy.real_score|intcomma }}</td>
        <td align="right"{%if sort=="score"%} class="datahigh"{%endif%}>{{ galaxy.score|intcomma }}</td>
        <td align="right"{%if sort=="planets"%} class="datahigh"{%endif%}>{{ galaxy|members }}</td>
        <td align="right"{%if sort=="ratio"%} class="datahigh"{%endif%}>{{ galaxy.ratio|round(1) }}</td>
        <td align="right"{%if sort=="xp"%} class="datahigh"{%endif%}>{{ galaxy.xp|intcomma }}</td>
        
        <td align="right"{%if sort and sort.startswith("size_growth")%} class="datahigh"{%endif%}>{{ galaxy|growth("size") }}</td>
        <td align="right"{%if sort and sort.startswith("value_growth")%} class="datahigh"{%endif%}>{{ galaxy|growth("value") }}</td>
        <td align="right"{%if sort and sort.startswith("score_growth")%} class="datahigh"{%endif%}>{{ galaxy|growth("score") }}</td>
        
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="17">Pages:{% for p in pages %} {% if p != page %}<a href="{% url "galaxies", sort, p %}">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
</table>
{% endblock %}
