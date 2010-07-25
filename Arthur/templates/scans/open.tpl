<table cellpadding="3" cellspacing="1" class="black">
    <tr class="datahigh"><th colspan="7">{{ title }}</th></tr>
    <tr class="header">
        <th>Coords</th>
        <th>Tick</th>
        <th>Type</th>
        <th>Dists</th>
        <th>Link</th>
        <th>Requester</th>
        <th></th>
    </tr>
    {% for req in requests %}
    <tr class="{{ loop.cycle('odd', 'even') }}">
        <td class="center">{{ req.target.x }}:{{ req.target.y }}:{{ req.target.z }}</td>
        <td class="center">{{ req.tick }}</td>
        <td class="center">{{ req.scantype }}</td>
        <td>i:{{ req.target.intel.dists }}/r:{{ req.dists }}</td>
        <td class="center"><a href="{{ req.link }}" target="_blank">Do Scan!</td>
        <td class="center">{{ req.user.name }}</td>
        <td><a href="{% url "request_cancel", req.id %}">Cancel</a></td>
    </tr>
    {% endfor %}
</table>
