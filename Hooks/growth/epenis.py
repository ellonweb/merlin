# epenis

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

class epenis(loadable):
    """Penis"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"epenis(?:\s([\w-]+))?")
        self.usage += " user"
    
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):
        
        if params.group(1) is not None:
            penis = M.DB.Maps.User.load(name=params.group(1),exact=False)
        else:
            penis = user
        if penis is None:
            message.reply("Who the fuck is %s?" % (params.group(1),))
            return
        
        session = M.DB.Session()
        session.add(penis)
        if penis.planet is None:
            if user == penis:
                message.reply("Set your planet first git.")
            else:
                message.reply("%s is too embarrassed about his tiny penis that he won't let me tell you how small it is." % (penis.name,))
            session.close()
            return
        
        if penis.epenis is None:
            if user == penis:
                message.reply("Wait for the tick, bitch.")
            else:
                message.reply("That freak %s doesn't have a penis!" % (penis.name,))
            session.close()
            return
        
        message.reply("epenis for %s is %s score long. This makes %s rank: %s for epenis in %s!" % (
                        penis.name, penis.epenis.penis, penis.name, penis.epenis.rank, message.botally,))
        session.close()
