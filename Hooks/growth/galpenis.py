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

from Core.db import session
from Core.maps import Galaxy
from Core.loadable import loadable

@loadable.module()
class galpenis(loadable):
    """Cock"""
    usage = " x:y"
    paramre = loadable.coordre
    
    def execute(self, message, user, params):
        
        galaxy = Galaxy.load(*params.group(1,2), session=session)
        if galaxy is None:
            message.alert("No galaxy with coords %s:%s" % params.group(1,2))
            return
        
        penis = galaxy.galpenis
        if penis is None:
            message.alert("No galpenis stats matching %s:%s" % params.group(1,2))
            return
        
        message.reply("galpenis for '%s' is %s score long. This makes %s:%s rank: %s for galpenis in the universe!" % (
                        galaxy.name, penis.penis, galaxy.x, galaxy.y, penis.rank,))
