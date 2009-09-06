# Aids

import re
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable

@loadable.module("member")
class aids(loadable):
    """See who a user has sexed"""
    usage = " pnick"
    paramre = re.compile(r"\s(\S+)")
    
    def execute(self, message, user, params):

        # assign param variables 
        search=params.group(1)

        # do stuff here
        if search.lower() == Config.get("Connection","nick").lower():
            message.reply("I am %s. I gave aids to all you bitches." % (Config.get("Connection","nick"),))
            return

        whore = User.load(name=search,exact=False,session=session)
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return

        Q=session.query(User.name).filter(User.sponsor == whore.name)
        bitches = Q.all()

        reply=""
        if whore == user:
            reply+="You are %s." % (user.name,)
            if len(bitches) < 1:
                reply+=" You have greedily kept your aids all to yourself."
            else:
                reply+=" You have given aids to:"
                for bitch in bitches:
                    reply+=" "+bitch[0]
        else:
            if len(bitches) < 1:
                reply+="%s hasn't given anyone aids, what a selfish prick." %(whore.name,)
            else:
                reply+="%s has given aids to:" % (whore.name,)
                for bitch in bitches:
                    reply+=" "+bitch[0]

        message.reply(reply)
