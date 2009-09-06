# Lookup a user's phone

import re
from Core.config import Config
from Core.db import session
from Core.maps import User, PhoneFriend
from Core.loadable import loadable

@loadable.module()
class phone(loadable):
    """Lookup someone's phone number or set permissions for who can view your number if you've not set public (pref)"""
    paramre = re.compile(r"\s(list|allow|deny|show)(?:\s(\S+))?",re.I)
    usage = " <list|allow|deny|show> [pnick]"
    
    @loadable.require_user
    def execute(self, message, user, params):

        # assign param variables
        command=params.group(1)
        trustee=params.group(2)

        if command.lower() == "list":
            # List of users than can see your phonenumber
            friends = user.phonefriends
            if len(friends) < 1:
                message.reply("You have no friends. How sad. Maybe you should go post on http://grouphug.us or something.")
                return
            reply="The following people can view your phone number:"
            for friend in friends:
                reply += " "+friend.name
            message.reply(reply)
            return

        if trustee is None:
            message.alert("None is not a valid user, retard.")
            return
        member = User.load(name=trustee,exact=False,session=session)
        if member is None:
            message.alert("%s is not a valid user."%(trustee,))
            return

        if command.lower() == "allow":
            # Add a PhoneFriend
            if member in user.phonefriends:
                reply="%s can already access your phone number."%(member.name,)
            else:
                user.phonefriends.append(member)
                session.commit()
                reply="Added %s to the list of people able to view your phone number."%(member.name,)
            message.reply(reply)
            return

        if command.lower() == "deny":
            # Remove a PhoneFriend
            friends = user.phonefriends
            if member not in friends:
                reply="Could not find %s among the people allowed to see your phone number." % (member.name,)
            else:
                session.query(PhoneFriend).filter_by(user=user, friend=member).delete(synchronize_session=False)
                session.commit()
                reply="Removed %s from the list of people allowed to see your phone number." % (member.name,)
            message.reply(reply)
            return

        if command.lower() == "show":
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
