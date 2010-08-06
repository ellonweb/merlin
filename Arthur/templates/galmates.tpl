{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th colspan="5">
            Galmates
        </th>
    </tr>
    <tr class="header">
        <th width="100"><a href="{% url "galmates", "name" %}">User (Alias)</a></th>
        <th width="70"><a href="{% url "galmates", "sponsor" %}">Sponsor</a></th>
        <th width="60"><a href="{% url "galmates", "access" %}">Access</a></th>
        <th width="60"><a href="{% url "galmates", "planet" %}">Planet</a></th>
        <th width="200">Phone</th>
    </tr>
    {% for member, alias, sponsor, access, p, phone, pubphone, phonefriend in members %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center"><a href="{% url "dashboard", member %}">{{ member }}</a>{% if alias %} ({{ alias }}){% endif %}</td>
        <td class="center"><a href="{% url "dashboard", sponsor %}">{{ sponsor }}</a></td>
        <td class="right">{{ access }}</td>
        <td class="center">{% if p %}<a href="{% url "planet", p.x, p.y, p.z %}">{{ p.x }}:{{ p.y }}:{{ p.z }}</a>{% endif %}</td>
        <td class="left">{% if pubphone or phonefriend %}{{ phone }}{% else %}Hidden{% endif %}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
