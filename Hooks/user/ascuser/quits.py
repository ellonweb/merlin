import re
from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class quits(loadable):
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
        if whore.quits<=0:
            message.reply("%s is a stalwart defender of his honor" % (whore.name,))
        else:
            message.reply("%s is a whining loser who has quit %d times." % (whore.name,whore.quits))
    
callbacks = [("PRIVMSG", quits())]