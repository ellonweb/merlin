{% extends "base.tpl" %}
{% block content %}
<center>
    {% if scan.scantype == "P" %}
        {% include "scans/pscan.tpl" %}
    {% endif %}
    {% if scan.scantype == "D" %}
        {% include "scans/dscan.tpl" %}
    {% endif %}
    {% if scan.scantype == "U" %}
        {% include "scans/unit.tpl" %}
    {% endif %}
    {% if scan.scantype == "J" %}
        {% include "scans/jgp.tpl" %}
    {% endif %}
    {% if scan.scantype == "A" %}
        {% include "scans/unit.tpl" %}
    {% endif %}
</center>
{% endblock %}
