import re
from Core.config import Config
from Core.db import session
from Core.maps import User
from Core.loadable import loadable

@loadable.module("member")
class quitter(loadable):
    usage = " pnick"
    paramre = re.compile(r"\s(\S+)")

    def execute(self, message, user, params):

        # assign param variables
        search=params.group(1)

        # do stuff here
        whore = User.load(name=search,exact=False)
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return
        whore.quits += 1
        session.commit()
        message.reply("That whining loser %s has now quit %d times." % (whore.name,whore.quits))
