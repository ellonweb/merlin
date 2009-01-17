# Invite: add gimp

import re
from .variables import channels, access
from .Core.modules import M
loadable = M.loadable.loadable

class invite(loadable):
    """This command adds a recruit to the private channel and gives them access to me. Since this is done automatically, make sure P is online and responding before you do this. You should also make sure that you correctly typed the person's pnick when you sponsored them."""
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " pnick"
        
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):

        # assign param variables
        recruit=params.group(1)
        
        # do stuff here
        gimp = M.DB.Maps.Gimp.load(name=recruit)
        if gimp is None:
            message.alert("No gimp with that pnick exists!")
            return
        if gimp.sponsor is not user:
            message.alert("That's not your gimp!")
            return
        if gimp.hoursleft() > 0:
            message.alert("Sponsorship of %s hasn't finished, you need to wait another %s hours!" %(gimp.name,gimp.hoursleft(),))
            return
        # check if the user already exists
        recruit = M.DB.Maps.User.load(name=gimp.name, exact=True, active=False)
        if recruit is None:
            recruit = M.DB.Maps.User(name=gimp.name)
        recruit.active = True
        recruit.access |= access['member']
        recruit.sponsor = user.name
        session = M.DB.Session()
        session.add(recruit)
        session.delete(gimp)
        session.commit()
        session.close()
        message.privmsg('P',"adduser #%s %s 399" %(channels['private'], recruit.name,))
        message.privmsg('P',"modinfo #%s automode %s op" %(channels['private'], recruit.name,))
        reply="You have successfully invited '%s'. The gimp is now your responsibility. If they fuck up and didn't know, it's your fault. So teach them well." % (recruit.name,)
    
callbacks = [("PRIVMSG", invite())]