<form onsubmit="request_scan(); return false;">
    <script type="text/javascript">
        function request_scan() {
            var x = document.getElementById("x").value;
            var y = document.getElementById("y").value;
            var z = document.getElementById("z").value;
            var type = document.getElementById('type').value;
            if (document.getElementById('dists').value == '' || document.getElementById('dists').value == 'dists')
                var dists = '';
            else
                var dists = document.getElementById('dists').value;
            var url = "/request/" + x + "." + y + "." + z + "/" + type + "/" + (dists ? dists + "/" : "");
            document.location = url;
        }
    </script>
    <table cellpadding="3" cellspacing="1" class="black">
        <tr class="datahigh"><th colspan="7">Request Scans</th></tr>
        <tr class="header">
            <th>Coords</th>
            <td><input type="text" id="x" name="x" value="{% if planet %}{{ planet.x }}{% endif %}" size="2" /></td>
            <td><input type="text" id="y" name="y" value="{% if planet %}{{ planet.y }}{% endif %}" size="2" /></td>
            <td><input type="text" id="z" name="z" value="{% if planet %}{{ planet.z }}{% endif %}" size="2" /></td>
            <td>        
                <select name="type" id="type">
                {% for type, name in types %}
                <option value="{{ type|lower }}">{{ name }}</option>
                {% endfor %}
                </select>
            </td>
            <td><input type="text" id="dists" name="dists" value="dists" size="3" onfocus="value=''" /></td>
            <td><input type="submit" id="request" name="request" value="Request Scan" /></td>
        </tr>
    </table>
</form>
