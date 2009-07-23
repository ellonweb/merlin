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

import re
from .Core.modules import M
loadable = M.loadable.loadable
from Hooks.ships import feud

class roidsave(loadable):
    """Tells you how much value will be mined by a number of roids in that many ticks. M=Max, F=Feudalism, D=Democracy."""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s+(\d+)\s+(\d+)(?:\s+(\d+))?")
        self.usage += " <roids> <ticks> [mining_bonus]"
    
    @loadable.run
    def execute(self, message, user, params):
        
        roids=int(params.group(1))
        ticks=int(params.group(2))
        bonus=int(params.group(3) or 0)
        mining = 250

        mining = int(mining *(float(bonus+100)/100))
        cost=self.num2short(ticks*roids*mining/100)

        cost_m=self.num2short(int(ticks*roids*mining/100*1.9529))
        cost_f=self.num2short(int(ticks*roids*mining/100*(1/(1-float(feud)))))
        cost_d=self.num2short(int(ticks*roids*mining/100*.9524))

        reply="%s roids with %s%% bonus will mine %s value (M: %s/F: %s/D: %s) in %s ticks (%s days)" % (roids,bonus,cost,cost_m,cost_f,cost_d,ticks,ticks/24)

        message.reply(reply)
