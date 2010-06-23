{% extends "base.tpl" %}
{% block content %}
<center>
    {% if scan.scantype == "A" %}
        {% include "scans/unit.tpl" %}
    {% endif %}
</center>
{% endblock %}
