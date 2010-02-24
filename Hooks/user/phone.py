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
 
from Core.config import Config
from Core.db import session
from Core.maps import User, PhoneFriend
from Core.loadable import loadable, route, require_user

class phone(loadable):
    """Lookup someone's phone number or set permissions for who can view your number if you've not set public (pref)"""
    usage = " <list|allow|deny|show> [pnick]"
    
    @route(r"list")
    @require_user
    def list(self, message, user, params):
        # List of users than can see your phonenumber
        friends = user.phonefriends
        if len(friends) < 1:
            message.reply("You have no friends. How sad. Maybe you should go post on http://grouphug.us or something.")
            return
        reply="The following people can view your phone number:"
        for friend in friends:
            reply += " "+friend.name
        message.reply(reply)
    
    @route(r"allow\s+(\S+)")
    @require_user
    def allow(self, message, user, params):
        trustee=params.group(1)
        member = User.load(name=trustee,exact=False)
        if member is None:
            message.alert("%s is not a valid user."%(trustee,))
            return
        
        # Add a PhoneFriend
        if member in user.phonefriends:
            reply="%s can already access your phone number."%(member.name,)
        else:
            user.phonefriends.append(member)
            session.commit()
            reply="Added %s to the list of people able to view your phone number."%(member.name,)
        message.reply(reply)
    
    @route(r"deny\s+(\S+)")
    @require_user
    def deny(self, message, user, params):
        trustee=params.group(1)
        member = User.load(name=trustee,exact=False)
        if member is None:
            message.alert("%s is not a valid user."%(trustee,))
            return
        
        # Remove a PhoneFriend
        friends = user.phonefriends
        if member not in friends:
            reply="Could not find %s among the people allowed to see your phone number." % (member.name,)
        else:
            session.query(PhoneFriend).filter_by(user=user, friend=member).delete(synchronize_session=False)
            session.commit()
            reply="Removed %s from the list of people allowed to see your phone number." % (member.name,)
        message.reply(reply)
    
    @route(r"show\s+(\S+)")
    @require_user
    def show(self, message, user, params):
        trustee=params.group(1)
        member = User.load(name=trustee,exact=False)
        if member is None:
            message.alert("%s is not a valid user."%(trustee,))
            return
        
        # Show a phone number
        # Instead of the no-public-Alki message, message.alert() will always return in private
        if user == member:
            if user.phone:
                reply="Your phone number is %s."%(user.phone,)
            else:
                reply="You haven't set your phone number. To set your phone number, do !pref phone=1-800-HOT-BIRD."
            message.alert(reply)
            return
        
        if member.pubphone and user.is_member():
            message.alert("%s says his phone number is %s"%(member.name,member.phone))
            return
        friends = member.phonefriends
        if user not in friends:
            message.reply("%s won't let you see their phone number. That paranoid cunt just doesn't trust you I guess."%(member.name,))
            return
        if member.phone:
            message.alert("%s says his phone number is %s"%(member.name,member.phone))
        else:
            message.reply("%s hasn't shared his phone number. What a paranoid cunt ."%(member.name,))
            return
