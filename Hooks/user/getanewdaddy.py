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
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable

@loadable.module("member")
class getanewdaddy(loadable):
    """Remove sponsorship of a member. Their access will be reduced to "galmate" level. Anyone is free to sponsor the person back under the usual conditions. This isn't a kick and it's not final.""" 
    usage = " pnick"
    paramre = re.compile(r"\s(\S+)")
    
    @loadable.require_user
    def execute(self, message, user, params):

        # do stuff here
        idiot = User.load(name=params.group(1), access="member")
        if idiot is None:
            message.reply("That idiot isn't a member!")
            return
        if (not user.is_admin()) and idiot.sponsor != user.name:
            message.reply("You are not %s's sponsor"%(idiot.name,))
            return
        
        if "galmate" in Config.options("Access"):
            idiot.access = Config.getint("Access","galmate")
        else:
            idiot.access = 0
        session.commit()
        message.privmsg('remuser %s %s'%(Config.get("Channels","home"), idiot.name,),'p')
        message.privmsg("ban %s *!*@%s.users.netgamers.org Your sponsor doesn't like you anymore"%(Config.get("Channels","home"), idiot.name,),'p')
        if idiot.sponsor != user.name:
            message.privmsg("note send %s Some admin has removed you for whatever reason. If you still wish to be a member, go ahead and find someone else to sponsor you back."%(idiot.name,),'p')
            message.reply("%s has been reduced to \"galmate\" level and removed from the channel. %s is no longer %s's sponsor. If anyone else would like to sponsor that person back, they may."%(idiot.name,idiot.sponsor,idiot.name))
        else:
            message.privmsg("note send %s Your sponsor (%s) no longer wishes to be your sponsor. If you still wish to be a member, go ahead and find someone else to sponsor you back."%(idiot.name,user.name,),'p')
            message.reply("%s has been reduced to \"galmate\" level and removed from the channel. You are no longer %s's sponsor. If anyone else would like to sponsor that person back, they may."%(idiot.name,idiot.name))
