{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th colspan="10"><a href="{% url "alliance_members", alliance.name %}">{{ alliance.name }}</a> History, based on present intel of {{ members }} ({{ alliance.members }}) members</th>
    </tr>
    <tr class="header">
        <th width="50">Tick</th>
        
        <th width="60">Avg Size</th>
        <th width="60">Size</th>
        <th width="60">Size Diff</th>
        
        <th width="90">Avg Value</th>
        <th width="90">Value</th>
        <th width="90">Value Diff</th>
        <th width="90">Score Diff</th>
        
        <th width="75">T10 Value</th>
        <th width="75">T100 Value</th>
    </tr>
    {% for tick, members, size, value, avgsize, avgvalue, sizediff, valuediff, scorediff, t10v, t100v, sizerank, valuerank in history %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td align="right">{{ tick }}</td>
        
        <td align="right">{{ avgsize|intcomma }}</td>
        <td align="right" title="Rank {{ sizerank }}">{{ size|intcomma }}</td>
        <td align="right">{{ sizediff|change|intcomma }}</td>
        
        <td align="right">{{ avgvalue|intcomma }}</td>
        <td align="right" title="Rank {{ valuerank }}">{{ value|intcomma }}</td>
        <td align="right">{{ valuediff|change|intcomma }}</td>
        <td align="right">{{ scorediff|change|intcomma }}</td>
        
        <td align="right">{{ t10v }}</td>
        <td align="right">{{ t100v }}</td>
    </tr>
    {% endfor %}
    
</table>
{% endblock %}
