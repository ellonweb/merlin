<table cellspacing="1" cellpadding="3" width="100%">
<tr>
    <td rowspan="2" width="33%" align="left">
        <a href="/"><img border="0" src="/static/logo.png" /></a>
    </td>
    <th valign="top" align="center">{{ slogan }}</th>
    <td width="33%" align="right"></td>
</tr>
<tr>
    <td width="34%" valign="middle" align="center">
{% if user is defined %}
    {% if user.planet %}{% with planet = user.planet %}
    
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
        <td width="33%" align="right">{{ planet|rank("size") }}</td>
    </tr>
    <tr>
        <td width="33%" align="left">Value:</td>
        <td width="34%" align="center">{{ planet.value|intcomma }}</td>
        <td width="33%" align="right">{{ planet|rank("value") }}</td>
    </tr>
    <tr>
        <td width="33%" align="left">Score:</td>
        <td width="34%" align="center">{{ planet.score|intcomma }}</td>
        <td width="33%" align="right">{{ planet|rank("score") }}</td>
    </tr>
    <tr>
        <td width="33%" align="left">XP:</td>
        <td width="34%" align="center">{{ planet.xp|intcomma }}</td>
        <td width="33%" align="right">{{ planet|rank("xp") }}</td>
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
{% endif %}
    </td>
    <td width="33%" align="right">
        <table class="stats">
            <tr><td>Planets:</td><td><span class="gray">{{update.planets}}</span></td><td><strong class="Ter">Ter:</strong></td><td><span class="gray">{{update.ter}}</span></td></tr>
            <tr><td>Galaxies:</td><td><span class="gray">{{update.galaxies}}</span></td><td><strong class="Cat">Cat:</strong></td><td><span class="gray">{{update.cat}}</span></td></tr>		
            <tr><td>Clusters:</td><td><span class="gray">{{update.clusters}}</span></td><td><strong class="Xan">Xan:</strong></td><td><span class="gray">{{update.xan}}</span></td></tr>		
            <tr><td>Alliances:</td><td><span class="gray">{{update.alliances}}</span></td><td><strong class="Zik">Zik:</strong></td><td><span class="gray">{{update.zik}}</span></td></tr>
            <tr><td>Cluster 200:</td><td><span class="gray">{{update.c200}}</span></td><td><strong class="Etd">Etd:</strong></td><td><span class="gray">{{update.etd}}</span></td></tr>
            <tr><td>Last Update:</td><td><span class="gray">{{update.age}}</span></td><td>Tick:</td><td><span class="gray">{{update.id}}</span></td></tr>
        </table>
    </td>
</tr>
</table>
