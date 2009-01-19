# Edit a user

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

class edituser(loadable):
    """Used to set and unset a user's permissions, seperated by commas; order doesn't matter"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)\s(.+)")
        self.usage += " user [set=[access,]*] [unset=[access,]*] [active=1]"
    
    @loadable.run_with_access(access['admin'] | access.get('hc',0))
    def execute(self, message, user, params):
        
        username = params.group(1)
        params = self.split_opts(params.group(2))
        
        member = M.DB.Maps.User.load(name=username, exact=False, active=False)
        if member is None:
            message.alert("No such user '%s'" % (username,))
            return
        sperm = uperm = active = ""
        for opt, val in params.items():
            if opt == "set":
                for lvl in val.split(","):
                    lvl = lvl.lower()
                    if access.has_key(lvl) and user.access/2 >= access[lvl]:
                        member.access = member.access | access[lvl]
                        sperm += " " + lvl
            if opt == "unset":
                for lvl in val.split(","):
                    lvl = lvl.lower()
                    if access.has_key(lvl) and user.access/2 >= access[lvl]:
                        if member.access & access[lvl]:
                            member.access = member.access ^ access[lvl]
                        uperm += " " + lvl
            if opt == "active" and (val == "1" or val == "0") and user.access/2 >= member.access:
                member.active = int(val)
                active += " " + val
        session = M.DB.Session()
        session.add(member)
        session.commit()
        session.close()
        message.reply("Editted user %s set: %s unset: %s active: %s" % (member.name, sperm, uperm, active,))
        if (not member.active) and M.CUT.Users.has_key(member.name):
            for nick in M.CUT.Users[member.name].nicks:
                nick.user = None
            del M.CUT.Users[member.name]
