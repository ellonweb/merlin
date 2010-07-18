{% extends "scans/group.tpl" %}
{% block title %}All scans from tick {{ tick }}{% endblock %}
{% block url %}{% url "scan_id", scan.tick, scan.pa_id %}{% endblock %}
