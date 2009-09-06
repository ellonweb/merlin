# Whois

import re
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable

@loadable.module("member")
class whois(loadable):
    """Lookup a user's details"""
    usage = " pnick"
    paramre = re.compile(r"\s(\S+)")
    
    def execute(self, message, user, params):

        # assign param variables 
        search=params.group(1)

        # do stuff here
        if search.lower() == Config.get("Connection","nick").lower():
            message.reply("I am %s. Hear me roar." % (Config.get("Connection","nick"),))
            return

        whore = User.load(name=search,exact=False,session=session)
        if whore is None or not whore.is_member():
            message.reply("No users matching '%s'"%(search,))
            return

        reply=""
        if whore == user:
            reply+="You are %s. Your sponsor is %s. You have %s invite%s left."
        else:
            reply+="Information about %s: Their sponsor is %s. They have %s invite%s left."
        reply=reply%(whore.name,whore.sponsor,whore.invites,['','s'][whore.invites!=1])

        message.reply(reply)
