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
 
import re
from Core.config import Config
from Core.db import session
from Core.maps import Planet, Alliance, User, Intel
from Core.loadable import loadable, route, require_user

class pref(loadable):
    """Set your planet, password for the webby, email and phone number; order doesn't matter"""
    usage = " [planet=x.y.z] [password=pass] [email=my.email@address.com] [phone=999] [pubphone=T|F] [smsmode=clickatell|google|both]"
    planet_coordre = re.compile(loadable.planet_coord)
    
    @route(r"")
    @require_user
    def show_prefs(self, message, user, params):
        reply = ""
        if user.planet is not None:
            reply += " planet=%s:%s:%s" % (user.planet.x,user.planet.y,user.planet.z,)
        if user.email:
            reply += " email=%s" % (user.email,)
        if user.phone:
            reply += " phone=%s pubphone=%s" % (user.phone, str(user.pubphone)[0],)
            if user.smsmode is not None:
                reply += " smsmode=%s" % (user.smsmode[0],)
        if len(reply) > 0:
            message.reply("Your preferences are:" + reply)
        else:
            message.reply("You haven't set any preferences, use !help pref to view the options")
    
    @route(r"(.+)")
    @require_user
    def set_prefs(self, message, user, params):
        
        params = self.split_opts(params.group(1))
        reply = ""
        for opt, val in params.items():
            if opt == "planet":
                m = self.planet_coordre.match(val)
                if m:
                    planet = Planet.load(*m.group(1,3,5))
                    if planet is None:
                        message.alert("No planet with coords %s:%s:%s" % m.group(1,3,5))
                        continue
                    user.planet = planet
                    reply += " planet=%s:%s:%s"%(planet.x,planet.y,planet.z)
                    if user.is_member():
                        alliance = Alliance.load(Config.get("Alliance","name"))
                        if planet.intel is None:
                            planet.intel = Intel(nick=user.name, alliance=alliance)
                        else:
                            planet.intel.nick = user.name
                            planet.intel.alliance = alliance
                elif val in self.nulls:
                    user.planet = None
                    reply += " planet=None"
            if opt == "password":
                if message.in_chan():
                    message.reply("Don't set your password in public you shit")
                    continue
                user.passwd = val
                reply += " password=%s"%(val)
            if opt == "email":
                try:
                    user.email = val
                except AssertionError:
                    pass
                else:
                    reply += " email=%s"%(val)
            if opt == "phone":
                if val in self.nulls:
                    user.phone = ""
                    reply += " phone=None"
                else:
                    user.phone = val
                    reply += " phone=%s"%(val)
            if opt == "pubphone":
                if val.lower() in self.true:
                    user.pubphone = True
                    reply += " pubphone=%s"%(True)
                elif val.lower() in self.false:
                    user.pubphone = False
                    reply += " pubphone=%s"%(False)
            if opt == "smsmode":
                if Config.get("Misc", "sms") != "combined":
                    message.alert("Your alliance doesn't support SMS mode switching")
                    continue
                if val[:1].lower() == "c":
                    user.googlevoice = False
                    reply += " smsmode=clickatell"
                elif val[:1].lower() == "g":
                    user.googlevoice = True
                    reply += " smsmode=googlevoice"
                elif val[:1].lower() == "b" or val in self.nulls:
                    user.googlevoice = None
                    reply += " smsmode=None"
        
        session.commit()
        if len(reply) > 0:
            message.reply("Updated your preferences:"+reply)
