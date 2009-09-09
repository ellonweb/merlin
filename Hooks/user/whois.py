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
from Core.maps import User
from Core.loadable import loadable

@loadable.module("member")
class whois(loadable):
    """Lookup a user's details"""
    usage = " pnick"
    paramre = re.compile(r"\s(\S+)")
    
    def execute(self, message, user, params):

        # assign param variables 
        search=params.group(1)

        # do stuff here
        if search.lower() == Config.get("Connection","nick").lower():
            message.reply("I am %s. Hear me roar." % (Config.get("Connection","nick"),))
            return

        whore = User.load(name=search,exact=False)
        if whore is None or not whore.is_member():
            message.reply("No users matching '%s'"%(search,))
            return

        reply=""
        if whore == user:
            reply+="You are %s. Your sponsor is %s. You have %s invite%s left."
        else:
            reply+="Information about %s: Their sponsor is %s."
        reply=reply%(whore.name,whore.sponsor,)

        message.reply(reply)
