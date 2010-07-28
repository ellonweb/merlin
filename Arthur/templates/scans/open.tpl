<table cellpadding="3" cellspacing="1" class="black">
    <script type="text/javascript">
        function request_blocks(id) {
            var dists = document.getElementById(id + '_dists').value;
            var url = "/request/" + id + "/blocks/" + dists + "/";
            document.location = url;
        }
    </script>
    <tr class="datahigh"><th colspan="8">{{ title }}</th></tr>
    <tr class="header">
        <th>Coords</th>
        <th>Tick</th>
        <th>Type</th>
        <th>Dists</th>
        <th>Link</th>
        <th>Requested by</th>
        <th></th>
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
        <td>
            <form onsubmit="request_blocks({{ req.id }}); return false;">
                <input type="submit" value="Blocks" />
                <input type="text" id="{{ req.id }}_dists" name="{{ req.id }}_dists" size="1" value="{{ req.dists }}" />
            </form>
        </td>
    </tr>
    {% endfor %}
    <tr class="header center">
        <td colspan="8">(Paste the links of the completed scans in the Lookup bar)</td>
    </tr>
</table>
