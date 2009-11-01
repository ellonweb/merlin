{% extends "base.tpl" %}
{% block content %}
{% load growth %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="17">{{ title }}</th>
    </tr>
    <tr class="header">
        <th colspan="9">&nbsp;</th>
        <th colspan="4">Score</th>
        <th colspan="4">Value</th>
    </tr>
    <tr class="header">
        <th>#</th>
        <th>Alliance</th>
        <th><a href="{% url ialliances "members" page|default:1 %}">Members</a></th>
        
        <th><a href="{% url ialliances "avg_size" page|default:1 %}">Av Size</a></th>
        <th><a href="{% url ialliances "avg_value" page|default:1 %}">Av Value</a></th>
        <th><a href="{% url ialliances "avg_score" page|default:1 %}">Av Score</a></th>
        
        <th><a href="{% url ialliances "size" page|default:1 %}">Size</a></th>
        <th><a href="{% url ialliances "value" page|default:1 %}">Value</a></th>
        <th><a href="{% url ialliances "score" page|default:1 %}">Score</a></th>
        
        <th><a href="{% url ialliances "t10s" page|default:1 %}">Top 10</a></th>
        <th><a href="{% url ialliances "t50s" page|default:1 %}">Top 50</a></th>
        <th><a href="{% url ialliances "t100s" page|default:1 %}">Top 100</a></th>
        <th><a href="{% url ialliances "t200s" page|default:1 %}">Top 200</a></th>
        
        <th><a href="{% url ialliances "t10v" page|default:1 %}">Top 10</a></th>
        <th><a href="{% url ialliances "t50v" page|default:1 %}">Top 50</a></th>
        <th><a href="{% url ialliances "t100v" page|default:1 %}">Top 100</a></th>
        <th><a href="{% url ialliances "t200v" page|default:1 %}">Top 200</a></th>
    </tr>
    {% for size, value, score, asize, avalue, ascore, t10s, t50s, t100s, t200s, t10v, t50v, t100v, t200v, members, name in alliances %}
    <tr class="{% cycle 'odd' 'even' %}">
        <td>{{ forloop.counter|add:offset }}</td>
        <td><a href="/alliance/{{ name }}/" class="gray">{{ name }}</a></td>
        <td align="right">{{ members }}</td>
        
        <td align="right">{{ asize }}</td>
        <td align="right">{{ avalue }}</td>
        <td align="right">{{ ascore }}</td>
        
        <td align="right">{{ size }}</td>
        <td align="right">{{ value }}</td>
        <td align="right">{{ score }}</td>
        
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
        <td colspan="17">Pages:{% for p in pages %} {%ifnotequal p page %}<a href="{% url alliances sort p %}">{% endifnotequal %}{{ p }}{%ifnotequal p page %}</a>{% endifnotequal %}{% endfor %}</td>
    </tr>
    {% endif %}
    
</table>
</td>
</tr>
</table>
{% endblock %}
