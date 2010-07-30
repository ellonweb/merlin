<tr class="datahigh">
    <th colspan="0">

<a id="{{ scan.pa_id }}"></a>
<a href="{% url "planet_scan_" + scan.scantype|lower, planet.x, planet.y, planet.z %}"
onclick="return linkshift(event, '{{ scan.link }}');">{{ scan.type }} Scan</a>
on <a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.x }}:{{ planet.y }}:{{ planet.z }}</a>
in PT [{{ scan.tick }}]
{% if user|intel %}
    {% if planet.intel and planet.intel.nick %}
        <i>{{ planet.intel.nick }}</i>
        {% if planet.alliance %}
            /
        {% endif %}
    {% endif %}
    {% if planet.intel and planet.alliance %}
        <i>{{ planet.alliance.name }}</i>
    {% endif %}
{% endif %}

    </th>
</tr>
