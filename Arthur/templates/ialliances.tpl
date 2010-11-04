{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="17">Alliance listing (intel)</th>
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
    {% for aname, members, size, value, score, asize, avalue, ascore, t10s, t50s, t100s, t200s, t10v, t50v, t100v, t200v, imembers, id in alliances %}
    <tr class="{% if user|intel and aname == name %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td>{{ loop.index + offset }}</td>
        <td><a class="{% if user|intel and aname == name %}myplanet{% else %}gray{% endif %}" href="{% url "alliance_members", aname %}">
            {{ aname }}
        </a></td>
        <td align="right"{%if sort=="members"%} class="datahigh"{%endif%}>{{ imembers }} ({{ members }})</td>
        
        <td align="right"{%if sort=="avg_size"%} class="datahigh"{%endif%}>{{ asize|intcomma }}</td>
        <td align="right"{%if sort=="avg_value"%} class="datahigh"{%endif%}>{{ avalue|intcomma }}</td>
        <td align="right"{%if sort=="avg_score"%} class="datahigh"{%endif%}>{{ ascore|intcomma }}</td>
        
        <td align="right"{%if sort=="size"%} class="datahigh"{%endif%}>{{ size|intcomma }}</td>
        <td align="right"{%if sort=="value"%} class="datahigh"{%endif%}>{{ value|intcomma }}</td>
        <td align="right"{%if sort=="score"%} class="datahigh"{%endif%}>{{ score|intcomma }}</td>
        
        <td align="right"{%if sort=="t10s"%} class="datahigh"{%endif%}>{{ t10s }}</td>
        <td align="right"{%if sort=="t50s"%} class="datahigh"{%endif%}>{{ t50s }}</td>
        <td align="right"{%if sort=="t100s"%} class="datahigh"{%endif%}>{{ t100s }}</td>
        <td align="right"{%if sort=="t200s"%} class="datahigh"{%endif%}>{{ t200s }}</td>
        
        <td align="right"{%if sort=="t10v"%} class="datahigh"{%endif%}>{{ t10v }}</td>
        <td align="right"{%if sort=="t50v"%} class="datahigh"{%endif%}>{{ t50v }}</td>
        <td align="right"{%if sort=="t100v"%} class="datahigh"{%endif%}>{{ t100v }}</td>
        <td align="right"{%if sort=="t200v"%} class="datahigh"{%endif%}>{{ t200v }}</td>
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        <td colspan="17">Pages:{% for p in pages %} {% if p != page %}<a href="{% url "alliances", sort, p %}">{% endif %}{{ p }}{% if p != page %}</a>{% endif %}{% endfor %}</td>
    </tr>
    {% endif %}
    
</table>
{% endblock %}
