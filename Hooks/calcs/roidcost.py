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
from Core.loadable import loadable, route

class roidcost(loadable):
    """Calculate how long it will take to repay a value loss capping roids."""
    usage = " <roids> <value_cost> [mining_bonus]"
    
    @route(r"(\d+)\s+(\d+(?:\.\d+)?[km]?)(?:\s+(\d+))?")
    def execute(self, message, user, params):
        
        roids, cost, bonus = params.groups()
        roids, cost, bonus = int(roids), self.short2num(cost), int(bonus or 0)
        mining = PA.getint("roids","mining")

        if roids == 0:
            message.reply("Another NewDawn landing, eh?")
            return

        mining=mining * ((float(bonus)+100)/100)

        repay = (cost*100)/(roids*mining)
        reply = "Capping %s roids at %s value with %s%% bonus will repay in %s ticks (%s days)" % (roids,self.num2short(cost),bonus,int(repay),int(repay/24))
        
        for gov in PA.options("govs"):
            bonus = PA.getfloat(gov, "prodcost")
            if bonus == 0:
                continue
            repay_b = repay/(1+bonus)
            reply += " %s: %s ticks (%s days)" % (PA.get(gov, "name"), int(repay_b), int(repay_b/24))
        
        message.reply(reply)
