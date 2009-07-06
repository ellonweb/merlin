# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

# Used for calculating production times of ships.

import math
import re
from .Core.modules import M
loadable = M.loadable.loadable
from Hooks.ships import feud

class prod(loadable):
    """Calculate ticks it takes to produce <number> <ships> with <factories>."""
    def __init__(self):

        loadable.__init__(self)
        self.paramre = re.compile(r"\s(\d+(?:\.\d+)?[km]?)\s(\S+)\s(\d+)")
        self.usage += " <number> <ship> <factories>."

    @loadable.run
    def execute(self, message, user, params):
        
        num, name, factories = params.groups()

        ship = M.DB.Maps.Ship.load(name=name)
        if ship is None:
            message.alert("%s is not a ship." % name)
            return
        num = self.short2num(num)
        factories = int(factories)

        ticks, feud_ticks = self.calc_ticks(ship, num, factories)

        message.reply("It will take %s ticks to build %s %s, or with feudalism %s ticks." % (
                ticks, self.num2short(num), ship.name, feud_ticks))

    def calc_ticks(self, ship, num, factories):
        """Calculate the cost in ticks. Return (ticks, ticks_with_feudalism)."""

        cost = number * ship.total_cost
        ln = lambda x: math.log(x) / math.log(math.e)
        required = 2 * math.sqrt(cost) * ln(cost)
        feud = 2 * math.sqrt(cost * 0.85) * ln(cost)
        output = int((4000 * factories) ** 0.98)
        ticks = int(math.ceil((required + 10000 * factories) / output))
        feud_ticks = int(1.2 * math.ceil((feud + 10000 * factories) / output))

        return ticks, feud_ticks
