# Aids

import re
from .variables import nick, access
from .Core.modules import M
loadable = M.loadable.loadable

class aids(loadable):
    """See who a user has sexed"""
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
            # Hardcoded == bad?
            message.reply("I am %s. I gave aids to all you bitches." % (nick,))
            return

        whore = M.DB.Maps.User.load(nick=search,exact=False)
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return

        session = M.DB.Session()
        Q=session.query(M.DB.Maps.User.name).filter(M.DB.Maps.User.sponsor == whore.name)
        bitches = Q.all()
        session.close()

        reply=""
        if whore == user:
            reply+="You are %s." % (user.name,)
            if len(bitches) < 1:
                reply+=" You have greedily kept your aids all to yourself."
            else:
                reply+=" You have given aids to:"
                for bitch in bitches:
                    reply+=" "+bitch
        else:
            if len(bitches) < 1:
                reply+="%s hasn't given anyone aids, what a selfish prick." %(whore.name,)
            else:
                reply+="%s has given aids to:" % (whore.name,)
                for bitch in bitches:
                    reply+=" "+bitch

        message.reply(reply)
