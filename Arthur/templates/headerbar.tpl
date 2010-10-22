<table cellspacing="1" cellpadding="3" width="100%">
<tr>
    <td width="33%" align="left">
    </td>
    <td width="34%" valign="middle" align="center">
    {% if user.planet %}{% with planet = user.planet, ph = user.planet.history(night) %}
    
<table cellspacing="0" cellpadding="1">
    <tr>
        <td align="center" colspan="3">
        <form method="post">
        You are: <a class="myplanet" href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.rulername }}</a>
            (<a href="{% url "galaxy", planet.x, planet.y %}">{{ planet.x }}:{{ planet.y }}</a>
            <a href="{% url "planet", planet.x, planet.y, planet.z %}">{{ planet.z }}</a>)
            <span class="{{ planet.race }}">{{ planet.race }}</span>
            <input type="submit" name="planet" value="Clear"/>
        </form>
        </td>
    </tr>
    <tr>
        <td width="33%" align="left">Size:</td>
        <td width="34%" align="center">{{ planet.size|intcomma }}</td>
        <td width="33%" align="right">{{ planet.size_rank }}{% if ph %} {{ planet.size_rank|growth_rank_image(ph.size_rank) }}{% endif %}</td>
    </tr>
    <tr>
        <td width="33%" align="left">Value:</td>
        <td width="34%" align="center">{{ planet.value|intcomma }}</td>
        <td width="33%" align="right">{{ planet.value_rank }}{% if ph %} {{ planet.value_rank|growth_rank_image(ph.value_rank) }}{% endif %}</td>
    </tr>
    <tr>
        <td width="33%" align="left">Score:</td>
        <td width="34%" align="center">{{ planet.score|intcomma }}</td>
        <td width="33%" align="right">{{ planet.score_rank }}{% if ph %} {{ planet.score_rank|growth_rank_image(ph.score_rank) }}{% endif %}</td>
    </tr>
    <tr>
        <td width="33%" align="left">XP:</td>
        <td width="34%" align="center">{{ planet.xp|intcomma }}</td>
        <td width="33%" align="right">{{ planet.xp_rank }}{% if ph %} {{ planet.xp_rank|growth_rank_image(ph.xp_rank) }}{% endif %}</td>
    </tr>
</table>
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
