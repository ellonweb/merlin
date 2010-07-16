{% extends "base.tpl" %}
{% block content %}
<p>Welcome {{ user.name }}!</p>
{% if planets %}
{% include "planet_list.tpl" %}
{% endif %}
{% endblock %}
