<table cellspacing="1" cellpadding="3" width="500" class="black">
{% with planet = scan.planet, pscan = scan.planetscan %}
<tr class="datahigh">
    <th colspan="4">
    {% include "scans/header.tpl" %}
      </th>
</tr>
    
    <tr class="header right">
        <td> Ruler </td>
        <td class="center"> {{ planet.rulername }} </td>
        <td> Planet </td>
        <td class="center"> {{ planet.planetname }} </td>
    </tr>
    
    <tr class="odd right">
        <td class="datahigh" width="25%"> Score </td>
        <td width="25%"> {{ planet.history(scan.tick)|default(planet).score|intcomma }} </td>
        <td class="datahigh" width="25%"> Value </td>
        <td width="25%"> {{ planet.history(scan.tick)|default(planet).value|intcomma }} </td>
    </tr>
    
    <tr class="even right">
        <td class="datahigh" width="25%"> Agents </td>
        <td width="25%"> {{ pscan.agents|intcomma }} </td>
        <td class="datahigh" width="25%"> Guards </td>
        <td width="25%"> {{ pscan.guards|intcomma }} </td>
    </tr>
    
    <tr class="header right">
        <td width="25%">  </td>
        <td width="25%"> Metal </td>
        <td width="25%"> Crystal </td>
        <td width="25%"> Eonium </td>
    </tr>
    
    <tr class="odd right">
        <td class="datahigh" width="25%"> Asteroids </td>
        <td width="25%"> {{ pscan.roid_metal|intcomma }} </td>
        <td width="25%"> {{ pscan.roid_crystal|intcomma }} </td>
        <td width="25%"> {{ pscan.roid_eonium|intcomma }} </td>
    </tr>
    
    <tr class="even right">
        <td class="datahigh" width="25%"> Resources </td>
        <td width="25%"> {{ pscan.res_metal|intcomma }} </td>
        <td width="25%"> {{ pscan.res_crystal|intcomma }} </td>
        <td width="25%"> {{ pscan.res_eonium|intcomma }} </td>
    </tr>
    
    <tr class="header center"><td colspan="4"> Factory Usage </td></tr>
    <tr class="datahigh center">
        <td> Light </td>
        <td> Medium </td>
        <td> Heavy </td>
        <td> Total </td>
    </tr>
    <tr class="odd center">
        <td> {{ pscan.factory_usage_light }} </td>
        <td> {{ pscan.factory_usage_medium }} </td>
        <td> {{ pscan.factory_usage_heavy }} </td>
        <td> {{ pscan.prod_res|intcomma }} </td>
    </tr>
    
{% endwith %}
</table>
