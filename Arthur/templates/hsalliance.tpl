{% from 'macros.tpl' import alliancelink with context %}
{% from 'history.tpl' import hsalliance with context %}
{% extends "base.tpl" %}
{% block content %}
{% call hsalliance(alliance, hsummary) %}
    <a class="{%if user|intel and alliance.name|lower == name|lower %}myplanet{%else%}gray{%endif%}" {{alliancelink(alliance.name)}}>{{alliance.name}}</a>
        -
    Alliance History
{% endcall %}
{% endblock %}
