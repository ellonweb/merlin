{% extends "base.tpl" %}
{% block content %}
{% if message %}
    <p>{{ message }}</p>
{% endif %}

{% include "scans/request.tpl" %}

<p>&nbsp;</p>

{% with title = "Your Open Requests", requests = mine %}
{% include "scans/open.tpl" %}
{% endwith %}

<p>&nbsp;</p>

{% with title = "All Open Requests", requests = everyone %}
{% include "scans/open.tpl" %}
{% endwith %}

{% endblock %}
