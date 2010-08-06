{% extends "planet_intelintitle.tpl" %}

{% if user == dashuser %}
    {% set who = "Your" %}
{% else %}
    {% set who =  dashuser.name + "'s" %}
{% endif %}

{% block title %}{{ who }} planet{% endblock %}
{% block content %}
<table class="black"><tr class="header"><th width="200">{{ who }} dashboard</th></tr></table>
<p>&nbsp;</p>

{% if planet %}
{{ super() }}
<p>&nbsp;</p>
{% endif %}

<table width="600"><tr valign="top">
    <td width="50%"><center>
        <table cellspacing="1" cellpadding="3" class="black">
            <tr class="datahigh"><th width="200">Family Tree</th></tr>
            <tr class="header"><th>Daddy</th></tr>
            <tr class="odd">
                <td class="center"><a href="{% url "dashboard", dashuser.sponsor %}">{{ dashuser.sponsor }}</a></td>
            </tr>
            <tr class="header"><th>{{ who }} Gimps</th></tr>
             {% for gimp in gimps %}
            <tr class="{{ loop.cycle('odd', 'even') }}">
                <td class="center"><a href="{% url "dashboard", gimp.name%}">{{ gimp.name }}</a></td>
            </tr>
            {% endfor %}
        </table>
    </center></td>
    
    <td width="50%"><center>
        <table cellspacing="1" cellpadding="3" class="black">
            <tr class="datahigh"><th colspan="2">WHO ATE ALL THE COOKIES?!</th></tr>
            <tr class="header">
                <th width="125">Mum</th>
                <th width="75">Cookies</th>
            </tr>
            {% for giver, amount in mums %}
            <tr class="{{ loop.cycle('odd', 'even') }}">
                <td class="center"><a href="{% url "dashboard", giver %}">{{ giver }}</a></td>
                <td class="right">{{ amount }}</td>
            </tr>
            {% endfor %}
        </table>
    </center></td>
</tr></table>

<p>&nbsp;</p>

<table width="600"><tr valign="top">
    <td width="50%"><center>
        <table cellspacing="1" cellpadding="3" class="black">
            <tr class="header"><th colspan="2">{{ who }} def</th></tr>
            {% if ships|length < 1 %}
                <tr class="odd"><td colspan="2" width="200">
                    That lazy pile of shit {{ dashuser.name }} hasn't updated their def since tick {{ dashuser.fleetupdated }}.
                </td></tr>
            {% else %}
                <tr class="odd"><td colspan="2">
                    Fleets: {{ dashuser.fleetcount }}
                </td></tr>
                <tr class="even"><td colspan="2">
                    Updated: {{ dashuser.fleetupdated }} ({{ dashuser.fleetupdated - tick}})
                </td></tr>
                <tr class="header"><td>Ship</td><td>Amount</td></tr>
            {% endif %}
            
            {% for ship in ships %}
            <tr class="{{ loop.cycle('odd', 'even') }}">
                <td>{{ ship.ship.name }}</td>
                <td class="right">{{ ship.ship_count|intcomma }}</td>
            </tr>
            {% endfor %}
            
            <tr class="header"><th colspan="2" width="200">Comment</th></tr>
            <tr class="odd"><td colspan="2">{{ dashuser.fleetcomment }}</td></tr>
        </table>
    </center></td>

    <td width="50%"><center>
        <table cellspacing="1" cellpadding="3" class="black">
            <tr class="header"><th width="200">Phone</th></tr>
            <tr class="odd"><td>{% if dashuser.pubphone or phonefriend %}{{ dashuser.phone }}{% else %}Hidden{% endif %}</td></tr>
            <tr class="even"><td class="right">Public: {{ dashuser.pubphone }}</td></tr>
            <tr class="odd"><td class="right">SMS mode: {% if user.smsmode %}{{ dashuser.smsmode }}{% else %}N/A{% endif %}</td></tr>
            <tr class="header"><th>{{ who }} PhoneFriends:</th></tr>
            {% for friend in dashuser.phonefriends %}
            <tr class="{{ loop.cycle('odd', 'even') }}">
                <td class="center"><a href="{% url "dashboard", friend.name %}">{{ friend.name }}</a></td>
            </tr>
            {% endfor %}
        </table>
    </center></td>
</tr></table>

{% endblock %}
