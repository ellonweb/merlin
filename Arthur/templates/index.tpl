{% extends "base.tpl" %}
{% block content %}
<center>
<p>Welcome {{ user }}!</p>
{% if planet %}
<table cellspacing="0" cellpadding="0" width="100%" class="black">
<tr>
<td>
<table cellspacing="1" cellpadding="3" width="100%">
	<tr class="planethigh">
		<th colspan="17">Your planet</th>
	</tr>
	<tr class="header">
		<th colspan="4">Rank</th>
		<th colspan="10">&nbsp;</th>
	</tr>
	<tr class="header">
		<th>Score</th>
		<th>Value</th>
		<th>Size</th>
		<th>XP</th>
		<th>X</th>
		<th>Y</th>
		<th>Z</th>
		<th>Ruler</th>
		<th>Planet</th>
		<th>Race</th>
		<th>Size</th>
		<th>Value</th>
		<th>Score</th>
		<th>XP</th>
	</tr>
	<tr class="odd">
		<td align="right">{{ planet.score_rank }}</td>
		<td align="right">{{ planet.value_rank }}</td>
		<td align="right">{{ planet.size_rank }}</td>
		<td align="right">{{ planet.xp_rank }}</td>
		<td align="right">{{ planet.x }}</td>
		<td align="right">{{ planet.y }}</td>
		<td align="right">{{ planet.z }}</td>
		<td>{{ planet.rulername }}</td>
		<td>{{ planet.planetname }}</td>
		<td class="{{ planet.race }}">{{ planet.race }}</td>
		<td align="right">{{ planet.size }}</td>
		<td align="right">{{ planet.value }}</td>
		<td align="right">{{ planet.score }}</td>
		<td align="right">{{ planet.xp }}</td>
	</tr>
</table>
</td>
</tr>
</table>
{% endif %}
</center>
{% endblock %}
