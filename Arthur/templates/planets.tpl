{% extends "base.tpl" %}
{% load growth %}
{% block content %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="20">Planet listing</th>
    </tr>
    <tr class="header">
        <th colspan="5">Rank</th>
        <th colspan="10">&nbsp;</th>
        <th colspan="3">Growth</th>
        <th colspan="2">Intel</th>
    </tr>
    <tr class="header">
        <th>#</th>
        <th><a href="{% url planets race "score" page %}">Score</a></th>
        <th><a href="{% url planets race "value" page %}">Value</a></th>
        <th><a href="{% url planets race "size" page %}">Size</a></th>
        <th><a href="{% url planets race "xp" page %}">XP</a></th>
        
        <th>X</th>
        <th>Y</th>
        <th>Z</th>
        <th>Ruler</th>
        <th>Planet</th>
        <th>Race</th>
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        <th>XP</th>
        
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        
        <th>Alliance</th>
        <th>Nick</th>
    </tr>
    {% for planet, ph, nick, alliance in planets %}
    <tr class="{% cycle 'odd' 'even' %}">
        <td>{{ forloop.counter|add:offset }}</td>
        <td align="right">{{ planet.score_rank }}{% if ph %} {{ planet.score_rank|growth_rank_image:ph.score_rank }}{% endif %}</td>
        <td align="right">{{ planet.value_rank }}{% if ph %} {{ planet.value_rank|growth_rank_image:ph.value_rank }}{% endif %}</td>
        <td align="right">{{ planet.size_rank }}{% if ph %} {{ planet.size_rank|growth_rank_image:ph.size_rank }}{% endif %}</td>
        <td align="right">{{ planet.xp_rank }}{% if ph %} {{ planet.xp_rank|growth_rank_image:ph.xp_rank }}{% endif %}</td>
        
        <td align="right">{{ planet.x }}</td>
        <td align="right">{{ planet.y }}</td>
        <td align="right">{{ planet.z }}</td>
        <td>{{ planet.rulername }}</td>
        <td>{{ planet.planetname }}</td>
        <td class="{{ planet.race }}">{{ planet.race }}</td>
        <td align="right">{{ planet.size }}</td>
        <td align="right">{{ planet.value }}</td>
        <td align="right">{{ planet.score }}</td>
        <td align="right">{{ planet.xp }}</td>
        
        <td align="right">{% if ph %}{{ planet.size|growth_roid:ph.size }}{% endif %}</td>
        <td align="right">{% if ph %}{{ planet.value|growth:ph.value }}{% endif %}</td>
        <td align="right">{% if ph %}{{ planet.score|growth:ph.score }}{% endif %}</td>
        
        <td>{%if alliance %}{{ alliance }}{% endif %}</td>
        <td>{%if nick %}{{ nick }}{% endif %}</td>
    </tr>
    {% endfor %}
    <tr class="datahigh">
        <td colspan="20">Pages:{% for p in pages %} {%ifnotequal p page %}<a href="{% url planets race sort p %}">{% endifnotequal %}{{ p }}{%ifnotequal p page %}</a>{% endifnotequal %}{% endfor %}</td>
    </tr>

</table>
</td>
</tr>
</table>
{% endblock %}
