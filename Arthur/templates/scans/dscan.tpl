{% with dscan = scan.devscan %}
    <tr>
        <td class="one left" width="35%"> Light Factory </td>
        <td class="two left" width="15%"> {{ dscan.light_factory|and_percent(dscan.total) }} </td>
        <td class="one left" width="35%"> Medium Factory </td>
        <td class="two left" width="15%"> {{ dscan.medium_factory|and_percent(dscan.total) }} </td>
    </tr>
    <tr>
        <td class="one left" width="35%"> Heavy Factory </td>
        <td class="two left" width="15%"> {{ dscan.heavy_factory|and_percent(dscan.total) }} </td>
        <td class="one left" width="35%"> Wave Amplifier </td>
        <td class="two left" width="15%"> {{ dscan.wave_amplifier|and_percent(dscan.total) }} </td>
    </tr>
    <tr>
        <td class="one left" width="35%"> Wave Distorter </td>
        <td class="two left" width="15%"> {{ dscan.wave_distorter|and_percent(dscan.total) }} </td>
        <td class="one left" width="35%"> Metal Refinery </td>
        <td class="two left" width="15%"> {{ dscan.metal_refinery|and_percent(dscan.total) }} </td>
    </tr>
    <tr>
        <td class="one left" width="35%"> Crystal Refinery </td>
        <td class="two left" width="15%"> {{ dscan.crystal_refinery|and_percent(dscan.total) }} </td>
        <td class="one left" width="35%"> Eonium Refinery </td>
        <td class="two left" width="15%"> {{ dscan.eonium_refinery|and_percent(dscan.total) }} </td>
    </tr>
    <tr>
        <td class="one left" width="35%"> Research Laboratory </td>
        <td class="two left" width="15%"> {{ dscan.research_lab|and_percent(dscan.total) }} </td>
        <td class="one left" width="35%"> Finance Centre </td>
        <td class="two left" width="15%"> {{ dscan.finance_centre|and_percent(dscan.total) }} </td>
    </tr>
    <tr>
        <td class="one left" width="35%"> Security Centre </td>
        <td class="two left" width="15%"> {{ dscan.security_centre|and_percent(dscan.total) }} </td>
        <td class="one left" width="35%">  </td>
        <td class="two left" width="15%">  </td>
    </tr>
    <tr><td class="one" colspan="4"> Total Constructions: {{ dscan.total }} </td></tr>
    
    <tr>
        <td class="one left" width="25%"> Space Travel </td>
        <td class="two left" width="5%"> {{ dscan.travel }} </td>
        <td class="two left" width="70%" colspan="2"> {{ dscan.travel_str() }} </td>
    </tr>
    <tr>
        <td class="one left" width="25%"> Infrajerome </td>
        <td class="two left" width="5%"> {{ dscan.infrastructure }} </td>
        <td class="two left" width="70%" colspan="2"> {{ dscan.infra_str() }} </td>
    </tr>
    <tr>
        <td class="one left" width="25%"> Hulls </td>
        <td class="two left" width="5%"> {{ dscan.hulls }} </td>
        <td class="two left" width="70%" colspan="2"> {{ dscan.hulls_str() }} </td>
    </tr>
    <tr>
        <td class="one left" width="25%"> Waves </td>
        <td class="two left" width="5%"> {{ dscan.waves }} </td>
        <td class="two left" width="70%" colspan="2"> {{ dscan.waves_str() }} </td>
    </tr>
    <tr>
        <td class="one left" width="25%"> Core Extraction </td>
        <td class="two left" width="5%"> {{ dscan.core }} </td>
        <td class="two left" width="70%" colspan="2"> {{ dscan.core_str() }} </td>
    </tr>
    <tr>
        <td class="one left" width="25%"> Covert Ops </td>
        <td class="two left" width="5%"> {{ dscan.covert_op }} </td>
        <td class="two left" width="70%" colspan="2"> {{ dscan.covop_str() }} </td>
    </tr>
    <tr>
        <td class="one left" width="25%"> Asteroid Mining </td>
        <td class="two left" width="5%"> {{ dscan.mining }} </td>
        <td class="two left" width="70%" colspan="2"> {{ dscan.mining_str() }} </td>
    </tr>
    <tr><td class="one" colspan="4"> Total Technologies: {{ dscan.travel + dscan.infrastructure + dscan.hulls + dscan.waves + dscan.core + dscan.covert_op + dscan.mining }} </td></tr>
    
{% endwith %}
