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
 
from Core.maps import Quote
from Core.loadable import loadable, route

class quote(loadable):
    @route(r"(.*)")
    def execute(self, message, user, params):
        
        params = params.group(1)
        quote, count = Quote.search(params)
        reply = str(quote)
        if count < 1:
            reply = "No quotes matching '%s'" % (params,)
        if count > 1 and params:
            reply+=" (%d more quotes match this search)" % (count - 1,)
        message.reply(reply)
