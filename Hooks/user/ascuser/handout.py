# Handout invites

import re
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class handout(loadable):
    """Handout invites to active members."""
    def __init__(self):
        loadable.__init__(self)
        self.access = access['admin']
        self.paramre = re.compile(r"(?:\s(\d+))?(?:\s([\w-]+))?")
        self.usage += " [number] [pnick]"
        
    def execute(self, message):
        user, params = loadable.execute(self, message) or (None,None)
        if not params:
            return

        # assign param variables 
        num_invites=int(param.group(1) or 1)
        to_nick=param.group(2)
        
        # do stuff here
        if to_nick:
            member = M.DB.Maps.User.load(name=to_nick)
            if (member is None) or not idiot.is_member():
                message.alert("Could not find any users with that pnick!")
                return
            member.invites += num_invites
            session = M.DB.Session()
            session.add(member)
            session.commit()
            session.close()
            message.reply("Added %d invites to user '%s'" %(num_invites,to_nick))
        else:
            session = M.DB.Session()
            Q = session.query(M.DB.Maps.User)
            Q = Q.filter(M.DB.Maps.User.active == True)
            Q = Q.filter(M.DB.Maps.User.access & access['member'] == access['member'])
            Q.update({"invites": M.DB.Maps.User.invites + num_invites}, synchronize_session=False)
            session.commit()
            session.close()
            message.reply("Added %d invites to all members" %(num_invites,))
    
callbacks = [("PRIVMSG", handout())]