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
 
from sqlalchemy import or_
from sqlalchemy.sql import asc, desc
from Core.db import session
from Core.maps import Planet, Alliance, Intel
from Core.loadable import loadable, route

class supersearch(loadable):
    """Advanced planet/intel search: alliance, nick, reportchan, amps, dists, size, value, race, comment"""
    usage = "[option=value]+ [comment=key words]"
    
    @route("(.+)", access = "galmate")
    def search(self, message, user, params):
        Q = session.query(Planet, Intel)
        Q = Q.join(Planet.intel)
        
        alliance = None
        nick = None
        reportchan = None
        amps = None
        dists = None
        size = None
        value = None
        race = None
        comment = None
        
        sort = None
        order =  {"score" : (asc(Planet.score_rank),),
                  "value" : (asc(Planet.value_rank),),
                  "size"  : (asc(Planet.size_rank),),
                  "xp"    : (asc(Planet.xp_rank),),
                  "amps"  : (desc(Intel.amps),),
                  "dists" : (desc(Intel.dists),),
                  "planet": (asc(Planet.x),asc(Planet.y),asc(Planet.z),),
                 }
        page = 1
        offset = 0
        
        params = self.split_opts(message.get_msg())
        for opt, val in params.items():
            if opt == "alliance":
                alliance = Alliance.load(val)
                if alliance is None:
                    message.alert("No alliances match %s" % (val,))
                    return
                Q = Q.filter(Intel.alliance == alliance)
            
            if opt == "nick":
                nick = val
                Q = Q.filter(or_(Intel.nick.ilike("%"+nick+"%"), Intel.fakenick.ilike("%"+nick+"%")))
            if opt == "reportchan":
                reportchan = val
                Q = Q.filter(Intel.reportchan.ilike(reportchan))
            
            if opt == "amps" and val.isdigit():
                amps = val
                Q = Q.filter(Intel.amps.op('>=')(amps))
                if not sort:
                    sort = order["amps"]
            if opt == "dists" and val.isdigit():
                dists = val
                Q = Q.filter(Intel.dists.op('>=')(dists))
                if not sort:
                    sort = order["dists"]
            
            if opt == "size" and (val.isdigit() or (val[0] in ('>','<',) and val[1:].isdigit())):
                if val[0] in ('>','<',):
                    smod = val[0] + '='
                    size = val[1:]
                else:
                    smod = '>='
                    size = val
                Q = Q.filter(Planet.size.op(smod)(size))
                if not sort:
                    sort = order["size"]
            if opt == "value" and (val.isdigit() or (val[0] in ('>','<',) and val[1:].isdigit())):
                if val[0] in ('>','<',):
                    vmod = val[0] + '='
                    value = val[1:]
                else:
                    vmod = '<='
                    value = val
                Q = Q.filter(Planet.value.op(vmod)(value))
                if not sort:
                    sort = order["value"]
            
            if opt == "race" and self.racere.match(val):
                race = val
                Q = Q.filter(Planet.race.ilike(race))
            
            if opt == "comment":
                comment = message.get_msg().split("comment=")[1]
                Q = Q.filter(Intel.comment.ilike(comment.replace(" ", "%")))
            
            if opt == "sort" and val in order:
                sort = order[val]
            
            if opt == "page" and val.isdigit():
                page = int(val) or 1
                offset = (page - 1) * 5
        
        if not sort:
            sort = order["score"]
        for order in sort:
            Q = Q.order_by(order)
        
        result = Q.limit(6).offset(offset).all()
        
        if len(result) < 1:
            reply="No"
            if race:
                reply+=" %s"%(race,)
            reply+=" planets"
            if alliance:
                reply+=" in Alliance: %s"%(alliance.name,)
            if nick:
                reply+=" with nick '%s'"%(nick,)
            if reportchan:
                reply+=" with reportchan '%s'"%(reportchan,)
            if amps:
                reply+=" with at least %s amps"%(amps,)
            if dists:
                reply+=" with at least %s dists"%(dists,)
            if comment:
                reply+=" with a comment like '%s'"%(comment,)
            if size:
                reply+=" Size %s %s" % (smod,size)
            if value:
                reply+=" Value %s %s" % (vmod,value)
            message.reply(reply)
            return
        
        replies = []
        for planet, intel in result[:5]:
            reply="%s:%s:%s (%s)" % (planet.x,planet.y,planet.z,planet.race)
            if value or size:
                reply+=" Value: %s Size: %s" % (planet.value,planet.size,)
            if amps:
                reply+=" Amps: %s" % (intel.amps,)
            if dists:
                reply+=" Dists: %s" % (intel.dists,)
            if reportchan:
                reply+=" Reportchan: '%s'" % (intel.reportchan,)
            if intel.nick:
                reply+=" Nick: %s" % (intel.nick,)
            if intel.alliance:
                reply+=" Alliance: %s" % (intel.alliance.name,)
            if comment:
                reply+=" Comment: '%s'" % (intel.comment,)
            replies.append(reply)
        if len(result) > 5:
            replies[-1]+=" (Too many results to list, please refine your search or use page=%s)" % (page+1,)
        message.reply("\n".join(replies))
