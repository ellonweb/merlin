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
from Core.db import session
from Core.maps import Slogan
from Core.loadable import loadable

@loadable.module("member")
class remslogan(loadable):
    usage = " <slogan to remove>"
    paramre = re.compile(r"\s+(.*)")
    
    def execute(self, message, user, params):
        
        params = params.group(1)
        slogan, count = Slogan.search(params)
        if count < 1:
            reply = "No slogans matching '%s'" % (params,)
        if count > 1:
            reply = "There were %d slogans matching your search, I can only be bothered to delete one slogan at a time you demanding fuckwit" % (count,)
        if count == 1:
            session.delete(slogan)
            session.commit()
            reply="Removed: '%s'" % (slogan,)
        message.reply(reply)
