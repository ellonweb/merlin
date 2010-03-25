{% extends "base.tpl" %}
{% block content %}
<center>
<p>Welcome {{ user }}!</p>
</center>
{% if planets %}
{% include "planet_list.tpl" %}
{% endif %}
{% endblock %}
