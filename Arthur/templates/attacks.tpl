{% extends "base.tpl" %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}
    <table cellpadding="3" cellspacing="1" width="400" class="black">
        <tr class="datahigh"><th colspan="3">
            Open Attacks
        </th></tr>
        <tr class="header">
            <th width="15%">Attack</th>
            <th width="15%">LT</th>
            <th width="70%">Comment</th>
        </tr>
        
        {% for attack in attacks %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a href="{% url "attack", attack.id %}">{{ attack.id }}</a></td>
            <td class="center">{{ attack.landtick }}</td>
            <td> {{ attack.comment }} </td>
        </tr>
        {% endfor %}
    </table>
    
    <p>&nbsp;</p>
    
    <table cellpadding="3" cellspacing="1" width="500" class="black">
        <tr class="datahigh"><th colspan="7">
            Your current bookings
        </th></tr>
        <tr class="header">
            <th width="15%">Planet</th>
            <th width="15%">LT</th>
            <th width="15%"></th>
            <th width="10%">Race</th>
            <th width="9%">Size</th>
            <th width="18%">Value</th>
            <th width="18%">Score</th>
        </tr>
        
        {% for planet, lt in bookings %}
        <tr class="{{ loop.cycle('odd', 'even') }}">
            <td class="center"><a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a></td>
            <td class="center">{{ lt - tick }}/{{ lt }}</td>
            <td class="center"><a href="{% url "unbook" planet.x, planet.y, planet.z, lt %}">Unbook</a></td>
            <td class="{{ planet.race }}">{{ planet.race }}</td>
            <td class="right"> {{ planet.size|intcomma }} </td>
            <td class="right"> {{ planet.value|intcomma }} </td>
            <td class="right"> {{ planet.score|intcomma }} </td>
        </tr>
        {% endfor %}
    </table>
{% endblock %}
