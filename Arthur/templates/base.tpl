<?xml version="1.0" encoding="iso-8859-1"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>{{ slogan }}</title>
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
    {% if menu %}
    <ul class="menulist" id="listMenuRoot">
        {% for drop in menu %}
        <li>
            <a href="{{ drop.1 }}">{{ drop.0 }}</a>
            <ul>
            {% if drop.2 %}
                {% for sub in drop.2 %}
                <li><a href="{{ sub.1 }}">{{ sub.0 }}</a></li>
                {% endfor%}
            {% endif %}
            </ul>
        </li>
        {% endfor %}
    </ul>
    {% endif %}

    <div style="clear: both; height: 2em"></div>
    {% block content %}{% endblock %}
</body>
</html>
