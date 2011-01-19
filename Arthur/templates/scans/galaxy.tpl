{% from 'macros.tpl' import galaxyscanslink with context %}
{% extends "scans/group.tpl" %}
{% block title %}
    <a class="{%if user.planet and galaxy == user.planet.galaxy %}myplanet{%else%}gray{%endif%}" {{galaxyscanslink(galaxy)}}>{{galaxy.name}}</a>
    (<a {{galaxyscanslink(galaxy)}}>{{ galaxy.x }}:{{ galaxy.y }}</a>)
        -
    Real Score: {{galaxy.real_score|intcomma}} ({{galaxy|rank("score")}})
{% endblock %}
