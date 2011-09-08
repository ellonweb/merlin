{% from 'macros.tpl' import planetlink, galaxyscanslink with context %}
{% from 'history.tpl' import hsplanet with context %}
{% extends "base.tpl" %}
{% block content %}
{% call hsplanet(planet, hsummary) %}
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.rulername|e}}</a>
        <i>of</i>
    <a class="{%if planet == user.planet %}myplanet{%else%}gray{%endif%}" {{planetlink(planet)}}>{{planet.planetname}}</a>
    (<a {{galaxyscanslink(planet.galaxy)}}>{{ planet.x }}:{{ planet.y }}</a>
    <a {{planetlink(planet)}}>{{ planet.z }}</a>)
    <span class="{{planet.race}}">{{planet.race}}</span>
        -
    Planet History
{% endcall %}
{% endblock %}
