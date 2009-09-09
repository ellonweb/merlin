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

class gimp(loadable):
    """List current gimps or give details of a specific gimp"""
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"(?:\s([\w-]+))?")
        self.usage += " [pnick]"
        
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):

        # assign param variables
        recruit=params.group(1)
        
        # do stuff here
        if recruit:
            gimp = M.DB.Maps.Gimp.load(name=recruit)
            if gimp is None:
                message.alert("No gimp with that pnick exists!")
                return
            message.reply("Gimp: %s, Sponsor: %s, Waiting: %d more hours, Comment: %s" % (gimp.name,gimp.sponsor.name,gimp.hoursleft(),gimp.comment))
            return
        else:
            session = M.DB.Session()
            gimps = session.query(M.DB.Maps.Gimp)
            if gimps.count() < 1:
                message.alert("There are currently no gimps up for recruit")
            else:
                reply="Current gimps (with sponsor):"
                for gimp in gimps:
                    reply += (" (gimp:%s,sponsor:%s (%d hours left))" % (gimp.name,gimp.sponsor.name,gimp.hoursleft()))
                message.reply(reply)
            session.close()
