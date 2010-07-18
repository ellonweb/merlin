{% extends "base.tpl" %}
{% block content %}
    <table align="center" cellpadding="3" cellspacing="1" width="600">
        <tr><td class="menuheader" colspan="7" align="center" height="15">Scans belonging to this group:</td></tr>
        <tr>
            <td class="one" nowrap="nowrap" width="2%"></td>
            <td class="one" nowrap="nowrap" width="10%"><b>Coords</b></td>
            <td class="one" nowrap="nowrap" width="10%"><b>Race</b></td>
            <td class="one" nowrap="nowrap" width="10%"><b>Size</b></td>
            <td class="one" nowrap="nowrap" width="20%"><b>Value</b></td>
            <td class="one" nowrap="nowrap" width="20%"><b>Score</b></td>
            <td class="one" nowrap="nowrap" width="30%"><b>Scans</b></td>
        </tr>
        
        {% for planet, scans in group %}
        <tr>
            <td class="two left">#{{ loop.index }}</td>
            <td class="two left"><a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
            <td class="two {{ planet.race }}">{{ planet.race }}</td>
            <td class="two right"> {{ planet.size }} </td>
            <td class="two right"> {{ planet.value|intcomma }} </td>
            <td class="two right"> {{ planet.score|intcomma }} </td>
            <td class="two left">
                {% for scan in scans %}
                    <a href="#{{ scan.pa_id }}">{{ scan.scantype }}</a>
                {% endfor %}
            </td>
        </tr>
        {% endfor %}
    </table>
    
    
    {% for scan in scans %}
    <p>&nbsp;</p>
    {% include "scans/scan.tpl" %}
    {% endfor %}
{% endblock %}
