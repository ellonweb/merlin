# Sponsor a user

import re
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class sponsor(loadable):
    """Sponsor a new recruit that you will take responsibility for. You can invite your gimp after a set time period."""
    def __init__(self):
        loadable.__init__(self)
        self.access = access['member']
        self.paramre = re.compile(r"\s([\w-]+)\s(.*)")
        self.usage += " pnick comments"
        
    def execute(self, message):
        user, params = loadable.execute(self, message) or (None,None)
        if not params:
            return

        # assign param variables
        recruit=params.group(1)
        comment=params.group(2)
        
        # do stuff here
        member = M.DB.Maps.User.load(name=pnick, active=True)
        if member is not None:
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
        session.add(M.DB.Maps.Gimp(user, recruit, comment))
        session.commit()
        session.close()
        message.reply("You have sponsored '%s' (MAKE SURE THIS IS THE RECRUIT'S PNICK.) In 36 hours you may use the !invite command to make them a member. It is your responsibility to get feedback about their suitability as a member in this period" % (recruit,))
    
callbacks = [("PRIVMSG", sponsor())]