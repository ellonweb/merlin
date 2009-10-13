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
        
        if mode in ("invite", "kick", "expire", "cancel",):
            self.execute2(message, user, params)
        
        elif mode == "show":
            id = params.group(2)
            prop = self.load_prop(id)
            if prop is None:
                message.reply("No proposition number %s exists."%(id,))
                return
            
            now = datetime.datetime.now()
            age = (now - prop.created).days
            reply = "proposition %s (%s days old):" %(prop.id,age,)
            reply+= " %s %s." %(prop.type,prop.person,)
            reply+= " %s commented '%s'." %(prop.proposer.name,prop.comment_text)
            
            if not prop.active:
                reply+= " This prop expired %d days ago."%((now-prop.closed).days,)
            
            if prop.active:
                veto = prop.votes.filter_by(vote="veto").all()
                if len(veto > 0):
                    reply+= " Vetoing: "
                    reply+= ", "join(map(lambda x: x.voter.name, veto))
            
            message.reply(reply)
            
            if prop.active:
                vote = prop.votes.filter_by(voter=user).first()
                if vote is not None:
                    reply = "You are currently voting '%s'"%(vote.vote,)
                    if vote.vote != "abstain":
                        reply+= " with %s carebears"%(vote.carebears,)
                    reply+= " on this proposition."
                else:
                    reply = " You are not currently voting on this proposition."
                message.alert(reply)
            
            if not prop.active:
                reply = self.text_result(prop)
                reply+= self.text_summary(prop)
                message.reply(reply)
        
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
    
    @loadable.channel("home")
    def execute2(self, message, user, params):
        mode = params.group(1).lower()
        
        if mode == "invite":
            person = params.group(2)
            u = User.load(name=person,access="member")
            if u is not None:
                message.reply("Stupid %s, that wanker %s is already a member."%(user.name,person))
                return
            if self.is_already_proposed_invite(person):
                message.reply("Silly %s, there's already a proposal to invite %s."%(user.name,person))
                return
            anc = user.has_ancestor(person)
            if anc is True:
                message.reply("Ew, incest.")
                return
            if anc is None:
                message.reply("Filthy orphans should be castrated.")
                return
            
            prop = Invite(proposer=user, person=person, comment_text=params.group(3))
            session.add(prop)
            session.commit()
            
            reply = "%s created a new proposition (nr. %d) to invite %s." %(user.name, prop.id, person)
            reply+= " When people have been given a fair shot at voting you can call a count using !prop expire %d."%(prop.id,)
            message.reply(reply)
        
        elif mode == "kick":
            person = params.group(2)
            if person.lower() == Config.get("Connection","nick").lower():
                message.reply("I'll peck your eyes out, cunt.")
                return
            u = User.load(name=person,access="member")
            if u is None:
                message.reply("Stupid %s, you can't kick %s, they're not a member."%(user.name,person))
                return
            if self.is_already_proposed_invite(person):
                message.reply("Silly %s, there's already a proposal to kick %s."%(user.name,person))
                return
            if u.access > user.access:
                message.reply("Unfortunately I like %s more than you. So none of that."%(u.name,))
                return
            
            prop = Kick(proposer=user, kicked=u, comment_text=params.group(3))
            session.add(prop)
            session.commit()
            
            reply = "%s created a new proposition (nr. %d) to kick %s." %(user.name, prop.id, person)
            reply+= " When people have been given a fair shot at voting you can call a count using !prop expire %d."%(prop.id,)
            message.reply(reply)
        
        elif mode == "expire":
            pass
        
        elif mode == "cancel":
            id = params.group(2)
            prop = self.load_prop(id)
            if prop is None:
                message.reply("No proposition number %s exists."%(id,))
                return
            
            if prop.proposer is not user and not user.is_admin():
                message.reply("Only %s may expire proposition %d."%(prop.proposer.name,id))
                return
            
            reply = "Cancelled proposal %s to %s %s" %(prop.id,prop.type,prop.person,)
            reply+= self.text_summary(prop)
            
            self.delete_prop(prop)
            message.reply(reply)
    
    def is_already_proposed_invite(self, person):
        Q = session.query(Invite).filter(Invite.person.ilike(person)).filter_by(active=True)
        return Q > 0
    
    def is_already_proposed_kick(self, person):
        Q = session.query(Kick).join(Kick.kicked).filter(User.name.ilike(person)).filter_by(active=True)
        return Q > 0
    
    def load_prop(self, id):
        invite = session.query(Invite).filter_by(id=id).first()
        kick = session.query(Kick).filter_by(id=id).first()
        return invite or kick
    
    def sum_votes(self, prop):
        yes = session.query(sum(Vote.carebears)).filter_by(prop_id=prop.id, vote="yes").scalar()
        no = session.query(sum(Vote.carebears)).filter_by(prop_id=prop.id, vote="no").scalar()
        veto = session.query(sum(Vote.carebears)).filter_by(prop_id=prop.id, vote="veto").scalar()
        return yes, no, veto
    
    def text_result(self, prop):
        yes, no, veto = self.sum_votes(prop)
        reply = "The prop"
        if veto > 0:
            reply+= " failed because of %s vetos"%(veto)
        elif yes > no:
            reply+= " passed by a vote of %s to %s"%(yes,no)
        else:
            reply+= " failed by a vote of %s to %s"%(no,yes)
        return reply
    
    def text_summary(self, prop):
        pretty_print=lambda x:"%s (%s)"%(x.voter.name,x.carebears)
        reply = ". The voters in favor were ("
        reply+= ", ".join(map(pretty_print,prop.votes.filter_by(vote="yes")))
        reply+= ") and against ("
        reply+= ", ".join(map(pretty_print,prop.votes.filter_by(vote="no")))
        reply+= ")."
        
        veto = prop.votes.filter_by(vote="veto").all()
        if len(veto) > 0:
            reply+= " Vetoing ("
            reply+= ", ".join([vote.user.name for vote in veto])
            reply+= ")."
        
        return reply
    
    def delete_prop(self, prop):
        prop.votes.delete()
        session.delete(prop)
        session.commit()
    
    def base_prop_search(self):
        invites = session.query(Invite.id, Invite.person, Invite.vote_result, literal("invite"))
        kicks = session.query(Kick.id, User.name, Kick.vote_result, literal("kick")).join(Kick.kicked)
        return invites.union(kicks)
    
    def get_open_props(self):
        Q = self.base_prop_search().filter_by(active=True).order_by(asc(Invite.id))
        return Q.all()
    
    def get_recent_props(self):
        Q = self.base_prop_search().filter_by(active=False).order_by(desc(Invite.id))
        return Q[:10]
    
    def search_props(self, search):
        Q = self.base_prop_search().filter(Invite.person.ilike("%"+search+"%")).order_by(desc(Invite.id))
        return Q.all()
