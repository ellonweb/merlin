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
 
import datetime
from sqlalchemy.sql.functions import current_timestamp
from Core.config import Config
from Core.db import session
from Core.maps import User, Cookie
from Core.loadable import loadable, route, require_user, channel

class cookie(loadable):
    """Cookies are used to give out carebears. Carebears are rewards for carefaces. Give cookies to people when you think they've done something beneficial for you or for the alliance in general."""
    usage = " [howmany] <receiver> <reason> | [stat]"
    access = "member"
    
    @route(r"\s+statu?s?")
    @require_user
    def stat(self, message, user, params):
        #Stats
        self.update_available_cookies(user)
        message.reply("You have %d cookies left until next bakeday, %s"%(user.available_cookies,user.name))
    
    @route(r"\s+(?:(\d+)\s+)?(\S\S+)\s+(\S.*)")
    @channel("home")
    @require_user
    def cookie(self, message, user, params):
        # Gief cookies!
        
        self.update_available_cookies(user)
        
        howmany=params.group(1)
        if howmany:
            howmany=int(howmany)
        else:
            howmany=1
        receiver=params.group(2)
        reason=params.group(3)
        
        if not self.can_give_cookies(user, howmany):
            message.reply("Silly, %s. You currently only have %s cookies to give out, but are trying to give out %s cookies. I'll bake you some new cookies tomorrow morning." % (user.name, user.available_cookies, howmany))
            return
        
        if receiver.lower() == Config.get('Connection','nick').lower():
            message.reply("Cookies? Pah! I only eat carrion.")
            return
        
        rec = User.load(receiver, exact=False, access="member")
        if not rec:
            message.reply("I don't know who '%s' is, so I can't very well give them any cookies can I?" % (receiver,))
            return
        if user == rec:
            message.reply("Fuck you, %s. You can't have your cookies and eat them, you selfish dicksuck."%(user.name,))
            return
        
        rec.carebears += howmany
        user.available_cookies -= howmany
        self.log_cookie(howmany, user, rec)
        session.commit()
        
        message.reply("%s said '%s' and gave %d cookie%s to %s, who stuffed their face and now has %d carebears"%(user.name,
                                                                                                                  reason,
                                                                                                                  howmany,
                                                                                                                  ["","s"][howmany>1],
                                                                                                                  rec.name,
                                                                                                                  rec.carebears))
    
    def update_available_cookies(self, user):
        now = datetime.datetime.now()
        now = datetime.datetime(now.year,now.month,now.day)
        if not user.last_cookie_date or (now - user.last_cookie_date).days > 0:
            user.available_cookies = Config.getint("Alliance","cookies")
            user.last_cookie_date = current_timestamp()
            session.commit()
    
    def can_give_cookies(self, user, howmany):
        if howmany > user.available_cookies:
            return False
        return True
    
    def log_cookie(self, howmany, user, rec):
        now = datetime.datetime.now()
        weeks = (now - datetime.datetime(now.year,1,1)).days / 7
        session.add(Cookie(year=now.year, week=weeks, howmany=howmany, giver=user, receiver=rec,))
