<table cellspacing="1" cellpadding="3" class="black">
{% with planet = scan.planet %}
    {% include "scans/header.tpl" %}
    
    <tr class="header">
        <th class="left" width="90">Ship</th>
        <th width="65">Amount</th>
        <th width="20">Cl</th>
        <th width="20">T1</th>
        <th width="20">T2</th>
        <th width="20">T3</th>
        
        <th class="left" width="90">Ship</th>
        <th width="65">Amount</th>
        <th width="20">Cl</th>
        <th width="20">T1</th>
        <th width="20">T2</th>
        <th width="20">T3</th>
    </tr>
    
    {% for unit in scan.units %}
        {% if loop.index is odd %}
            <tr class="{{ loop.cycle('odd', 'odd', 'even', 'even') }}">
        {% endif %}
        
        <td class="datahigh left"> {{ unit.ship.name }} </td>
        <td class="right"> {{ unit.amount|intcomma }} </td>
        <td class="center"> {{ unit.ship.class_[:2]|upper }} </td>
        <td class="center"> {{ unit.ship.t1[:2]|upper }} </td>
        <td class="center"> {{ unit.ship.t2|default("-")[:2]|upper }} </td>
        <td class="center"> {{ unit.ship.t3|default("-")[:2]|upper }} </td>
        
        {% if loop.last and loop.index is odd %}
            <td class="datahigh left">  </td>
            <td class="right">  </td>
            <td class="center">  </td>
            <td class="center">  </td>
            <td class="center">  </td>
            <td class="center">  </td>
        {% endif %}
        
        {% if loop.index is even %}
            </tr>
        {% endif %}
    {% endfor %}
    
    <tr class="header center">
        <td colspan=6>
            Total Units: {{ scan.ship_count(True)|intcomma }} ({{ scan.ship_count(False)|intcomma }} visible)
        </td>
        <td colspan=6>
            Total Value: {{ scan.ship_value()|intcomma }}
        </td>
    </tr>
    
    <tr class="datahigh center">
        <td colspan=6>
            <a href="{{ scan.bcalc(True) }}" target="_blank">Calc as Target</a>
        </td>
        <td colspan=6>
            <a href="{{ scan.bcalc(False) }}" target="_blank">Calc as Attacker</a>
        </td>
    </tr>
    
{% endwith %}
</table>
