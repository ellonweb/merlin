<table cellspacing="1" cellpadding="3" width="500" class="black">
{% with planet = scan.planet, dscan = scan.devscan %}
<tr class="datahigh">
    <th colspan="4">
    {% include "scans/header.tpl" %}
      </th>
</tr>
    
    <tr class="header center"><td colspan="4"> Constructions: ({{ dscan.total }} total) </td></tr>
    <tr class="odd">
        <td class="datahigh" width="35%"> Light Factory </td>
        <td width="15%"> {{ dscan.light_factory|and_percent(dscan.total) }} </td>
        <td class="datahigh" width="35%"> Medium Factory </td>
        <td width="15%"> {{ dscan.medium_factory|and_percent(dscan.total) }} </td>
    </tr>
    <tr class="even">
        <td class="datahigh" width="35%"> Heavy Factory </td>
        <td width="15%"> {{ dscan.heavy_factory|and_percent(dscan.total) }} </td>
        <td class="datahigh" width="35%"> Wave Amplifier </td>
        <td width="15%"> {{ dscan.wave_amplifier|and_percent(dscan.total) }} </td>
    </tr>
    <tr class="odd">
        <td class="datahigh" width="35%"> Wave Distorter </td>
        <td width="15%"> {{ dscan.wave_distorter|and_percent(dscan.total) }} </td>
        <td class="datahigh" width="35%"> Metal Refinery </td>
        <td width="15%"> {{ dscan.metal_refinery|and_percent(dscan.total) }} </td>
    </tr>
    <tr class="even">
        <td class="datahigh" width="35%"> Crystal Refinery </td>
        <td width="15%"> {{ dscan.crystal_refinery|and_percent(dscan.total) }} </td>
        <td class="datahigh" width="35%"> Eonium Refinery </td>
        <td width="15%"> {{ dscan.eonium_refinery|and_percent(dscan.total) }} </td>
    </tr>
    <tr class="odd">
        <td class="datahigh" width="35%"> Research Laboratory </td>
        <td width="15%"> {{ dscan.research_lab|and_percent(dscan.total) }} </td>
        <td class="datahigh" width="35%"> Finance Centre </td>
        <td width="15%"> {{ dscan.finance_centre|and_percent(dscan.total) }} </td>
    </tr>
    <tr class="even">
        <td class="datahigh" width="35%"> Security Centre </td>
        <td width="15%"> {{ dscan.security_centre|and_percent(dscan.total) }} </td>
        <td class="datahigh" width="35%">  </td>
        <td width="15%">  </td>
    </tr>
    
    <tr class="header center"><td colspan="4"> Research: ({{ dscan.travel + dscan.infrastructure + dscan.hulls + dscan.waves + dscan.core + dscan.covert_op + dscan.mining }} total) </td></tr>
    <tr class="odd">
        <td class="datahigh" width="25%"> Space Travel </td>
        <td width="5%"> {{ dscan.travel }} </td>
        <td width="70%" colspan="2"> {{ dscan.travel_str() }} </td>
    </tr>
    <tr class="even">
        <td class="datahigh" width="25%"> Infrajerome </td>
        <td width="5%"> {{ dscan.infrastructure }} </td>
        <td width="70%" colspan="2"> {{ dscan.infra_str() }} </td>
    </tr>
    <tr class="odd">
        <td class="datahigh" width="25%"> Hulls </td>
        <td width="5%"> {{ dscan.hulls }} </td>
        <td width="70%" colspan="2"> {{ dscan.hulls_str() }} </td>
    </tr>
    <tr class="even">
        <td class="datahigh" width="25%"> Waves </td>
        <td width="5%"> {{ dscan.waves }} </td>
        <td width="70%" colspan="2"> {{ dscan.waves_str() }} </td>
    </tr>
    <tr class="odd">
        <td class="datahigh" width="25%"> Core Extraction </td>
        <td width="5%"> {{ dscan.core }} </td>
        <td width="70%" colspan="2"> {{ dscan.core_str() }} </td>
    </tr>
    <tr class="even">
        <td class="datahigh" width="25%"> Covert Ops </td>
        <td width="5%"> {{ dscan.covert_op }} </td>
        <td width="70%" colspan="2"> {{ dscan.covop_str() }} </td>
    </tr>
    <tr class="odd">
        <td class="datahigh" width="25%"> Asteroid Mining </td>
        <td width="5%"> {{ dscan.mining }} </td>
        <td width="70%" colspan="2"> {{ dscan.mining_str() }} </td>
    </tr>
    
{% endwith %}
</table>
