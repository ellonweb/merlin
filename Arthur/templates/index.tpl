{% extends "planets.tpl" %}
{% block title %}Your planet{% endblock %}
{% block content %}
<p>Welcome {{ user.name }}!</p>
{% if planets %}
{{ super() }}
{% endif %}
{% endblock %}
