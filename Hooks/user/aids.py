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
from Core.db import session
from Core.maps import User
from Core.loadable import loadable, route, require_user

class aids(loadable):
    """See who a user has sexed"""
    usage = " <pnick>"
    access = "member"
    
    @route(r"(\S+)")
    def user(self, message, user, params):

        # assign param variables 
        search=params.group(1)

        # do stuff here
        if search.lower() == Config.get("Connection","nick").lower():
            message.reply("I am %s. I gave aids to all you bitches." % (Config.get("Connection","nick"),))
            return

        whore = User.load(name=search,exact=False)
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return
        else:
            self.execute(message, user, whore)
    
    @route(r"")
    @require_user
    def me(self, message, user, params):
        self.execute(message, user, user)
    
    def execute(self, message, user, whore):
        bitches = whore.gimps

        reply=""
        if whore == user:
            reply+="You are %s." % (user.name,)
            if len(bitches) < 1:
                reply+=" You have greedily kept your aids all to yourself."
            else:
                reply+=" You have given aids to:"
                for bitch in bitches:
                    reply+=" "+bitch[0]
        else:
            if len(bitches) < 1:
                reply+="%s hasn't given anyone aids, what a selfish prick." %(whore.name,)
            else:
                reply+="%s has given aids to:" % (whore.name,)
                for bitch in bitches:
                    reply+=" "+bitch[0]

        message.reply(reply)
