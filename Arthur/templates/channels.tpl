{% extends "base.tpl" %}
{% block content %}
{% for level, channels in accesslist %}
<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th colspan="3">
            {{ level|capitalize }} channels
        </th>
    </tr>
    <tr class="header">
        <th width="100"><a href="{% url "channels", "name" %}">Name</a></th>
        <th width="75"><a href="{% url "channels", "userlevel" %}">User Level</a></th>
        <th width="75"><a href="{% url "channels", "maxlevel" %}">Max Level</a></th>
    </tr>
    {% for name, userlevel, maxlevel in channels %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center">{{ name }}</td>
        <td class="right">{{ userlevel }}</td>
        <td class="right">{{ maxlevel }}</td>
    </tr>
    {% endfor %}
</table>
{% if not loop.last %}<p>&nbsp;</p>{% endif %}
{% endfor %}
{% endblock %}
