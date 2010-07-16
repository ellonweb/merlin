{% extends "base.tpl" %}
{% block content %}
    <table align="center" cellpadding="3" cellspacing="1" width="600">
        <tr><td class="menuheader" colspan="7" align="center" height="15">Scans belonging to this group:</td></tr>
        <tr>
            <td class="one" nowrap="nowrap" width="2%"></td>
            <td class="one" nowrap="nowrap" width="10%"><b>Coords</b></td>
            <td class="one" nowrap="nowrap" width="10%"><b>Race</b></td>
            <td class="one" nowrap="nowrap" width="10%"><b>Size</b></td>
            <td class="one" nowrap="nowrap" width="20%"><b>Value</b></td>
            <td class="one" nowrap="nowrap" width="20%"><b>Score</b></td>
            <td class="one" nowrap="nowrap" width="30%"><b>Scans</b></td>
        </tr>
    </table>
    
    {% for scan in scans %}
    <p>&nbsp;</p>
    {% include "scans/scan.tpl" %}
    {% endfor %}
{% endblock %}
