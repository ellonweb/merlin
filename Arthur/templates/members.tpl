{% extends "base.tpl" %}
{% block content %}
{% for level, members in accesslist %}
<table cellspacing="1" cellpadding="3" class="black">
    <tr class="datahigh">
        <th colspan="7">
            {{ level|capitalize }}s
        </th>
    </tr>
    <tr class="header">
        <th width="100"><a href="{% url "members", "name" %}">User (Alias)</a></th>
        <th width="70"><a href="{% url "members", "sponsor" %}">Sponsor</a></th>
        <th width="60"><a href="{% url "members", "access" %}">Access</a></th>
        <th width="70"><a href="{% url "members", "carebears" %}">CareBears</a></th>
        <th width="60"><a href="{% url "members", "planet" %}">Planet</a></th>
        <th width="80"><a href="{% url "members", "defage" %}">MyDef Age</a></th>
        <th width="200">Phone</th>
    </tr>
    {% for member, alias, sponsor, access, carebears, p, fleetupdated, phone, pubphone, phonefriend in members %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center"><a href="{% url "dashboard", member %}">{{ member }}</a>{% if alias %} ({{ alias }}){% endif %}</td>
        <td class="center"><a href="{% url "dashboard", sponsor %}">{{ sponsor }}</a></td>
        <td class="right">{{ access }}</td>
        <td class="right">{{ carebears }}</td>
        <td class="center">{% if p %}<a href="{% url "planet", p.x, p.y, p.z %}">{{ p.x }}:{{ p.y }}:{{ p.z }}</a>{% endif %}</td>
        <td class="right">{% if fleetupdated %}{{ tick - fleetupdated }} ticks{% endif %}</td>
        <td class="left">{% if pubphone or phonefriend %}{{ phone }}{% else %}Hidden{% endif %}</td>
    </tr>
    {% endfor %}
</table>
{% if not loop.last %}<p>&nbsp;</p>{% endif %}
{% endfor %}
{% endblock %}
