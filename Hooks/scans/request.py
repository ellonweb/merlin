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
 
# Request a scan

from sqlalchemy.sql import asc
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, User, Request
from Core.chanusertracker import CUT
from Core.loadable import loadable, route, require_user, robohci

class request(loadable):
    """Request a scan"""
    alias = "req"
    usage = " <x.y.z> <scantype> [dists] | <id> blocks <amps> | cancel <id> | list | links"
    
    @route(loadable.planet_coord+"\s+("+"|".join(PA.options("scans"))+r")\w*(?:\s+(\d+))?", access = "member")
    @require_user
    def execute(self, message, user, params):
        planet = Planet.load(*params.group(1,3,5))
        if planet is None:
            message.alert("No planet with coords %s:%s:%s" % params.group(1,3,5))
            return
        
        scan = params.group(6).upper()
        dists = int(params.group(7) or 0)
        
        request = self.request(message, user, planet, scan, dists)
        if message.get_chan() != self.scanchan():
            message.reply("Requested a %s Scan of %s:%s:%s. !request cancel %s to cancel the request." % (request.type, planet.x, planet.y, planet.z, request.id,))
    
    @robohci
    def robocop(self, message, request_id, mode):
        request = Request.load(request_id, active=False)
        if request is None:
            return
        
        if mode == "cancel":
            reply = "Cancelled scan request %s" % (request.id,)
            message.privmsg(reply, self.scanchan())
            nicks = CUT.list_user_nicks(request.user.name)
            for nick in nicks:
                message.privmsg(reply, nick)
            return
        
        if mode == "block":
            reply = "Updated request %s dists to %s" % (request.id, request.dists,)
            message.privmsg(reply, self.scanchan())
            nicks = CUT.list_user_nicks(request.user.name)
            for nick in nicks:
                message.privmsg(reply, nick)
            return
        
        user = request.user
        planet = request.target
        dists_intel = planet.intel.dists if planet.intel else 0
        message.privmsg("[%s] %s requested a %s Scan of %s:%s:%s Dists(i:%s/r:%s) " % (request.id, user.name, request.type, planet.x,planet.y,planet.z, dists_intel, request.dists,) + request.link, self.scanchan())
    
    def request(self, message, user, planet, scan, dists):
        request = Request(target=planet, scantype=scan, dists=dists)
        user.requests.append(request)
        session.commit()
        
        dists_intel = planet.intel.dists if planet.intel else 0
        message.privmsg("[%s] %s requested a %s Scan of %s:%s:%s Dists(i:%s/r:%s) " % (request.id, user.name, request.type, planet.x,planet.y,planet.z, dists_intel, request.dists,) + request.link, self.scanchan())
        
        return request
    
    @route(r"c(?:ancel)?\s+(\d+)", access = "member")
    @require_user
    def cancel(self, message, user, params):
        id = params.group(1)
        request = Request.load(id)
        if request is None:
            message.reply("No open request number %s exists (idiot)."%(id,))
            return
        if request.user is not user and not user.is_admin() and not self.is_chan(message, self.scanchan()):
            message.reply("Only %s may cancel request %s."%(request.user.name,id))
            return
        
        request.active = False
        session.commit()
        
        reply = "Cancelled scan request %s" % (id,)
        message.reply(reply)
        if message.get_chan() != self.scanchan():
            message.privmsg(reply, self.scanchan())
        
        nicks = CUT.list_user_nicks(request.user.name)
        if message.get_nick() not in nicks:
            for nick in nicks:
                message.privmsg(reply, nick)
    
    @route(r"(\d+)\s+b(?:lock(?:s|ed)?)?\s+(\d+)", access = "member")
    def blocks(self, message, user, params):
        id = params.group(1)
        dists = int(params.group(2))
        request = Request.load(id)
        if request is None:
            message.reply("No open request number %s exists (idiot)."%(id,))
            return
        
        request.dists = max(request.dists, dists)
        session.commit()
        
        reply = "Updated request %s dists to %s" % (id, request.dists,)
        message.reply(reply)
        if message.get_chan() != self.scanchan():
            message.privmsg(reply, self.scanchan())
        
        nicks = CUT.list_user_nicks(request.user.name)
        if message.get_nick() not in nicks:
            for nick in nicks:
                message.privmsg(reply, nick)
    
    @route(r"l(?:ist)?", access = "member")
    def list(self, message, user, params):
        Q = session.query(Request)
        Q = Q.filter(Request.tick > Updates.current_tick() - 5)
        Q = Q.filter(Request.active == True)
        Q = Q.order_by(asc(Request.id))
        
        if Q.count() < 1:
            message.reply("There are no open scan requests")
            return
        
        message.reply(" ".join(map(lambda request: "[%s: %s %s:%s:%s]" % (request.id, request.scantype, request.target.x, request.target.y, request.target.z,), Q.all())))
    
    @route(r"links?", access = "member")
    def links(self, message, user, params):
        Q = session.query(Request)
        Q = Q.filter(Request.tick > Updates.current_tick() - 5)
        Q = Q.filter(Request.active == True)
        Q = Q.order_by(asc(Request.id))
        
        if Q.count() < 1:
            message.reply("There are no open scan requests")
            return
        
        message.reply(" ".join(map(lambda request: "[%s: %s]" % (request.id, request.link,), Q[:5])))
    
    def scanchan(self):
        return Config.get("Channels", "scans") if "scans" in Config.options("Channels") else Config.get("Channels", "home")
