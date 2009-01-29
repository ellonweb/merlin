# apenis

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
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class apenis(loadable):
    """Schlong"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"apenis(?:\s([\w-]+))?")
        self.usage += " alliance"
    
    @loadable.run_with_access()
    def execute(self, message, user, params):
        
        if params.group(1) is not None:
            alliance = M.DB.Maps.Alliance.load(params.group(1))
            if alliance is None:
                message.alert("No alliances match %s" % (params.group(1),))
                return
        elif user.is_member():
            alliance = M.DB.Maps.Alliance.load(message.botally)
            if alliance is None:
                message.alert("No alliances match %s" % (message.botally,))
                return
        else:
            session = M.DB.Session()
            session.add(user)
            if user.planet is None or user.planet.alliance is None:
                message.alert("Make sure you've set your planet with !pref and alliance with !intel")
                session.close()
                return
            else:
                alliance = user.planet.alliance
                session.close()
        
        session = M.DB.Session()
        session.add(alliance)
        penis = alliance.apenis
        session.close()
        if penis is None:
            message.alert("No apenis stats matching %s" % (alliance.name,))
            return
        
        message.reply("apenis for %s is %s score long. This makes %s rank: %s apenis. The average peon is sporting a %s score epenis." % (
                        alliance.name, penis.penis, alliance.name, penis.rank, int(penis.penis/alliance.members),))
