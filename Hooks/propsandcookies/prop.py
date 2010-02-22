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
from sqlalchemy.sql import asc, desc, literal, union
from sqlalchemy.sql.functions import current_timestamp, sum
from Core.config import Config
from Core.db import session
from Core.maps import Alliance, User, Invite, Kick, Vote
from Core.messages import PUBLIC_REPLY
from Core.loadable import loadable, route, require_user, channel

class prop(loadable):
    """A proposition is a vote to do something. For now, you can raise propositions to invite or kick someone. Once raised the proposition will stand until you expire it.  Make sure you give everyone time to have their say. Votes for and against a proposition are weighted by carebears. You must have at least 1 carebear to vote."""
    usage = " [<invite|kick> <pnick> <comment>] | [list] | [vote <number> <yes|no|abstain>] | [expire <number>] | [show <number>] | [cancel <number>] | [recent] | [search <pnick>]"
    access = "member"
    
    @route(r"\s+show\s+(\d+)")
    def show(self, message, user, params):
        id = params.group(1)
        prop = self.load_prop(id)
        if prop is None:
            message.reply("No proposition number %s exists (idiot)."%(id,))
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
            if len(veto) > 0:
                reply+= " Vetoing: "
                reply+= ", ".join(map(lambda x: x.voter.name, veto))
        
        message.reply(reply)
        
        if prop.active:
            vote = prop.votes.filter_by(voter=user).first()
            if vote is not None:
                reply = "You are currently voting '%s'"%(vote.vote,)
                if vote.vote not in ("abstain","veto",):
                    reply+= " with %s carebears"%(vote.carebears,)
                reply+= " on this proposition."
            else:
                reply = "You are not currently voting on this proposition."
            message.alert(reply)
        
        if not prop.active:
            reply = self.text_result(prop.vote_result.lower(), *self.sum_votes(prop))
            reply+= self.text_summary(prop)
            message.reply(reply)
    
    @route(r"\s+vote\s+(\d+)\s+(yes|no|abstain|veto)")
    @require_user
    def vote(self, message, user, params):
        id = params.group(1)
        vote = params.group(2).lower()
        prop = self.load_prop(id)
        if prop is None:
            message.reply("No proposition number %s exists (idiot)."%(id,))
            return
        if not prop.active:
            message.reply("You can't vote on prop %s, it's expired."%(id,))
            return
        if prop.proposer == user:
            message.reply("Arbitrary Munin rule #167: No voting on your own props.")
            return
        if prop.person == user.name and vote == 'veto':
            message.reply("You can't veto a vote to kick you.")
            return
        
        old_vote = prop.votes.filter(Vote.voter==user).first()
        prop.votes.filter(Vote.voter==user).delete()
        prop.votes.append(Vote(voter=user, vote=vote, carebears=user.carebears))
        session.commit()
        
        if old_vote is None:
            reply = "Set your vote on proposition %s as %s"%(id,vote,)
        else:
            reply = "Changed your vote on proposition %s from %s"%(id,old_vote.vote,)
            if old_vote.vote not in ("abstain","veto",):
                reply+= " (%s)"%(old_vote.carebears,)
            reply+= " to %s"%(vote,)
        if vote not in ("abstain","veto",):
            reply+= " with %s carebears"%(user.carebears,)
        reply+= "."
        message.reply(reply)
    
    @route(r"\s+list")
    def list(self, message, user, params):
        prev = []
        for id, person, result, type in self.get_open_props():
            prop_info = "%s: %s %s"%(id,type,person)
            vote = user.votes.filter_by(prop_id=id).first()
            if vote is not None and message.reply_type() is not PUBLIC_REPLY:
                prop_info += " (%s,%s)"%(vote.vote[0].upper(),vote.carebears)
            prev.append(prop_info)
        message.reply("Propositions currently being voted on: %s"%(", ".join(prev),))
    
    @route(r"\s+recent")
    def recent(self, message, user, params):
        prev = []
        for id, person, result, type in self.get_recent_props():
            prev.append("%s: %s %s %s"%(id,type,person,result[0].upper() if result else ""))
        message.reply("Recently expired propositions: %s"%(", ".join(prev),))
    
    @route(r"\s+search\s+(\S+)")
    def search(self, message, user, params):
        search = params.group(1)
        prev = []
        for id, person, result, type in self.search_props(search):
            prev.append("%s: %s %s %s"%(id,type,person,result[0].upper() if result else ""))
        message.reply("Propositions matching '%s': %s"%(search, ", ".join(prev),))
    
    @route(r"\s+invite\s+(\S+)\s+(.+)")
    @channel("home")
    @require_user
    def invite(self, message, user, params):
        person = params.group(1)
        u = User.load(name=person,access="member")
        if u is not None:
            message.reply("Stupid %s, that wanker %s is already a member."%(user.name,person))
            return
        if self.is_already_proposed_invite(person):
            message.reply("Silly %s, there's already a proposal to invite %s."%(user.name,person))
            return
        if not self.member_count_below_limit():
            message.reply("You have tried to invite somebody, but we have too many losers and I can't be bothered dealing with more than %s of you."%(Config.getint("Alliance", "members"),))
            return
        anc = user.has_ancestor(person)
        if anc is True:
            message.reply("Ew, incest.")
            return
        if anc is None:
            message.reply("Filthy orphans should be castrated.")
            return
        
        prop = Invite(proposer=user, person=person, comment_text=params.group(2))
        session.add(prop)
        session.commit()
        
        reply = "%s created a new proposition (nr. %d) to invite %s." %(user.name, prop.id, person)
        reply+= " When people have been given a fair shot at voting you can call a count using !prop expire %d."%(prop.id,)
        message.reply(reply)
    
    @route(r"\s+kick\s+(\S+)\s+(.+)")
    @channel("home")
    @require_user
    def kick(self, message, user, params):
        person = params.group(1)
        if person.lower() == Config.get("Connection","nick").lower():
            message.reply("I'll peck your eyes out, cunt.")
            return
        u = User.load(name=person,access="member")
        if u is None:
            message.reply("Stupid %s, you can't kick %s, they're not a member."%(user.name,person))
            return
        if self.is_already_proposed_kick(person):
            message.reply("Silly %s, there's already a proposal to kick %s."%(user.name,person))
            return
        if u.access > user.access:
            message.reply("Unfortunately I like %s more than you. So none of that."%(u.name,))
            return
        
        prop = Kick(proposer=user, kicked=u, comment_text=params.group(2))
        session.add(prop)
        session.commit()
        
        reply = "%s created a new proposition (nr. %d) to kick %s." %(user.name, prop.id, person)
        reply+= " When people have been given a fair shot at voting you can call a count using !prop expire %d."%(prop.id,)
        message.reply(reply)
    
    @route(r"\s+expire\s+(\d+)")
    @channel("home")
    @require_user
    def expire(self, message, user, params):
        id = params.group(1)
        prop = self.load_prop(id)
        if prop is None:
            message.reply("No proposition number %s exists (idiot)."%(id,))
            return
        if prop.proposer is not user and not user.is_admin():
            message.reply("Only %s may expire proposition %d."%(prop.proposer.name,id))
            return
        if prop.type == "invite" and not self.member_count_below_limit():
            message.reply("You have tried to invite somebody, but we have too many losers and I can't be bothered dealing with more than %s of you."%(Config.getint("Alliance", "members"),))
            return
        
        self.recalculate_carebears(prop)
        
        yes, no, veto = self.sum_votes(prop)
        passed = yes > no and veto <= 0
        vote_result = ['no','yes'][passed]
        
        reply = self.text_result(vote_result, yes, no, veto)
        reply+= self.text_summary(prop)
        message.reply(reply)
        
        if prop.type == "invite" and passed:
            pnick = prop.person
            access = Config.getint("Access", "member")
            member = User.load(name=pnick, active=False)
            if member is None:
                member = User(name=pnick, access=access, sponsor=prop.proposer.name)
                session.add(member)
            elif not member.active:
                member.active = True
                member.access = access
                member.sponsor = prop.proposer.name
            elif not member.is_member():
                member.access = access
                member.sponsor = prop.proposer.name
            message.privmsg("adduser %s %s 399" %(Config.get("Channels","home"), pnick,), "P")
            message.reply("%s has been added to %s and given member level access to me."%(pnick,Config.get("Channels","home")))
        
        if prop.type == "kick" and passed:
            idiot = prop.kicked
            if "galmate" in Config.options("Access"):
                idiot.access = Config.getint("Access","galmate")
            else:
                idiot.access = 0
            
            if idiot.planet is not None and idiot.planet.intel is not None:
                intel = idiot.planet.intel
                alliance = Alliance.load(Config.get("Alliance","name"))
                if intel.alliance == alliance:
                    intel.alliance = None
            
            message.privmsg("remuser %s %s"%(Config.get("Channels","home"), idiot.name,),'p')
            message.privmsg("ban %s *!*@%s.users.netgamers.org Your sponsor doesn't like you anymore"%(Config.get("Channels","home"), idiot.name,),'p')
            message.privmsg("note send %s A proposition to kick you from %s has been raised by %s with reason '%s' and passed by a vote of %s to %s."%(idiot.name,Config.get("Alliance","name"),prop.proposer.name,prop.comment_text,yes,no),'p')
            message.reply("%s has been reduced to \"galmate\" level and removed from the channel."%(idiot.name,))
        
        prop.active = False
        prop.closed = current_timestamp()
        prop.vote_result = vote_result
        session.commit()
    
    @route(r"\s+cancel\s+(\d+)")
    @channel("home")
    @require_user
    def cancel(self, message, user, params):
        id = params.group(1)
        prop = self.load_prop(id)
        if prop is None:
            message.reply("No proposition number %s exists (idiot)."%(id,))
            return
        if prop.proposer is not user and not user.is_admin():
            message.reply("Only %s may expire proposition %d."%(prop.proposer.name,id))
            return
        
        vote_result = "cancel"
        
        reply = self.text_result(vote_result, yes, no, veto)
        reply+= self.text_summary(prop)
        message.reply(reply)
        
        prop.active = False
        prop.closed = current_timestamp()
        prop.vote_result = vote_result
        session.commit()
    
    def member_count_below_limit(self):
        Q = session.query(User).filter(User.active == True).filter(User.access >= Config.getint("Access", "member"))
        return Q.count() < Config.getint("Alliance", "members")
    
    def is_already_proposed_invite(self, person):
        Q = session.query(Invite).filter(Invite.person.ilike(person)).filter_by(active=True)
        return Q.count() > 0
    
    def is_already_proposed_kick(self, person):
        Q = session.query(Kick).join(Kick.kicked).filter(User.name.ilike(person)).filter_by(active=True)
        return Q.count() > 0
    
    def load_prop(self, id):
        invite = session.query(Invite).filter_by(id=id).first()
        kick = session.query(Kick).filter_by(id=id).first()
        return invite or kick
    
    def recalculate_carebears(self, prop):
        Q = session.query(Vote, User.carebears).join(Vote.voter).filter(Vote.prop_id==prop.id)
        for vote, carebears in Q:
            vote.carebears = carebears
    
    def sum_votes(self, prop):
        yes = session.query(sum(Vote.carebears)).filter_by(prop_id=prop.id, vote="yes").scalar()
        no = session.query(sum(Vote.carebears)).filter_by(prop_id=prop.id, vote="no").scalar()
        veto = session.query(Vote).filter_by(prop_id=prop.id, vote="veto").count()
        return yes, no, veto
    
    def text_result(self, vote_result, yes, no, veto):
        reply = "The prop"
        if vote_result == "cancel":
            reply+= " was cancelled with %s votes for, %s against and %s vetos"%(yes,no,veto)
        elif veto > 0:
            reply+= " failed because of %s vetos"%(veto)
        elif vote_result == "yes":
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
            reply+= ", ".join([vote.voter.name for vote in veto])
            reply+= ")."
        
        return reply
    
    def delete_prop(self, prop):
        prop.votes.delete()
        session.delete(prop)
        session.commit()
    
    def base_props_selectable(self):
        invites = session.query(Invite.id, Invite.person, Invite.vote_result, literal("invite").label("type"), Invite.active)
        kicks = session.query(Kick.id, User.name, Kick.vote_result, literal("kick").label("type"), Kick.active).join(Kick.kicked)
        props = union(invites, kicks).alias("prop")
        return props
    
    def get_open_props(self):
        props = self.base_props_selectable()
        Q = session.query(props.c.id, props.c.person, props.c.vote_result, props.c.type)
        Q = Q.filter(props.c.active==True).order_by(asc(props.c.id))
        return Q.all()
    
    def get_recent_props(self):
        props = self.base_props_selectable()
        Q = session.query(props.c.id, props.c.person, props.c.vote_result, props.c.type)
        Q = Q.filter(props.c.active==False).order_by(desc(props.c.id))
        return Q[:10]
    
    def search_props(self, search):
        props = self.base_props_selectable()
        Q = session.query(props.c.id, props.c.person, props.c.vote_result, props.c.type)
        Q = Q.filter(props.c.person.ilike("%"+search+"%")).order_by(desc(props.c.id))
        return Q.all()
