import re
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable

@loadable.module("member")
class quits(loadable):
    paramre = re.compile(r"\s(\S+)")
    usage = " pnick"

    def execute(self, message, user, params):

        # assign param variables
        search=params.group(1)

        # do stuff here
        whore = User.load(name=search,exact=False)
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return
        if whore.quits<=0:
            message.reply("%s is a stalwart defender of his honor" % (whore.name,))
        else:
            message.reply("%s is a whining loser who has quit %d times." % (whore.name,whore.quits))
