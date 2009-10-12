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
import re
from sqlalchemy.sql import asc, desc, literal
from sqlalchemy.sql.functions import current_timestamp
from Core.config import Config
from Core.db import session
from Core.maps import User, Invite, Kick, Vote
from Core.loadable import loadable

@loadable.module("member")
class prop(loadable):
    """A proposition is a vote to do something. For now, you can raise propositions to invite or kick someone. Once raised the proposition will stand until you expire it.  Make sure you give everyone time to have their say. Votes for and against a proposition are weighted by carebears. You must have at least 1 carebear to vote."""
    usage = " [<invite|kick> <pnick> <comment>] | [list] | [vote <number> <yes|no|abstain>] | [expire <number>] | [show <number>] | [cancel <number>] | [recent] | [search <pnick>]"
    paramre = (re.compile(r"\s+(invite|kick)\s+(\S+)\s+(.+)",re.I),
               re.compile(r"\s+(show|expire|cancel)\s+(\d+)",re.I),
               re.compile(r"\s+(vote)\s+(\d+)\s+(yes|no|abstain|veto)",re.I),
               re.compile(r"\s+(list|recent)",re.I),
               re.compile(r"\s+(search)\s+(\S+)",re.I),
               )
    
    @loadable.require_user
    def execute(self, message, user, params):
        
        mode = params.group(1).lower()
        if mode == "invite":
            pass
        elif mode == "kick":
            pass
        elif mode == "show":
            pass
        elif mode == "expire":
            pass
        elif mode == "cancel":
            pass
        elif mode == "vote":
            pass
        elif mode == "list":
            prev = []
            for id, person, result, type in self.get_open_props():
                prev.append("%s: %s %s"%(id,type,person))
            message.reply("Propositions currently being voted on: %s"%(", ".join(prev),))
        elif mode == "recent":
            prev = []
            for id, person, result, type in self.get_recent_props():
                prev.append("%s: %s %s %s"%(id,type,person,result[0].upper() if result else ""))
            message.reply("Recently expired propositions: %s"%(", ".join(prev),))
        elif mode == "search":
            search = params.group(2)
            prev = []
            for id, person, result, type in self.search_props(search):
                prev.append("%s: %s %s %s"%(id,type,person,result[0].upper() if result else ""))
            message.reply("Propositions matching '%s': %s"%(search, ", ".join(prev),))
    
    def base_prop_search(self):
        invites = session.query(Invite.id, Invite.person, Invite.vote_result, literal("invite")).filter_by(active=False)
        kicks = session.query(Kick.id, User.name, Kick.vote_result, literal("kick")).join(Kick.kicked).filter_by(active=False)
        return invites.union(kicks)
    
    def get_open_props(self):
        Q = self.base_prop_search().order_by(asc(Invite.id))
        return Q.all()
    
    def get_recent_props(self):
        Q = self.base_prop_search().order_by(desc(Invite.id))
        return Q[:10]
    
    def search_props(self, search):
        Q = self.base_prop_search().filter(Invite.person.ilike("%"+search+"%")).order_by(desc(Invite.id))
        return Q.all()
