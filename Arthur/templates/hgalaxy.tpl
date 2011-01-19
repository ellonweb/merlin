{% from 'macros.tpl' import galaxyscanslink with context %}
{% from 'history.tpl' import hgalaxy %}
{% extends "base.tpl" %}
{% block content %}
{% call hgalaxy(galaxy, history) %}
    <a class="{%if user.planet and galaxy == user.planet.galaxy %}myplanet{%else%}gray{%endif%}" {{galaxyscanslink(galaxy)}}>{{galaxy.name}}</a>
    (<a {{galaxyscanslink(galaxy)}}>{{ galaxy.x }}:{{ galaxy.y }}</a>)
        -
    {%if ticks%}Last {{ticks}} Ticks (<a href="{%url "hgalaxy", galaxy.x, galaxy.y%}">All History</a>){%else%}All History{%endif%}
{% endcall %}
{% endblock %}
