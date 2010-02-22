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
 
from Core.exceptions_ import UserError
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable, route, require_user

class adduser(loadable):
    """Used to add new users with the specified pnick and access level"""
    usage = " <pnick> <access>"
    
    @route(r"\s+(.+)\s+(\S+)", access = "admin")
    @require_user
    def execute(self, message, user, params):
        
        pnicks = params.group(1)
        access = params.group(2)
        if not access.isdigit():
            try:
                access = Config.getint("Access",access)
            except Exception:
                message.reply("Invalid access level '%s'" % (access,))
                return
        else:
            access = int(access)
        
        if access > user.access:
            message.reply("You may not add a user with higher access to your own")
            return
        
        added = []
        exists = []
        for pnick in pnicks.split():
            member = User.load(name=pnick, active=False)
            if member is None:
                member = User(name=pnick, access=access, sponsor=user.name)
                session.add(member)
                added.append(pnick)
            elif not member.active:
                member.active = True
                member.access = access
                member.sponsor = user.name
                added.append(pnick)
            elif not member.is_member():
                member.access = access
                member.sponsor = user.name
                added.append(pnick)
            else:
                exists.append(pnick)
        session.commit()
        if len(exists):
            message.reply("Users (%s) already exist" % (",".join(exists),))
        if len(added):
            message.reply("Added users (%s) at level %s" % (",".join(added),access))
        if len(added) and access >= Config.getint("Access","member"):
            message.privmsg("adduser %s %s 399" %(Config.get("Channels","home"), ",".join(added),), "P")
    
    def check_access(self, message, access=None, user=None, channel=None):
        try:
            user = loadable.check_access(self, message, access, user, channel)
            if not self.is_user(user):
                raise UserError
            else:
                return user
        except UserError:
            if message.get_pnick() in Config.options("Admins"):
                return User(name=Config.get("Connection", "nick"), access=Config.getint("Access", "admin"))
            else:
                raise
