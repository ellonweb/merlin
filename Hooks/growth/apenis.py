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
from Core.exceptions_ import PNickParseError
from Core.config import Config
from Core.db import session
from Core.maps import Alliance
from Core.loadable import loadable

@loadable.module()
class apenis(loadable):
    """Schlong"""
    usage = " alliance"
    paramre = re.compile(r"(?:\s(\S+))?")
    
    def execute(self, message, user, params):
        
        if params.group(1) is not None:
            alliance = Alliance.load(params.group(1), session=session)
            if alliance is None:
                message.alert("No alliances match %s" % (params.group(1),))
                return
        elif self.is_user(user) and user.is_member():
            alliance = Alliance.load(Config.get("Alliance","name"), session=session)
            if alliance is None:
                message.alert("No alliances match %s" % (Config.get("Alliance","name"),))
                return
        else:
            if not self.is_user(user):
                raise PNickParseError
            if user.planet is None or user.planet.alliance is None:
                message.alert("Make sure you've set your planet with !pref and alliance with !intel")
                return
            else:
                alliance = user.planet.alliance
        
        penis = alliance.apenis
        if penis is None:
            message.alert("No apenis stats matching %s" % (alliance.name,))
            return
        
        message.reply("apenis for %s is %s score long. This makes %s rank: %s apenis. The average peon is sporting a %s score epenis." % (
                        alliance.name, penis.penis, alliance.name, penis.rank, int(penis.penis/alliance.members),))
