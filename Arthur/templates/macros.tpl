{% macro planetlink(planet) -%}
    href="{% url "planet", planet.x, planet.y, planet.z %}"
    {%- if user|intel %} onclick="return linkshift(event, '{% url "iplanet", planet.x, planet.y, planet.z %}');"
    {%- else %} onclick="return linkshift(event)"
    {% endif -%}
{%- endmacro %}
{% macro planetscanslink(planet) -%}
    href="{% url "planet", planet.x, planet.y, planet.z %}"
    {%- if user|scans %} onclick="return linkshift(event, '{% url "planet_scans", planet.x, planet.y, planet.z %}');"
    {%- else %} onclick="return linkshift(event)"
    {% endif -%}
{%- endmacro %}
{% macro galaxyscanslink(galaxy) -%}
    href="{% url "galaxy", galaxy.x, galaxy.y %}"
    {%- if user|scans %} onclick="return linkshift(event, '{% url "galaxy_scans", galaxy.x, galaxy.y %}');"
    {%- else %} onclick="return linkshift(event)"
    {% endif -%}
{%- endmacro %}
{% macro alliancelink(name) -%}
    href="{% url "alliance", name %}"
    {%- if user|intel %} onclick="return linkshift(event, '{% url "alliance_members", name %}');"
    {%- else %} onclick="return linkshift(event)"
    {% endif -%}
{%- endmacro %}
