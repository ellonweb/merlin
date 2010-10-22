{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="0">Alliance listing</th>
    </tr>
    <tr class="header">
        <th colspan="5">Rank</th>
        <th colspan="6">&nbsp;</th>
        <th colspan="4">Growth</th>
    </tr>
    <tr class="header">
        <th>#</th>
        <th><a href="{% url "alliances", "score", page|default(1) %}">Score</a></th>
        <th><a href="{% url "alliances", "size", page|default(1) %}">Size</a></th>
        <th><a href="{% url "alliances", "avg_score", page|default(1) %}">Av Score</a></th>
        <th><a href="{% url "alliances", "avg_size", page|default(1) %}">Av Size</a></th>
        
        <th>Name</th>
        <th><a href="{% url "alliances", "members", page|default(1) %}">Members</a></th>
        <th>Av Size</th>
        <th>Av Score</th>
        <th>Size</th>
        <th>Score</th>
        
        <th>Av Size</th>
        <th>Av Score</th>
        <th>Size</th>
        <th>Score</th>
        
    </tr>
    {% for alliance, ah in alliances %}
    <tr class="{% if user|intel and alliance.name == name %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td>{{ loop.index + offset }}</td>
        <td align="right">{{ alliance.score_rank }}{% if ah %} {{ alliance.score_rank|growth_rank_image(ah.score_rank) }}{% endif %}</td>
        <td align="right">{{ alliance.size_rank }}{% if ah %} {{ alliance.size_rank|growth_rank_image(ah.size_rank) }}{% endif %}</td>
        <td align="right">{{ alliance.score_avg_rank }}{% if ah %} {{ alliance.score_avg_rank|growth_rank_image(ah.score_avg_rank) }}{% endif %}</td>
        <td align="right">{{ alliance.size_avg_rank }}{% if ah %} {{ alliance.size_avg_rank|growth_rank_image(ah.size_avg_rank) }}{% endif %}</td>
        
        <td><a class="{% if user|intel and alliance.name == name %}myplanet{% else %}gray{% endif %}" href="{% url "alliance_members", alliance.name %}">
            {{ alliance.name }}
        </a></td>
        <td align="right">{% if ah %}{{ alliance.members|growth_members(ah.members, True) }}{% else %}{{ alliance.members }}{% endif %}</td>
        <td align="right">{{ alliance.size_avg|intcomma }}</td>
        <td align="right">{{ alliance.score_avg|intcomma }}</td>
        <td align="right">{{ alliance.size|intcomma }}</td>
        <td align="right">{{ alliance.score|intcomma }}</td>
        
        <td align="right">{% if ah %}{{ alliance.size_avg|growth_roid(ah.size_avg) }}{% endif %}</td>
        <td align="right">{% if ah %}{{ alliance.score_avg|growth(ah.score_avg) }}{% endif %}</td>
        <td align="right">{% if ah %}{{ alliance.size|growth_roid(ah.size) }}{% endif %}</td>
        <td align="right">{% if ah %}{{ alliance.score|growth(ah.score) }}{% endif %}</td>
        
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="15">Pages:{% for p in pages %} {% if p != page %}<a href="{% url "alliances", sort, p %}">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
</table>
{% endblock %}
