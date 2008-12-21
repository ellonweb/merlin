# List of gimps

import re
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class gimp(loadable):
    """List current gimps or give details of a specific gimp"""
    def __init__(self):
        loadable.__init__(self)
        self.access = access['member']
        self.paramre = re.compile(r"(?:\s([\w-]+))")
        self.usage += " [pnick]"
        
    def execute(self, message):
        user, params = loadable.execute(self, message) or (None,None)
        if not params:
            return

        # assign param variables
        recruit=params.group(1)
        
        # do stuff here
        if recruit:
            gimp = M.DB.Maps.Gimp.load(name=recruit)
            if gimp is None:
                message.alert("No gimp with that pnick exists!")
                return
            message.reply("Gimp: %s, Sponsor: %s, Waiting: %d more hours, Comment: %s" % (gimp.name,gimp.sponsor.name,gimp.hoursleft(),gimp.comment)
            return
        else:
            session = M.DB.Session()
            gimps = session.query(M.DB.Maps.Gimp)
            if gimps.count() < 1:
                message.alert("There are currently no gimps up for recruit")
            else:
                reply="Current gimps (with sponsor):"
                for gimp in gimps:
                    reply += (" (gimp:%s,sponsor:%s (%d hours left))" % (gimp.name,gimp.sponsor.name,gimp.hoursleft()))
                message.reply(reply)
            session.close()
    
callbacks = [("PRIVMSG", gimp())]