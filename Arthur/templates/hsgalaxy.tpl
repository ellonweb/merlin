{% from 'macros.tpl' import galaxyscanslink with context %}
{% from 'history.tpl' import hsgalaxy with context %}
{% extends "base.tpl" %}
{% block content %}
{% call hsgalaxy(galaxy, hsummary) %}
    <a class="{%if user.planet and galaxy == user.planet.galaxy %}myplanet{%else%}gray{%endif%}" {{galaxyscanslink(galaxy)}}>{{galaxy.name}}</a>
    (<a {{galaxyscanslink(galaxy)}}>{{ galaxy.x }}:{{ galaxy.y }}</a>)
        -
    Galaxy History
{% endcall %}
{% endblock %}
