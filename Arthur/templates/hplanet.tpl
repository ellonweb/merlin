{% from 'macros.tpl' import planetlink, galaxyscanslink with context %}
{% from 'history.tpl' import hplanet with context %}
{% extends "base.tpl" %}
{% block content %}
{% call hplanet(planet, history) %}
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.rulername|e}}</a>
        <i>of</i>
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.planetname}}</a>
    (<a {{galaxyscanslink(planet.galaxy)}}>{{ planet.x }}:{{ planet.y }}</a>
    <a {{planetlink(planet)}}>{{ planet.z }}</a>)
    <span class="{{planet.race}}">{{planet.race}}</span>
        -
    {%if ticks%}Last {{ticks}} Ticks (<a href="{%url "hplanet", planet.x, planet.y, planet.z%}">All History</a>){%else%}All History{%endif%}
{% endcall %}
{% endblock %}
