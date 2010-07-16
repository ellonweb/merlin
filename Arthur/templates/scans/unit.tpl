<table width="500" class="scan">
{% with planet = scan.planet %}
    <tr>
        <td class="menuheader" colspan=12 height=15>
            {% include "scans/header.tpl" %}
        </td>
    </tr>
    
    <tr>
        <td class="menuheader left" width=30%>Ship</td>
        <td class="menuheader left" width=10%>Amount</td>
        <td class="menuheader left" width=5%>Cl</td>
        <td class="menuheader left" width=5%>T1</td>
        <td class="menuheader left" width=5%>T2</td>
        <td class="menuheader left" width=5%>T3</td>
        
        <td class="menuheader left" width=30%>Ship</td>
        <td class="menuheader left" width=10%>Amount</td>
        <td class="menuheader left" width=5%>Cl</td>
        <td class="menuheader left" width=5%>T1</td>
        <td class="menuheader left" width=5%>T2</td>
        <td class="menuheader left" width=5%>T3</td>
    </tr>
    
    {% for unit in scan.units %}
        {% if loop.index is odd %}
            <tr>
        {% endif %}
        
        <td class="one left"> {{ unit.ship.name }} </td>
        <td class="two left"> {{ unit.amount }} </td>
        <td class="two"> {{ unit.ship.class_[:2]|upper }} </td>
        <td class="two"> {{ unit.ship.t1[:2]|upper }} </td>
        <td class="two"> {{ unit.ship.t2|default("-")[:2]|upper }} </td>
        <td class="two"> {{ unit.ship.t3|default("-")[:2]|upper }} </td>
        
        {% if loop.last and loop.index is odd %}
            <td class="one left">  </td>
            <td class="two left">  </td>
            <td class="two">  </td>
            <td class="two">  </td>
            <td class="two">  </td>
            <td class="two">  </td>
        {% endif %}
        
        {% if loop.index is even %}
            </tr>
        {% endif %}
    {% endfor %}
    
    <tr>
        <td class=one width=100% colspan=6>
            Total Units: {{ scan.ship_count(True)|intcomma }} ({{ scan.ship_count(False)|intcomma }} visible)
        </td>
        <td class=one width=100% colspan=6>
            Total Value: {{ scan.ship_value()|intcomma }}
        </td>
    </tr>
    
    <tr>
        <td class="two center" width=100% colspan=6>
            <a href="{{ scan.bcalc(True) }}" target="_blank">Calc as Target</a>
        </td>
        <td class="two center" width=100% colspan=6>
            <a href="{{ scan.bcalc(False) }}" target="_blank">Calc as Attacker</a>
        </td>
    </tr>
    
{% endwith %}
</table>
