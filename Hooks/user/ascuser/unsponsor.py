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

class unsponsor(loadable):
    """Unsponsor one of your gimps."""
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " pnick"
        
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):

        # assign param variables
        recruit=params.group(1)
        
        # do stuff here
        gimp = M.DB.Maps.Gimp.load(name=recruit)
        if gimp is None:
            message.alert("No gimp with that pnick exists!")
            return
        if gimp.sponsor is not user:
            message.alert("That's not your gimp!")
            return
        user.invites += 1
        session = M.DB.Session()
        session.add(user)
        session.delete(gimp)
        session.commit()
        session.close()
        message.reply("You have unsponsored '%s'." % (recruit,))
