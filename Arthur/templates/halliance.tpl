{% from 'macros.tpl' import alliancelink with context %}
{% from 'history.tpl' import halliance %}
{% extends "base.tpl" %}
{% block content %}
{% call halliance(alliance, history) %}
    <a class="{%if user|intel and alliance.name == name %}myplanet{%else%}gray{%endif%}" {{alliancelink(alliance)}}>{{alliance.name}}</a>
        -
    {%if ticks%}Last {{ticks}} Ticks (<a href="{%url "halliance", alliance.name%}">All History</a>){%else%}All History{%endif%}
{% endcall %}
{% endblock %}
