# galpenis

# This file is part of Merlin.
 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

from .variables import access
from .Core.modules import M
loadable = M.loadable.loadable

class galpenis(loadable):
    """Cock"""
    
    def __init__(self):
        loadable.__init__(self)
        self.paramre = self.coordre
        self.usage += " x:y"
    
    @loadable.run_with_access()
    def execute(self, message, user, params):
        
        galaxy = M.DB.Maps.Galaxy.load(*params.group(1,2))
        if galaxy is None:
            message.alert("No galaxy with coords %s:%s" % params.group(1,2))
            return
        
        session = M.DB.Session()
        session.add(galaxy)
        penis = galaxy.galpenis
        session.close()
        if penis is None:
            message.alert("No galpenis stats matching %s:%s" % params.group(1,2))
            return
        
        message.reply("galpenis for '%s' is %s score long. This makes %s:%s rank: %s for galpenis in the universe!" % (
                        galaxy.name, penis.penis, galaxy.x, galaxy.y, penis.rank,))
