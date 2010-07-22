{% extends "base.tpl" %}
{% block content %}
<p>&nbsp;</p>

{{ title }}


<table>

<tr class="datahigh">
<th colspan="2">
Request Scans
</th>
</tr>
<tr>
<th>Coords</th>
<td>
<input type="text" id="x" name="x" value="{% if planet %}{{ planet.x }}{% endif %}" size="2" />:
<input type="text" id="y" name="y" value="{% if planet %}{{ planet.y }}{% endif %}" size="2" />:
<input type="text" id="z" name="z" value="{% if planet %}{{ planet.z }}{% endif %}" size="2" />

<select name="scan" id="scan">
<option value="p">Planet</option>
<option value="d">Development</option>
<option value="u">Unit</option>
<option value="n">News</option>
<option value="j">Jumpgate probe</option>
<option value="a">Advanced Unit</option>
</select>

<input type="button" id="request" name="request" value="Request scan" onclick="request_scan()"/>
<script type="text/javascript">
function request_scan() {
url = "/request/" + document.getElementById("x").value + "." + document.getElementById('y').value + "." + document.getElementById('z').value + "/" + document.getElementById('scan').value;
document.location = url;
}
</script>
</td>
</tr>
</table>
<br />
<br />

<table>

<tr class="datahigh">
        <th colspan="4">
            Active requests
        </th>
    </tr>
<tr class="header">
        <th>Coords</th>
        <th>Scan Type</th>
        <th>Dists</th>
        <th>Requester</th>
    </tr>
{% for req in requests %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center">{{ req.target.x }}:{{ req.target.y }}:{{ req.target.z }}</td>
        <td><a href="{{ req.paurl }}">{{ req.scanname }}</a></td>
        <td>{{ req.dists or "&nbsp;" }}</td>
        <td class="center">{{ req.user.name }}</td>
    </tr>
    {% endfor %}
</table>

<p>&nbsp;</p>

<table>

    <tr class="datahigh">
        <th colspan="6">
            My Recent Requests
        </th>
    </tr>
    <tr class="header">
      <th colspan="2">
        Request
      </th>
      <th colspan="4">
        Result
      </th>
    </tr>
    <tr class="header">
        <th>Coords</th>
        <th>Scan Type</th>
        <th>Link</th>
        <th>Tick</th>
        <th>Scanned  by</th>
        <th>Planetarion Url</th>
    </tr>
    {% for req in userrequests %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center">{{ req.target.x }}:{{ req.target.y }}:{{ req.target.z }}</td>
        <td><a href="{{ req.paurl }}">{{ req.scanname }}</a></td>
        {% if req.scan %}
          <td class="center"><a href="{% url "scan_id", req.scan.tick, req.scan.pa_id %}"
                    onclick="return linkshift(event, '{{ req.scan.link }}');">{{ req.scan.scantype }}</a></td>
          <td class="center">{{ req.scan.tick }}</td>
          <td class="center">{{ req.scan.scanner.name }}</td>
          <td class="center"><a href="{{ req.scan.link }}" target="_blank">{{ req.scan.pa_id }}</a></td>
        {% endif %}
    </tr>
    {% endfor %}
</table>

{% endblock %}