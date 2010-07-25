{% extends "base.tpl" %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}

{% include "scans/request.tpl" %}

<p>&nbsp;</p>

{% with title = "Open Requests", requests = open %}
{% include "scans/open.tpl" %}
{% endwith %}

{% endblock %}
