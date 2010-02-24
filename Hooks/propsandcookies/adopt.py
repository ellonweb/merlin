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
 
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable, route, require_user, channel

class adopt(loadable):
    """Adopt an orphan"""
    usage = " <pnick>"
    
    @route(r"(\S+)", access = "member")
    @channel("home")
    @require_user
    def execute(self, message, user, params):
        
        adoptee = params.group(1)
        if adoptee.lower() == Config.get("Connection","nick").lower():
            message.reply("Fuck off you stupid twat, stop trying to be a clever shit.")
            return
        if adoptee.lower() == user.name.lower():
            message.reply("Stop wanking your own dick and find a daddy to do it for you, retard.")
            return
        
        a = User.load(name=adoptee, access="member")
        if a is None:
            message.reply("No members matching '%s'"%(adoptee,))
            return

        s = User.load(name=a.sponsor, access="member") if a.sponsor else None
        if s is not None:
            message.reply("%s already has a daddy you filthy would-be kidnapper!"%(a.name,))
            return
        
        anc = user.has_ancestor(a.name)
        if anc is True:
            message.reply("Ew, incest.")
            return
        if anc is None:
            message.reply("Filthy orphans should be castrated.")
            return
        
        a.sponsor = user.name
        session.commit()
        message.reply("Congratulations! You're now the proud father of a not-so newly born %s!"%(a.name,))
