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
 
from Core.db import session
from Core.maps import User
from Core.loadable import loadable, route, require_user

class alias(loadable):
    """Set an alias that maps to your pnick, useful if you have a different nick than your pnick and people use autocomplete."""
    usage = " <alias> (at most 15 characters)"
    
    @route(r"(\S{3,15})?")
    @require_user
    def execute(self, message, user, params):

        # assign param variables 
        alias=params.group(1)
        if alias is None:
            m = message.get_msg().split()
            if len(m) > 1 and m[1] in self.nulls:
                pass
            else:
                message.reply("You are %s, your alias is %s"%(user.name,user.alias,))
                return
            
        if alias is not None:
            if User.load(name=alias) is not None:
                message.reply("Your alias is already in use or is someone else's pnick (not allowed). Tough noogies.")
                return
            if session.query(User).filter(User.active==True).filter(User.alias.ilike(alias)).first() is not None:
                message.reply("Your alias is already in use or is someone else's pnick (not allowed). Tough noogies.")
                return
        
        user.alias = alias
        session.commit()
        message.reply("Update alias for %s (that's you) to %s"%(user.name,user.alias,))
