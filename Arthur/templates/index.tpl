{% extends "base.tpl" %}
{% block content %}
<table width="100%"><tr>
    <td width="50%" valign="top" rowspan="2"><center>
        <table width="100%" cellspacing="1" cellpadding="3" class="black">
            <tr class="header">
                <th class="left" colspan="4"><a href="{% url "planet_ranks" %}">Top Planets</a></th>
                <th class="right">Size</th>
                <th class="right">Score</th>
                <th class="center" colspan="2">Growth</th>
            </tr>
             {% for planet, ph in topplanets %}
            <tr class="{{ loop.cycle('odd', 'even') }}">
        <td align="right">{{ planet.score_rank }}{% if ph %} {{ planet.score_rank|growth_rank_image(ph.score_rank) }}{% endif %}</td>
        <td align="center">
            <a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.z }}</a>
        </td>
        <td>{{ planet.planetname }}</td>
        <td class="{{ planet.race }}">{{ planet.race }}</td>
        <td align="right">{{ planet.size|intcomma }}</td>
        <td align="right">{{ planet.score|intcomma }}</td>
        <td align="right">{% if ph %}{{ planet.size|growth_roid(ph.size) }}{% endif %}</td>
        <td align="right">{% if ph %}{{ planet.score|growth(ph.score) }}{% endif %}</td>
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
                <th class="center" colspan="2">Growth</th>
            </tr>
             {% for galaxy, gh in topgalaxies %}
            <tr class="{{ loop.cycle('odd', 'even') }}">
        <td align="right">{{ galaxy.score_rank }}{% if gh %} {{ galaxy.score_rank|growth_rank_image(gh.score_rank) }}{% endif %}</td>
        <td align="center"><a href="{% url "galaxy", galaxy.x, galaxy.y %}">{{ galaxy.x }}:{{ galaxy.y }}</a></td>
        <td>{{ galaxy.name }}</td>
        <td align="right">{{ galaxy.size|intcomma }}</td>
        <td align="right">{{ galaxy.score|intcomma }}</td>
        <td align="right">{% if gh %}{{ galaxy.size|growth_roid(gh.size) }}{% endif %}</td>
        <td align="right">{% if gh %}{{ galaxy.score|growth(gh.score) }}{% endif %}</td>
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
                <th class="center" colspan="2">Growth</th>
            </tr>
             {% for alliance, ah in topalliances %}
            <tr class="{{ loop.cycle('odd', 'even') }}">
        <td align="right">{{ alliance.score_rank }}{% if ah %} {{ alliance.score_rank|growth_rank_image(ah.score_rank) }}{% endif %}</td>
        <td><a href="{% url "alliance_members", alliance.name %}" class="gray">{{ alliance.name }}</a></td>
        <td align="right">{{ alliance.members }}</td>
        <td align="right">{{ alliance.size_avg|intcomma }}</td>
        <td align="right">{{ alliance.score_avg|intcomma }}</td>
        <td align="right">{{ alliance.size|intcomma }}</td>
        <td align="right">{{ alliance.score|intcomma }}</td>
        <td align="right">{% if ah %}{{ alliance.size|growth_roid(ah.size) }}{% endif %}</td>
        <td align="right">{% if ah %}{{ alliance.score|growth(ah.score) }}{% endif %}</td>
            </tr>
            {% endfor %}
        </table>
    </center></td>
</tr></table>
{% endblock %}
