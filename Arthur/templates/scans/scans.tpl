{% extends "base.tpl" %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}

{% include "scans/request.tpl" %}

<p>&nbsp;</p>

{% with title = "Your Open Requests", requests = open %}
{% include "scans/open.tpl" %}
{% endwith %}

<p>&nbsp;</p>

{% with title = "Your Completed Requests", scans = completed %}
{% include "scans/completed.tpl" %}
{% endwith %}

<p>&nbsp;</p>

{% with title = "Your Recent Scans", scans = scans %}
{% include "scans/completed.tpl" %}
{% endwith %}

{% endblock %}
