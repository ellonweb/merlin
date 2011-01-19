{% from 'macros.tpl' import planetscanslink, galaxyscanslink with context %}
{% extends "scans/group.tpl" %}
{% block title %}
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetscanslink(planet)}}>{{planet.rulername}}</a>
        <i>of</i>
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetscanslink(planet)}}>{{planet.planetname}}</a>
    (<a {{galaxyscanslink(planet.galaxy)}}>{{ planet.x }}:{{ planet.y }}</a>
    <a {{planetscanslink(planet)}}>{{ planet.z }}</a>)
    <span class="{{planet.race}}">{{planet.race}}</span>
{% endblock %}
