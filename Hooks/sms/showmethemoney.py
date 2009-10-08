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
 
from clickatell import Clickatell
from Core.config import Config
from Core.loadable import loadable

@loadable.module(100)
class showmethemoney(loadable):
    
    def execute(self, message, user, params):
        
        username = Config.get("clickatell", "user")
        password = Config.get("clickatell", "pass")
        api_id = Config.get("clickatell", "api")

        ct = Clickatell(username, password, api_id)
        if not ct.auth():
            message.reply("Could not authenticate with server. Super secret message not sent.")
            return

        balance = ct.getbalance()

        if not balance:
            reply="Help me help you. I need the kwan. SHOW ME THE MONEY"
        else:
            reply="Current kwan balance: %d"%(float(balance),)

        message.reply(reply)
