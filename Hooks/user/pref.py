# Set your preferences

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
from .Core.modules import M
loadable = M.loadable.loadable

class pref(loadable):
    """Set your planet, password for the webby, email and phone number; order doesn't matter"""
    
    def __init__(self):
        loadable.__init__(self)
        self.access = 0
        self.paramre = re.compile(r"\s(.+)")
        self.usage += " [planet=x.y.z] [pass=password] [email=my.email@address.com] [phone=999]"
        self.emailre = re.compile("^([\w.]+@[\w.]+)")
    
    def execute(self, message):
        user, params = loadable.execute(self, message) or (None,None)
        if not params:
            return
        
        params = self.split_opts(params.group(1))
        pl = pw = em = ph = ""
        for opt, val in params.items():
            if opt == "planet":
                m = self.planet_coordre.search(val)
                if m:
                    #target = Planet(coords=m.groups()) <-- load the planet, check it exists and all that
                    pl = val
                    #user.hash = target.hash <-- planet_id, planet_cannon etc
            if opt == "pass":
                pw = val
                user.passwd = pw
            if opt == "email" and self.emailre.search(val):
                em = val
                user.email = em
            if opt == "phone":
                ph = val
                user.phone = ph
        session = M.DB.Session()
        session.add(user)
        session.commit()
        session.close()
        message.reply("Updated your preferences: planet=%s pass=%s email=%s phone=%s" % (pl,pw,em,ph,))
    
callbacks = [("PRIVMSG", pref())]