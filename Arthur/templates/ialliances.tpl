{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="0">Alliance listing (intel)</th>
    </tr>
    <tr class="header">
        <th colspan="9">&nbsp;</th>
        <th colspan="4">Score</th>
        <th colspan="4">Value</th>
    </tr>
    <tr class="header">
        <th>#</th>
        <th>Alliance</th>
        <th><a href="{% url "ialliances", "members", page|default(1) %}">Members</a></th>
        
        <th><a href="{% url "ialliances", "avg_size", page|default(1) %}">Av Size</a></th>
        <th><a href="{% url "ialliances", "avg_value", page|default(1) %}">Av Value</a></th>
        <th><a href="{% url "ialliances", "avg_score", page|default(1) %}">Av Score</a></th>
        
        <th><a href="{% url "ialliances", "size", page|default(1) %}">Size</a></th>
        <th><a href="{% url "ialliances", "value", page|default(1) %}">Value</a></th>
        <th><a href="{% url "ialliances", "score", page|default(1) %}">Score</a></th>
        
        <th><a href="{% url "ialliances", "t10s", page|default(1) %}">Top 10</a></th>
        <th><a href="{% url "ialliances", "t50s", page|default(1) %}">Top 50</a></th>
        <th><a href="{% url "ialliances", "t100s", page|default(1) %}">Top 100</a></th>
        <th><a href="{% url "ialliances", "t200s", page|default(1) %}">Top 200</a></th>
        
        <th><a href="{% url "ialliances", "t10v", page|default(1) %}">Top 10</a></th>
        <th><a href="{% url "ialliances", "t50v", page|default(1) %}">Top 50</a></th>
        <th><a href="{% url "ialliances", "t100v", page|default(1) %}">Top 100</a></th>
        <th><a href="{% url "ialliances", "t200v", page|default(1) %}">Top 200</a></th>
    </tr>
    {% for name, members, size, value, score, asize, avalue, ascore, t10s, t50s, t100s, t200s, t10v, t50v, t100v, t200v, imembers, id in alliances %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td>{{ loop.index + offset }}</td>
        <td><a href="{% url "alliance_members", name %}" class="gray">{{ name }}</a></td>
        <td align="right">{{ imembers }} ({{ members }})</td>
        
        <td align="right">{{ asize|intcomma }}</td>
        <td align="right">{{ avalue|intcomma }}</td>
        <td align="right">{{ ascore|intcomma }}</td>
        
        <td align="right">{{ size|intcomma }}</td>
        <td align="right">{{ value|intcomma }}</td>
        <td align="right">{{ score|intcomma }}</td>
        
        <td align="right">{{ t10s }}</td>
        <td align="right">{{ t50s }}</td>
        <td align="right">{{ t100s }}</td>
        <td align="right">{{ t200s }}</td>
        
        <td align="right">{{ t10v }}</td>
        <td align="right">{{ t50v }}</td>
        <td align="right">{{ t100v }}</td>
        <td align="right">{{ t200v }}</td>
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="17">Pages:{% for p in pages %} {% if p != page %}<a href="{% url "alliances", sort, p %}">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
</table>
{% endblock %}
