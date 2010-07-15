{% extends "base.tpl" %}
{% block content %}
<center>
<table width=500 class="scan">
{% with planet = scan.planet %}
    <tr>
        <td class="menuheader" colspan=12 height=15>
            {% include "scans/header.tpl" %}
        </td>
    </tr>
    {% if scan.scantype == "P" %}
        {% include "scans/pscan.tpl" %}
    {% endif %}
    {% if scan.scantype == "D" %}
        {% include "scans/dscan.tpl" %}
    {% endif %}
    {% if scan.scantype == "U" %}
        {% include "scans/unit.tpl" %}
    {% endif %}
    {% if scan.scantype == "A" %}
        {% include "scans/unit.tpl" %}
    {% endif %}
{% endwith %}
</table>
</center>
{% endblock %}
