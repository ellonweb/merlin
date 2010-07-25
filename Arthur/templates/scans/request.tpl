<form onsubmit="request_scan(); return false;">
    <script type="text/javascript">
        function request_scan() {
            url = "/request/" + document.getElementById("x").value + "." + document.getElementById('y').value + "." + document.getElementById('z').value + "/" + document.getElementById('scan').value;
            document.location = url;
        }
    </script>
    <table cellpadding="3" cellspacing="1" class="black">
        <tr class="datahigh"><th colspan="6">Request Scans</th></tr>
        <tr class="header">
            <th>Coords</th>
            <td><input type="text" id="x" name="x" value="{% if planet %}{{ planet.x }}{% endif %}" size="2" /></td>
            <td><input type="text" id="y" name="y" value="{% if planet %}{{ planet.y }}{% endif %}" size="2" /></td>
            <td><input type="text" id="z" name="z" value="{% if planet %}{{ planet.z }}{% endif %}" size="2" /></td>
            <td>        
                <select name="scan" id="scan">
                {% for type, name in types %}
                <option value="{{ type|lower }}">{{ name }}</option>
                {% endfor %}
                </select>
            </td>
            <td><input type="submit" id="request" name="request" value="Request Scan" /></td>
        </tr>
    </table>
</form>
