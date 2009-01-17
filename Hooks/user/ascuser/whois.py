# Whois

import re
from .variables import nick, access
from .Core.modules import M
loadable = M.loadable.loadable

class whois(loadable):
    """Lookup a user's details""" 
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " pnick"
        
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):

        # assign param variables 
        search=m.group(1)

        # do stuff here
        if search.lower() == nick.lower():
            message.reply("I am %s. Hear me roar." % (nick,))
            return

        whore = M.DB.Maps.User.load(nick=search,exact=False)
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return

        reply=""
        if whore == user:
            reply+="You are %s. Your sponsor is %s. You have %s invite%s left."
        else:
            reply+="Information about %s: Their sponsor is %s. They have %s invite%s left."
        reply=reply%(whore.name,whore.sponsor,whore.invites,['','s'][whore.invites!=1])

        message.reply(reply)
    
callbacks = [("PRIVMSG", whois())]