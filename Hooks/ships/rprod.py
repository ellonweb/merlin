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
 
from math import floor, e, log, sqrt
from Core.paconf import PA
from Core.maps import Ship
from Core.loadable import loadable, route

class rprod(loadable):
    """Calculate how many <ship> you can build in <ticks> with <factories>. Specify population and/or government for bonuses."""
    usage = " <ship> <ticks> <factories> [population] [government]"
    dx = tolerance = 0.00001
    
    @route(r"(\S+)\s+(\d+)\s+(\d+)(?:\s+(.*))?")
    def execute(self, message, user, params):
        
        name, ticks, factories = params.group(1,2,3)

        ship = Ship.load(name=name)
        if ship is None:
            message.alert("%s is not a ship." % name)
            return
        ticks = int(ticks)
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

        res = int(self.revprod(ticks, factories, bonus))
        ships = int(res / cost)

        reply = "You can build %s %s (%s) in %d ticks" % (self.num2short(ships), ship.name, self.num2short(ships*ship.total_cost/PA.getint("numbers", "ship_value")), ticks)
        reply += " using %s factories" % (factories,) if factories > 1 else ""
        reply += " with a" if race or gov else ""
        reply += " %s"%(PA.get(gov,"name"),) if gov else ""
        reply += " %s"%(PA.get(race,"name"),) if race else ""
        reply += " planet" if race or gov else ""
        reply += " with %s%% population"%(pop,) if pop else ""
        message.reply(reply)

    def derive(self, f):
        """Numerical derivation of the function f."""

        return lambda x: (f(x + self.dx) - f(x)) / self.dx

    def close(self, a, b):
        """Is the result acceptable?"""

        return abs(a - b) < self.tolerance

    def newton_transform(self, f):
        """Do a newton transform of the function f."""

        return lambda x: x - (f(x) / self.derive(f)(x))

    def fixed_point(self, f, guess):
        """Fixed point search."""

        while not self.close(guess, f(guess)):
            guess = f(guess)
        return guess

    def newton(self, f, guess):
        """Generic equation solver using newtons method."""

        return self.fixed_point(self.newton_transform(f),
                                guess)

    def rpu(self, y):
        """Curry it."""

        return lambda x: 2 * sqrt(x) * log(x, e) - y

    def revprod(self, ticks, facs, bonus):
        """Reversed production formula."""

        output = ((4000 * facs) ** 0.98) * bonus
        return self.newton(self.rpu(ticks * output - 10000 * facs), 10)
