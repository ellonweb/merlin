{% extends "base.tpl" %}
{% block content %}
<table cellspacing="1" cellpadding="3" width="100%" class="black">
    <tr class="datahigh">
        <th colspan="5">
            Galmates
        </th>
    </tr>
    <tr class="header">
        <th width="100"><a href="{% url "galmates", "name" %}">User (Alias)</a></th>
        <th width="100"><a href="{% url "galmates", "sponsor" %}">Sponsor</a></th>
        <th width="100"><a href="{% url "galmates", "access" %}">Access</a></th>
        <th width="100"><a href="{% url "galmates", "planet" %}">Planet</a></th>
        <th width="100">Phone</th>
    </tr>
    {% for member, alias, sponsor, access, planet, phone, pubphone, phonefriend in members %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td>{{ member }}{% if alias %} ({{ alias }}){% endif %}</td>
        <td>{{ sponsor }}</td>
        <td>{{ access }}</td>
        <td>{% if planet %}{{ planet.x }}:{{ planet.y }}:{{ planet.z }}{% endif %}</td>
        <td>{% if pubphone or phonefriend %}{{ phone }}{% else %}Hidden{% endif %}</td>
    </tr>
    {% endfor %}
</table>
{% endblock %}
