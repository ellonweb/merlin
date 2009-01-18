# Getanewdaddy: kick

import re
from .variables import channels, access
from .Core.modules import M
loadable = M.loadable.loadable

class getanewdaddy(loadable):
    """Remove sponsorship of a member. Their access will be reduced "galmate" level. Anyone is free to sponsor the person back under the usual conditions. This isn't a kick and it's not final.""" 
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " pnick"
        
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):

        # do stuff here
        idiot = M.DB.Maps.User.load(name=params.group(1))
        if (idiot is None) or not idiot.is_member():
            message.alert("That idiot isn't a member!")
            return
        if (not user.is_admin()) and idiot.sponsor != user.name:
            message.alert("You are not %s's sponsor"%(idiot.name,))
            return
        idiot.access = 0
        session = M.DB.Session()
        session.add(idiot)
        session.commit()
        session.close()
        message.privmsg('p','remuser #%s %s'%(channels['private'], idiot.name,))
        message.privmsg('p',"ban #%s *!*@%s.users.netgamers.org Your sponsor doesn't like you anymore"%(channels['private'], idiot.name,))
        if idiot.sponsor != user.name:
            message.privmsg('p',"note send %s Some admin has removed you for whatever reason. If you still wish to be a member, go ahead and find someone else to sponsor you back."%(idiot.name,))
            message.reply("%s has been reduced to \"galmate\" level and removed from the channel. %s is no longer %s's sponsor. If anyone else would like to sponsor that person back, they may."%(idiot.name,idiot.sponsor,idiot.name))
        else:
            message.privmsg('p',"note send %s Your sponsor (%s) no longer wishes to be your sponsor. If you still wish to be a member, go ahead and find someone else to sponsor you back."%(idiot.name,user.name,))
            message.reply("%s has been reduced to \"galmate\" level and removed from the channel. You are no longer %s's sponsor. If anyone else would like to sponsor that person back, they may."%(idiot.name,idiot.name))
        return
    
callbacks = [("PRIVMSG", getanewdaddy())]