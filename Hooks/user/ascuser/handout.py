# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
 
import re
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class handout(loadable):
    """Handout invites to active members."""
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"(?:\s(\d+))?(?:\s([\w-]+))?")
        self.usage += " [number] [pnick]"
        
    @loadable.run_with_access(access['admin'])
    def execute(self, message, user, params):

        # assign param variables 
        num_invites=int(param.group(1) or 1)
        to_nick=param.group(2)
        
        # do stuff here
        if to_nick:
            member = M.DB.Maps.User.load(name=to_nick)
            if (member is None) or not idiot.is_member():
                message.alert("Could not find any users with that pnick!")
                return
            member.invites += num_invites
            session = M.DB.Session()
            session.add(member)
            session.commit()
            session.close()
            message.reply("Added %d invites to user '%s'" %(num_invites,to_nick))
        else:
            session = M.DB.Session()
            Q = session.query(M.DB.Maps.User)
            Q = Q.filter(M.DB.Maps.User.active == True)
            Q = Q.filter(M.DB.Maps.User.access & access['member'] == access['member'])
            Q.update({"invites": M.DB.Maps.User.invites + num_invites}, synchronize_session=False)
            session.commit()
            session.close()
            message.reply("Added %d invites to all members" %(num_invites,))
