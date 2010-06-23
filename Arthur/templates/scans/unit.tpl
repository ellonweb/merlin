<table width=500 class="scan">
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
        <td class="two"> {{ unit.ship.class_|slice_(":2")|upper }} </td>
        <td class="two"> {{ unit.ship.t1|slice_(":2")|upper }} </td>
        <td class="two"> {{ unit.ship.t2|default("-")|slice_(":2")|upper }} </td>
        <td class="two"> {{ unit.ship.t3|default("-")|slice_(":2")|upper }} </td>
        
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
{% endwith %}
</table>
