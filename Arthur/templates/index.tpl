{% extends "planet_intelintitle.tpl" %}
{% block title %}Your planet{% endblock %}
{% block content %}
<p>Welcome {{ user.name }}!</p>
{% if planet %}
{{ super() }}
{% endif %}
{% endblock %}
