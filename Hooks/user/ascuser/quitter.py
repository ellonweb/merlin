import re
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class quitter(loadable):
    def __init__(self):
        loadable.__init__(self)
        self.paramre = re.compile(r"\s([\w-]+)")
        self.usage += " pnick"
        
    @loadable.run_with_access(access['member'])
    def execute(self, message, user, params):

        # assign param variables
        search=m.group(1)

        # do stuff here
        whore = M.DB.Maps.User.load(nick=search,exact=False)
        if whore is None:
            message.reply("No users matching '%s'"%(search,))
            return
        whore.quits += 1
        session = M.DB.Session()
        session.add(whore)
        session.commit()
        session.close()
        message.reply("That whining loser %s has now quit %d times." % (whore.name,whore.quits))
