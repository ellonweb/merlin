{% load growth %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
    <tr class="datahigh">
        <th colspan="{% if page and intel %}20{% else %}{% if intel %}19{% else %}18{% endif %}{% endif %}">
            {{ title }}
        </th>
    </tr>
    <tr class="header">
        <th colspan="{% if page %}5{% else %}4{% endif %}">Rank</th>
        <th colspan="10">&nbsp;</th>
        <th colspan="3">Growth</th>
        {% if intel %}
        <th colspan="2">Intel</th>
        {% endif %}
    </tr>
    <tr class="header">
        {% if page %}<th>#</th>{% endif %}
        {% if not alliance and not galaxy %}
        <th><a href="{% url planets race|default:"all" "score" page|default:1 %}">Score</a></th>
        <th><a href="{% url planets race|default:"all" "value" page|default:1 %}">Value</a></th>
        <th><a href="{% url planets race|default:"all" "size" page|default:1 %}">Size</a></th>
        <th><a href="{% url planets race|default:"all" "xp" page|default:1 %}">XP</a></th>
        {% endif %}
        {% if galaxy %}
        <th>Score</th>
        <th>Value</th>
        <th>Size</th>
        <th>XP</th>
        {% endif %}
        {% if alliance %}
        <th><a href="{% url alliance alliance.name race|default:"all" "score" page|default:1 %}">Score</a></th>
        <th><a href="{% url alliance alliance.name race|default:"all" "value" page|default:1 %}">Value</a></th>
        <th><a href="{% url alliance alliance.name race|default:"all" "size" page|default:1 %}">Size</a></th>
        <th><a href="{% url alliance alliance.name race|default:"all" "xp" page|default:1 %}">XP</a></th>
        {% endif %}
        
        <th>X</th>
        <th>Y</th>
        <th>Z</th>
        <th>Ruler</th>
        <th>Planet</th>
        {% if not alliance and not galaxy %}
        <th><a href="{% url planets race|default:"all" "race" page|default:1 %}">Race</a></th>
        {% endif %}
        {% if galaxy %}
        <th>Race</th>
        {% endif %}
        {% if alliance %}
        <th><a href="{% url alliance alliance.name race|default:"all" "race" page|default:1 %}">Race</a></th>
        {% endif %}
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        <th>XP</th>
        
        <th>Size</th>
        <th>Value</th>
        <th>Score</th>
        
        {% if intel %}
        <th>Alliance</th>
        <th>Nick</th>
        {% endif %}
    </tr>
    {% for planet, ph, nick, alliance in planets %}
    <tr class="{% cycle 'odd' 'even' %}">
        {% if page %}<td>{{ forloop.counter|add:offset }}</td>{% endif %}
        <td align="right">{{ planet.score_rank }}{% if ph %} {{ planet.score_rank|growth_rank_image:ph.score_rank }}{% endif %}</td>
        <td align="right">{{ planet.value_rank }}{% if ph %} {{ planet.value_rank|growth_rank_image:ph.value_rank }}{% endif %}</td>
        <td align="right">{{ planet.size_rank }}{% if ph %} {{ planet.size_rank|growth_rank_image:ph.size_rank }}{% endif %}</td>
        <td align="right">{{ planet.xp_rank }}{% if ph %} {{ planet.xp_rank|growth_rank_image:ph.xp_rank }}{% endif %}</td>
        
        <td align="right"><a href="{% url galaxy planet.x planet.y %}">{{ planet.x }}</a></td>
        <td align="right"><a href="{% url galaxy planet.x planet.y %}">{{ planet.y }}</a></td>
        <td align="right"><a href="{% url planet planet.x planet.y planet.z %}">{{ planet.z }}</a></td>
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
        
        {% if intel %}
        <td>{%if alliance %}<a href="/alliance/{{ alliance }}/">{{ alliance }}</a>{% endif %}</td>
        <td>{%if nick %}{{ nick }}{% endif %}</td>
        {% endif %}
    </tr>
    {% endfor %}
    
    {% if pages %}
    <tr class="datahigh">
        {% if not alliance %}
        <td colspan="20">Pages:{% for p in pages %} {%ifnotequal p page %}<a href="{% url planets race sort p %}">{% endifnotequal %}{{ p }}{%ifnotequal p page %}</a>{% endifnotequal %}{% endfor %}</td>
        {% else %}
        <td colspan="20">Pages:{% for p in pages %} {%ifnotequal p page %}<a href="{% url alliance alliance.name race sort p %}">{% endifnotequal %}{{ p }}{%ifnotequal p page %}</a>{% endifnotequal %}{% endfor %}</td>
        {% endif %}
    </tr>
    {% endif %}
    
    {% if galaxy %}
    <tr class="header">
        <td colspan="19" height="6"/>
    </tr>
    <tr class="datahigh">
        <td align="right">{{ galaxy.score_rank }}{% if gh %} {{ galaxy.score_rank|growth_rank_image:gh.score_rank }}{% endif %}</td>
        <td align="right">{{ galaxy.value_rank }}{% if gh %} {{ galaxy.value_rank|growth_rank_image:gh.value_rank }}{% endif %}</td>
        <td align="right">{{ galaxy.size_rank }}{% if gh %} {{ galaxy.size_rank|growth_rank_image:gh.size_rank }}{% endif %}</td>
        <td align="right">{{ galaxy.xp_rank }}{% if gh %} {{ galaxy.xp_rank|growth_rank_image:gh.xp_rank }}{% endif %}</td>
        
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>
        <td align="right">{{ galaxy.size }}</td>
        <td align="right">{{ galaxy.value }}</td>
        <td align="right">{{ galaxy.score }}</td>
        <td align="right">{{ galaxy.xp }}</td>
        
        <td align="right">{% if gh %}{{ galaxy.size|growth_roid:gh.size }}{% endif %}</td>
        <td align="right">{% if gh %}{{ galaxy.value|growth:gh.value }}{% endif %}</td>
        <td align="right">{% if gh %}{{ galaxy.score|growth:gh.score }}{% endif %}</td>
        
        <td>&nbsp;</td>
        <td>&nbsp;</td>
    </tr>
    {% endif %}
    
</table>
</td>
</tr>
</table>
