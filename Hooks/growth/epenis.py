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
 
from Core.config import Config
from Core.maps import User
from Core.loadable import loadable, route

class epenis(loadable):
    """Penis"""
    usage = " [user]"
    
    @route(r"(\S+)?", access = "member")
    def execute(self, message, user, params):
        
        if params.group(1) is not None:
            penis = User.load(name=params.group(1),exact=False,access="member")
        else:
            penis = user
        if not self.is_user(penis):
            message.reply("Who the fuck is %s?" % (params.group(1),))
            return
        
        if penis.planet is None:
            if user == penis:
                message.reply("Set your planet first git.")
            else:
                message.reply("%s is too embarrassed about his tiny penis that he won't let me tell you how small it is." % (penis.name,))
            return
        
        if penis.epenis is None:
            if user == penis:
                message.reply("Wait for the tick, bitch.")
            else:
                message.reply("That freak %s doesn't have a penis!" % (penis.name,))
            return
        
        message.reply("epenis for %s is %s score long. This makes %s rank: %s for epenis in %s!" % (
                        penis.name, penis.epenis.penis, penis.name, penis.epenis.rank, Config.get("Alliance","name"),))
