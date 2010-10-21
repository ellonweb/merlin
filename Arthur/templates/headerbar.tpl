<table cellspacing="1" cellpadding="3" width="100%">
<tr>
    <td width="33%" align="left">
    </td>
    <td width="34%" valign="middle" align="center">
    {% if setplanet %}
        <p>{{ setplanet }}</p>
    {% endif %}
    {% if user.planet %}{% with planet = user.planet, ph = user.planet.history(night) %}
        You are: {{ planet.rulername }} of {{ planet.planetname }}
            (<a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.z }}</a>)
            <span class="{{ planet.race }}">{{ planet.race }}</span><br>
        Size: {{ planet.size|intcomma }}{% if ph %} {{ planet.size_rank|growth_rank_image(ph.size_rank) }}{% endif %} {{ planet.size_rank }}<br>
        Value: {{ planet.value|intcomma }}{% if ph %} {{ planet.value_rank|growth_rank_image(ph.value_rank) }}{% endif %} {{ planet.value_rank }}<br>
        Score: {{ planet.score|intcomma }}{% if ph %} {{ planet.score_rank|growth_rank_image(ph.score_rank) }}{% endif %} {{ planet.score_rank }}<br>
        XP: {{ planet.xp|intcomma }}{% if ph %} {{ planet.xp_rank|growth_rank_image(ph.xp_rank) }}{% endif %} {{ planet.xp_rank }}<br>
        <form method="post">
            <input type="submit" name="planet" value="Clear"/>
        </form>
    {% endwith %}
    {% else %}
        <form method="post">
            My Coords:<br />
            <input type="text" size="7" name="planet"/>
            <input type="submit" value="!"/>
        </form>
    {% endif %}
    </td>
    <td width="33%" align="right">
    </td>
</tr>
</table>
