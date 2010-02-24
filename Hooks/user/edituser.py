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
from Core.chanusertracker import CUT
from Core.loadable import loadable, route, require_user

class edituser(loadable):
    """Used to change a user's access or (de)activate them"""
    usage = " <user> (<access>|true|false)"
    
    @route(r"(\S+)\s+(\S+)", access = "admin")
    @require_user
    def execute(self, message, user, params):
        
        username = params.group(1)
        access = params.group(2).lower()
        if not access.isdigit() and access not in self.true and access not in self.false:
            try:
                access = Config.getint("Access",access)
            except Exception:
                message.reply("Invalid access level '%s'" % (access,))
                return
        elif access.isdigit():
            access = int(access)
        elif access in self.true:
            access = True
        elif access in self.false:
            access = False
        
        member = User.load(name=username, exact=False, active=False)
        if member is None:
            message.alert("No such user '%s'" % (username,))
            return
        
        if access > user.access or member.access > user.access:
            message.reply("You may not change access higher than your own")
            return
        
        mbraxx = Config.getint("Access","member")
        home = Config.get("Channels","home")
        
        if type(access) == int:
            if member.active == True and member.access < mbraxx and access >= mbraxx:
                message.privmsg("adduser %s %s 399" %(home, member.name,), "P")
                message.reply("%s has been added to %s"%(member.name, home,))
            if member.active == True and member.access >= mbraxx and access < mbraxx:
                message.privmsg("remuser %s %s"%(home, member.name,), "P")
                message.privmsg("ban %s *!*@%s.users.netgamers.org GTFO, EAAD"%(home, member.name,), "P")
            member.access = access
        else:
            if member.active != access and access == True and member.access >= mbraxx:
                message.privmsg("adduser %s %s 399" %(home, member.name,), "P")
                message.reply("%s has been added to %s"%(member.name, home,))
            if member.active != access and access == False and member.access >= mbraxx:
                message.privmsg("remuser %s %s"%(home, member.name,), "P")
                message.privmsg("ban %s *!*@%s.users.netgamers.org GTFO, EAAD"%(home, member.name,), "P")
            member.active = access
        session.commit()
        message.reply("Editted user %s access: %s" % (member.name, access,))
        if not member.active:
            CUT.untrack_user(member.name)
