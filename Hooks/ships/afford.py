# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
from Core.paconf import PA
from Core.db import session
from Core.maps import Planet, Ship, Scan, PlanetScan, DevScan
from Core.loadable import loadable, route

class afford(loadable):
    """Calculates the number of a certain ship the planet can produce based on the most recent planet scan"""
    usage = " <x:y:z> <ship>"
    
    @route(loadable.planet_coord+r"\s+(\w+)")
    def execute(self, message, user, params):
        
        p = Planet.load(*params.group(1,3,5))
        if p is None:
            message.reply("No planet with coords %s:%s:%s found" % params.group(1,3,5))
            return
        ship = Ship.load(name=params.group(6))
        if ship is None:
            message.alert("No Ship called: %s" % (params.group(6),))
            return
        
        scan = p.scan("P")
        if scan is None:
            message.reply("No planet scans available on %s:%s:%s" % (p.x,p.y,p.z,))
            return
        
        planetscan = scan.planetscan
        tick=scan.tick
        res_m=planetscan.res_metal
        res_c=planetscan.res_crystal
        res_e=planetscan.res_eonium
        prod_res=planetscan.prod_res
        rand_id=scan.pa_id
        
        cost_m=ship.metal
        cost_c=ship.crystal
        cost_e=ship.eonium
        total_cost=ship.total_cost
        
        class_factory_table = {'Fighter': 'factory_usage_light', 'Corvette': 'factory_usage_light', 'Frigate': 'factory_usage_medium',
                               'Destroyer': 'factory_usage_medium', 'Cruiser': 'factory_usage_heavy', 'Battleship': 'factory_usage_heavy'}
        prod_modifier_table = {'None': 0.0, 'Low': 0.33, 'Medium': 0.66, 'High': 1.0}
        
        capped_number = min(res_m/cost_m, res_c/cost_c, res_e/cost_e)
        overflow = res_m+res_c+res_e-(capped_number*(cost_m+cost_c+cost_e))
        buildable = capped_number + ((overflow*.95)/total_cost)
        
        reply="Newest planet scan on %s:%s:%s (id: %s, pt: %s)" % (p.x,p.y,p.z,rand_id,tick)
        reply+=" can purchase %s: %s"%(ship.name,int(buildable))
        
        for gov in PA.options("govs"):
            bonus = PA.getfloat(gov, "prodcost")
            if bonus == 0:
                continue
            reply+=" | %s: %s"%(PA.get(gov, "name"),int(buildable/(1+bonus)))
        
        factory_usage=getattr(planetscan,class_factory_table[ship.class_])
        if prod_res > 0 and factory_usage != "None":
            max_prod_modifier=prod_modifier_table[factory_usage]
            buildable_from_prod = buildable + max_prod_modifier*prod_res/total_cost
            reply+=" Counting %s res in prod at %s usage:" % (self.num2short(prod_res),factory_usage)
            reply+=" %s"%(int(buildable_from_prod))
            
            for gov in PA.options("govs"):
                bonus = PA.getfloat(gov, "prodcost")
                if bonus == 0:
                    continue
                reply+=" | %s: %s"%(PA.get(gov, "name"),int(buildable_from_prod/(1+bonus)))
        
        message.reply(reply)
