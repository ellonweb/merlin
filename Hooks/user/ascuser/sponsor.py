# Sponsor a user

import re
from .variables import nick, access
from .Core.modules import M
loadable = M.loadable.loadable

class sponsor(loadable):
    def __init__(self):
        if M.DB.Maps.Gimp.wait == 0:
            self.__doc__ = """This command is used to sponsor a new recruit. When you sponsor someone, you suggest them for recuitment to the alliance and state that you will make sure they're at home and don't fuck up. Once you've sponsored someone you must ensure that there are absolutely no objections or I'm going to beat you up.
                              Once you've ensured that your gimp is generally accepted, you may use the !invite command to add them to the channel and %s. You may at any point withdraw your sponsorship by using the unsponsor command. You may view currently pending sponsorships with !gimp. If you have any questions, good luck finding useful answers.""" % (nick,)
        else:
            self.__doc__ = """This command is used to sponsor a new recruit. When you sponsor someone, you suggest them for recuitment to the alliance and state that you will make sure they're at home and don't fuck up. Once you've sponsored someone, make sure you speak to others about your possible invite, it is your responsibility to guarantee that they will be welcome.
                              After %s hours you may use the !invite command to add them to the channel and %s. You may at any point withdraw your sponsorship by using the unsponsor command. You may view currently pending sponsorships with !gimp. If you have any questions, good luck finding useful answers.""" % (M.DB.Maps.Gimp.wait, nick,)
        loadable.__init__(self)
        self.access = access['member']
        self.paramre = re.compile(r"\s([\w-]+)\s(.*)")
        self.usage += " pnick comments"
        
    def execute(self, message):
        user, params = loadable.execute(self, message) or (None,None)
        if not params:
            return

        if M.DB.Maps.Gimp.wait < 0:
            message.reply("Fuck off and stop watering down this elitist shithole.")
            return

        # assign param variables
        recruit=params.group(1)
        comment=params.group(2)
        
        # do stuff here
        member = M.DB.Maps.User.load(name=pnick, active=True)
        if (member is not None) and member.is_member():
            message.alert("A user with that pnick already exists!")
            return
        gimp = M.DB.Maps.Gimp.load(name=recruit)
        if gimp is not None:
            message.alert("A gimp with that pnick already exists!")
            return
        try:
            user.invites -= 1
        except AssertionError:
            message.alert("You do not have enough invites.")
            return
        session = M.DB.Session()
        session.add(user)
        session.add(M.DB.Maps.Gimp(sponsor_id=user.id, name=recruit, comment=comment))
        session.commit()
        session.close()
        if M.DB.Maps.Gimps.wait == 0:
            message.reply("You have sponsored '%s' (MAKE SURE THIS IS THE RECRUIT'S PNICK.) When you have ensured that there are no objections you may use the !invite command to make them a member." % (recruit,))
        else:
            message.reply("You have sponsored '%s' (MAKE SURE THIS IS THE RECRUIT'S PNICK.) In %s hours you may use the !invite command to make them a member. It is your responsibility to get feedback about their suitability as a member in this period." % (recruit,M.DB.Maps.Gimp.wait,))
    
callbacks = [("PRIVMSG", sponsor())]