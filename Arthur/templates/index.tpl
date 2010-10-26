{% extends "base.tpl" %}
{% block content %}
<table width="100%"><tr>
    <td width="50%" valign="top" rowspan="2"><center>
        <table width="100%" cellspacing="1" cellpadding="3" class="black">
            <tr class="header">
                <th class="left" colspan="4"><a href="{% url "planet_ranks" %}">Top Planets</a></th>
                <th class="right">Size</th>
                <th class="right">Score</th>
                <th class="center" colspan="2"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
            </tr>
{% if user.planet and user.planet.score_rank > 20 %}{% do topplanets.append(user.planet) %}{% endif %}
            {% for planet in topplanets %}
{% if loop.index > 20 %}<tr class="header"><td colspan="0"></td></tr>{% endif %}
    <tr class="{% if planet == user.planet %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td align="right">{{ planet|rank("score") }}</td>
        <td align="right">
            <a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a href="{% url "planet", planet.x, planet.y, planet.z %}">&nbsp;{{ planet.z }}</a>
        </td>
        <td><a class="{% if planet == user.planet %}myplanet{% else %}gray{% endif %}" href="{% url "planet", planet.x, planet.y, planet.z %}">
                {{ planet.planetname }}
        </a></td>
        <td class="{{ planet.race }}">{{ planet.race }}</td>
        <td align="right">{{ planet.size|intcomma }}</td>
        <td align="right">{{ planet.score|intcomma }}</td>
        <td align="right">{{ planet|growth("size") }}</td>
        <td align="right">{{ planet|growth("score") }}</td>
            </tr>
            {% endfor %}
        </table>
    </center></td>
    
    <td width="50%" valign="top"><center>
        <table width="100%" cellspacing="1" cellpadding="3" class="black">
            <tr class="header">
                <th class="left" colspan="3"><a href="{% url "galaxy_ranks" %}">Top Galaxies</a></th>
                <th class="right">Size</th>
                <th class="right">Score</th>
                <th class="center" colspan="2"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
            </tr>
{% if user.planet.galaxy and user.planet.galaxy.score_rank > 10 %}{% do topgalaxies.append(user.planet.galaxy) %}{% endif %}
            {% for galaxy in topgalaxies %}
{% if loop.index > 10 %}<tr class="header"><td colspan="0"></td></tr>{% endif %}
    <tr class="{% if galaxy == user.planet.galaxy %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td align="right">{{ galaxy|rank("score") }}</td>
        <td align="right"><a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a></td>
        <td><a class="{% if galaxy == user.planet.galaxy %}myplanet{% else %}gray{% endif %}" href="{% url "galaxy", galaxy.x, galaxy.y %}">
                {{ galaxy.name }}
        </a></td>
        <td align="right">{{ galaxy.size|intcomma }}</td>
        <td align="right">{{ galaxy.score|intcomma }}</td>
        <td align="right">{{ galaxy|growth("size") }}</td>
        <td align="right">{{ galaxy|growth("score") }}</td>
            </tr>
            {% endfor %}
        </table>
    </center></td>
    
    </tr>
    <tr>
    <td width="50%" valign="bottom"><center>
        <table width="100%" cellspacing="1" cellpadding="3" class="black">
            <tr class="header">
                <th class="left" colspan="2"><a href="{% url "alliance_ranks" %}">Top Alliances</a></th>
                <th class="center">M.</th>
                <th class="right">Av. Size</th>
                <th class="right">Av. Score</th>
                <th class="right">Size</th>
                <th class="right">Score</th>
                <th class="center" colspan="2"><a href="" onclick="toggleGrowth();return false;">Growth</a></th>
            </tr>
            {% for alliance in topalliances %}
    <tr class="{% if user|intel and alliance.name == name %}datahigh{% else %}{{ loop.cycle('odd', 'even') }}{% endif %}">
        <td align="right">{{ alliance|rank("score") }}</td>
        <td><a class="{% if user|intel and alliance.name == name %}myplanet{% else %}gray{% endif %}" href="{% url "alliance_members", alliance.name %}">
            {{ alliance.name }}
        </a></td>
        <td align="right">{{ alliance|members }}</td>
        <td align="right">{{ alliance.size_avg|intcomma }}</td>
        <td align="right">{{ alliance.score_avg|intcomma }}</td>
        <td align="right">{{ alliance.size|intcomma }}</td>
        <td align="right">{{ alliance.score|intcomma }}</td>
        <td align="right">{{ alliance|growth("size") }}</td>
        <td align="right">{{ alliance|growth("score") }}</td>
            </tr>
            {% endfor %}
        </table>
    </center></td>
</tr></table>
{% endblock %}
