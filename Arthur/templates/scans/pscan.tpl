<table width="500" class="scan">
{% with planet = scan.planet, pscan = scan.planetscan %}
    <tr>
        <td class="menuheader" colspan=12 height=15>
            {% include "scans/header.tpl" %}
        </td>
    </tr>
    
    <tr>
        <td class="one left" height="15"> Ruler </td>
        <td class="two left" height="15"> {{ planet.rulername }} </td>
        <td class="one left" height="15"> Planet </td>
        <td class="two left" height="15"> {{ planet.planetname }} </td>
    </tr>
    
    <tr>
        <td class="one left" height="15" width="25%"> Score </td>
        <td class="two left" height="15" width="25%"> {{ planet.history(scan.tick)|default(planet).score|intcomma }} </td>
        <td class="one left" height="15" width="25%"> Value </td>
        <td class="two left" height="15" width="25%"> {{ planet.history(scan.tick)|default(planet).value|intcomma }} </td>
    </tr>
    
    <tr>
        <td class="one left" height="15" width="25%"> Agents </td>
        <td class="two left" height="15" width="25%"> {{ pscan.agents|intcomma }} </td>
        <td class="one left" height="15" width="25%"> Guards </td>
        <td class="two left" height="15" width="25%"> {{ pscan.guards|intcomma }} </td>
    </tr>
    
    <tr>
        <td class="one left" height="15" width="25%">  </td>
        <td class="one left" height="15" width="25%"> Metal </td>
        <td class="one left" height="15" width="25%"> Crystal </td>
        <td class="one left" height="15" width="25%"> Eonium </td>
    </tr>
    
    <tr>
        <td class="one left" height="15" width="25%"> Asteroids </td>
        <td class="two left" height="15" width="25%"> {{ pscan.roid_metal|intcomma }} </td>
        <td class="two left" height="15" width="25%"> {{ pscan.roid_crystal|intcomma }} </td>
        <td class="two left" height="15" width="25%"> {{ pscan.roid_eonium|intcomma }} </td>
    </tr>
    
    <tr>
        <td class="one left" height="15" width="25%"> Resources </td>
        <td class="two left" height="15" width="25%"> {{ pscan.res_metal|intcomma }} </td>
        <td class="two left" height="15" width="25%"> {{ pscan.res_crystal|intcomma }} </td>
        <td class="two left" height="15" width="25%"> {{ pscan.res_eonium|intcomma }} </td>
    </tr>
    
    <tr><td class="one" colspan="4"> Factory Usage </td></tr>
    <tr>
        <td class="one left"> Light </td>
        <td class="one left"> Medium </td>
        <td class="one left"> Heavy </td>
        <td class="one left"> Total </td>
    </tr>
    <tr>
        <td class="two left"> {{ pscan.factory_usage_light }} </td>
        <td class="two left"> {{ pscan.factory_usage_medium }} </td>
        <td class="two left"> {{ pscan.factory_usage_heavy }} </td>
        <td class="two left"> {{ pscan.prod_res|intcomma }} </td>
    </tr>
    
{% endwith %}
</table>
