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
 
from ssl import SSLError
from urllib import urlencode
from urllib2 import urlopen, URLError
from Core.exceptions_ import SMSError
from Core.config import Config
from Core.loadable import loadable, route

class showmethemoney(loadable):
    
    @route(access = "member")
    def execute(self, message, user, params):
        
        username = Config.get("clickatell", "user")
        password = Config.get("clickatell", "pass")
        api_id = Config.get("clickatell", "api")

        get = urlencode({"user": Config.get("clickatell", "user"),
                         "password": Config.get("clickatell", "pass"),
                         "api_id": Config.get("clickatell", "api"),
                        })
        
        try:
            status, msg = urlopen("https://api.clickatell.com/http/getbalance", get).read().split(":")
        
            if status in ("Credit",):
                balance = float(msg.strip())
                if not balance:
                    message.reply("Help me help you. I need the kwan. SHOW ME THE MONEY")
                else:
                    message.reply("Current kwan balance: %d"%(balance,))
            elif status in ("ERR",):
                raise SMSError(msg.strip())
            else:
                message.reply("That wasn't supposed to happen. I don't really know what wrong. Maybe your mother dropped you.")
        
        except (URLError, SSLError, SMSError) as e:
            message.reply("Error sending message: %s" % (str(e),))
