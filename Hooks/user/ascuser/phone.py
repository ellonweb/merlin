import re
from .Core.modules import M
loadable = M.loadable.loadable

class phone(loadable):
    """Lookup someone's phone number or set permissions for who can view your number if you've not set public (pref)"""
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s(list|allow|deny|show)(?:\s([\w-]+))?",re.I)
        self.usage += " <list|allow|deny|show> [pnick]"
        
    @loadable.run_with_access() # any registered user can use this, even gal mates
    def execute(self, message, user, params):

        # assign param variables
        command=m.group(1)
        trustee=m.group(2)

        if command.lower() == "list":
            # List of users than can see your phonenumber
            session = M.DB.Session()
            session.add(user)
            friends = user.phonefriends
            session.close()
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
        member = M.DB.Maps.User.load(name=trustee,exact=False)
        if member is None:
            message.alert("%s is not a valid user."%(trustee,))
            return

        if command.lower() == "allow":
            # Add a PhoneFriend
            session = M.DB.Session()
            session.add(user)
            if member in user.phonefriends:
                reply="%s can already access your phone number."%(member.name,)
            else:
                user.phonefriends.append(member)
                session.commit()
                reply="Added %s to the list of people able to view your phone number."%(member.name,)
            session.close()
            message.reply(reply)
            return

        if command.lower() == "deny":
            # Remove a PhoneFriend
            session = M.DB.Session()
            session.add(user)
            friends = user.phonefriends
            if member not in friends:
                reply="Could not find %s among the people allowed to see your phone number." % (member.name,)
            else:
                session.query(M.DB.Maps.PhoneFriend).filter_by(user=user, friend=member).delete(synchronize_session=False)
                session.commit()
                reply="Removed %s from the list of people allowed to see your phone number." % (member.name,)
            session.close()
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
            session = M.DB.Session()
            session.add(member)
            friends = member.phonefriends
            session.close()
            if user not in friends:
                message.alert("%s won't let you see their phone number. That paranoid cunt just doesn't trust you I guess."%(member.name,))
                return
            if member.phone:
                message.alert("%s says his phone number is %s"%(member.name,member.phone))
            else:
                message.alert("%s hasn't shared his phone number. What a paranoid cunt ."%(member.name,))
            return
