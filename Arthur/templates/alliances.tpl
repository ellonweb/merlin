{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="0">Alliance listing</th>
    </tr>
    <tr class="header">
        <th colspan="5">Rank</th>
        <th colspan="6">&nbsp;</th>
        <th class="center" colspan="4"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
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
        
        <th><a href="{% url "alliances", "avg_size_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "alliances", "avg_size_growth_pc", page|default(1) %}');">Av Size</a></th>
        <th><a href="{% url "alliances", "avg_score_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "alliances", "avg_score_growth_pc", page|default(1) %}');">Av Score</a></th>
        <th><a href="{% url "alliances", "size_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "alliances", "size_growth_pc", page|default(1) %}');">Size</a></th>
        <th><a href="{% url "alliances", "score_growth", page|default(1) %}" onclick="return linkshift(event, '{% url "alliances", "score_growth_pc", page|default(1) %}');">Score</a></th>
        
    </tr>
    {% for alliance in alliances %}
    <tr class="{% if user|intel and alliance.name == name %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td>{{ loop.index + offset }}</td>
        <td align="right">{{ alliance|rank("score") }}</td>
        <td align="right">{{ alliance|rank("size") }}</td>
        <td align="right">{{ alliance|rank("score_avg") }}</td>
        <td align="right">{{ alliance|rank("size_avg") }}</td>
        
        <td><a class="{% if user|intel and alliance.name == name %}myplanet{% else %}gray{% endif %}" href="{% url "alliance_members", alliance.name %}">
            {{ alliance.name }}
        </a></td>
        <td align="right">{{ alliance|members(True) }}</td>
        <td align="right">{{ alliance.size_avg|intcomma }}</td>
        <td align="right">{{ alliance.score_avg|intcomma }}</td>
        <td align="right">{{ alliance.size|intcomma }}</td>
        <td align="right">{{ alliance.score|intcomma }}</td>
        
        <td align="right">{{ alliance|growth("size_avg") }}</td>
        <td align="right">{{ alliance|growth("score_avg") }}</td>
        <td align="right">{{ alliance|growth("size") }}</td>
        <td align="right">{{ alliance|growth("score") }}</td>
        
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="15">Pages:{% for p in pages %} {% if p != page %}<a href="{% url "alliances", sort, p %}">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
</table>
{% endblock %}
