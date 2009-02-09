# bigdicks

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

from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class bigdicks(loadable):
    """BEEFCAKE!!!11onetwo"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = self.commandre
    
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):
        
        alliance = M.DB.Maps.Alliance.load(message.botally)
        if alliance is None:
            message.reply("No alliance matching '%s' found"%(message.botally,))
            return
        session = M.DB.Session()
        Q = session.query(M.DB.Maps.User, M.DB.Maps.epenis)
        Q = Q.join(M.DB.Maps.User.epenis)
        Q = Q.order_by(M.DB.SQL.desc(M.DB.Maps.epenis.rank))
        result = Q[:5]
        session.close()

        if len(result) < 1:
            msg.alert("There is no penis")
            return
        reply="Big dicks:"
        prev = []
        for user, penis in result:
            prev.append("%d:%s (%s)"%(penis.rank, user.name, self.num2short(penis.penis)))
        reply="Big dicks: " + ", ".join(prev)
        message.reply(reply)
