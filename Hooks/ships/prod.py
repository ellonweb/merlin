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
 
from math import ceil, floor, e, log, sqrt
from Core.paconf import PA
from Core.maps import Ship
from Core.loadable import loadable, route

class prod(loadable):
    """Calculate ticks it takes to produce <number> <ships> with <factories>. Specify population and/or government for bonuses."""
    usage = " <number> <ship> <factories> [population] [government]"
    
    @route(r"(\d+(?:\.\d+)?[km]?)\s+(\S+)\s+(\d+)(?:\s+(.*))?")
    def execute(self, message, user, params):
        
        num, name, factories = params.group(1,2,3)

        ship = Ship.load(name=name)
        if ship is None:
            message.alert("%s is not a ship." % name)
            return
        num = self.short2num(num)
        factories = int(factories)

        race = ship.race[:3].lower()
        race = "etd" if race == "eit" else race

        gov = None
        pop = 0
        for p in (params.group(4) or "").split():
            m=self.govre.match(p)
            if m and not gov:
                gov=m.group(1).lower()
                continue
            if p.isdigit() and not pop:
                pop = int(p)
                continue

        m = ship.metal
        c = ship.crystal
        e = ship.eonium
        bonus = 1 + pop/100.0
        if gov:
            m *= (1+PA.getfloat(gov,"prodcost"))
            c *= (1+PA.getfloat(gov,"prodcost"))
            e *= (1+PA.getfloat(gov,"prodcost"))
            bonus += PA.getfloat(gov,"prodtime")
        if race:
            bonus += PA.getfloat(race,"prodtime")
        cost = floor(m)+floor(c)+floor(e)
        print cost

        ticks = self.calc_ticks(cost, num, bonus, factories)

        reply = "It will take %s ticks to build %s %s (%s)" % (ticks, self.num2short(num), ship.name, self.num2short(num*ship.total_cost/100))
        reply += " using %s factories" % (factories,) if factories > 1 else ""
        reply += " with a" if race or gov else ""
        reply += " %s"%(PA.get(gov,"name"),) if gov else ""
        reply += " %s"%(PA.get(race,"name"),) if race else ""
        reply += " planet" if race or gov else ""
        reply += " with %s%% population"%(pop,) if pop else ""
        message.reply(reply)

    def calc_ticks(self, cost, num, bonus, factories):
        """Calculate the cost in ticks."""

        ln = lambda x: log(x) / log(e)
        norm_cost = num * cost
        norm_req = sqrt(norm_cost) * ln(norm_cost**2)
        output = int(((4000 * factories) ** 0.98) * bonus)
        norm_ticks = int(ceil((norm_req + 10000 * factories) / output))

        return norm_ticks
