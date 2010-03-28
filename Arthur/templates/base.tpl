<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>{{ name }}</title>
    <link rel="stylesheet" href="/static/style.css" />

    {% if menu %}
    <!-- FreeStyle Menu v1.0RC by Angus Turnbull http://www.twinhelix.com -->
    <script type="text/javascript" src="/static/fsmenu.js"></script>
    <link rel="stylesheet" type="text/css" href="/static/listmenu_h.css" id="listmenu-h" title="Horizontal 'Earth'" />
    <!-- Fallback CSS menu file allows list menu operation when JS is disabled. -->
    <noscript><link rel="stylesheet" type="text/css" href="/static/listmenu_fallback.css" /></noscript>
    <script type="text/javascript" src="/static/anim.js"></script>
    {% endif %}

</head>

<body>
<div id="wrapper">
<center>
<table cellspacing="1" cellpadding="3">
    <tr class="datahigh">
        <th colspan="2">{{ slogan }}</th>
    </tr>
</table>
</center>
    {% if menu %}
    <table cellspacing="1" cellpadding="3">
        <tr class="header">
            <td>
    <ul class="menulist" id="listMenuRoot">
        {% for drop in menu %}
        <li>
            <a href="{{ drop.1 }}"{% if drop.2 %} target="_blank"{% endif %}>{{ drop.0 }}</a>
            <ul>
            {% if drop.3 %}
                {% for sub in drop.3 %}
                <li><a href="{{ sub.1 }}"{% if sub.2 %} target="_blank"{% endif %}>{{ sub.0 }}</a></li>
                {% endfor%}
            {% endif %}
            </ul>
        </li>
        {% endfor %}
    </ul>
            </td>
<form method="post" action="/lookup/">
            <th>Lookup:</th>
            <td><input type="text" name="lookup" size="8"/></td>
            <td><input type="submit" value="!"/></td>
</form>
        </tr>
    </table>
    {% endif %}

    <div style="clear: both; height: 2em"></div>
    {% block content %}{% endblock %}
    <div id="push"></div>
</div>
<div id="footer" align="center">
    Uses <a href="http://www.twinhelix.com/">DHTML / JavaScript Menu &copy; by TwinHelix Designs</a>
    <br />
    All your base are belong to us. Codez &copy; 2009-2010 Elliot Rosemarine.
    <br />
    Templates &copy; 2006-2010 Arho Huttunen, Thomas D&auml;hling &amp; Elliot Rosemarine.
</div>
</body>
</html>
