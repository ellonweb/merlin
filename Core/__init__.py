# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

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
 
import gc
import sys
import time

class merlin(object):
    # Main bot container
    
    def attach(self, irc=(), robocop=()):
        self.irc = irc
        self.robocop = robocop
    
    def detach(self):
        return self.irc, self.robocop
    
    @property
    def nick(self):
        return self.irc[1]
    @nick.setter
    def nick(self, nick):
        self.irc = self.irc[0], nick
    
    def run(self):
        # Import elements of Core we need
        # These will be refreshed each time the Loader reloads
        from Core.loader import Loader
        from Core.exceptions_ import Quit, Reboot, Reload, Call999
        from Core.connection import Connection
        from Core.robocop import RoboCop
        from Core.router import Router
        
        # Collect any garbage remnants that might have been left behind
        #  from an old loader or backup that wasn't properly dereferenced
        gc.collect()
        
        try:
            # Attach the IRC connection and configure
            self.irc = Connection.attach(*self.irc)
            # Attach the RoboCop/clients sockets and configure
            self.robocop = RoboCop.attach(*self.robocop)
            
            # Operation loop
            Router.run()
        
        except Call999 as exc:
            # RoboCop server failed, restart it
            self.robocop = RoboCop.disconnect(str(exc))
            return
        
        except Reboot as exc:
            # Reset the connection first
            self.irc = Connection.disconnect(str(exc) or "Rebooting")
            print "%s Reloading..." % (time.asctime(),)
            # Reimport all the modules
            Loader.reload()
            return
        
        except Reload:
            print "%s Reloading..." % (time.asctime(),)
            # Reimport all the modules
            Loader.reload()
            return
        
        except (Quit, KeyboardInterrupt, SystemExit) as exc:
            self.irc = Connection.disconnect(str(exc) or "Bye!")
            self.robocop = RoboCop.disconnect(str(exc) or "Bye!")
            sys.exit("Bye!")

Merlin = merlin()
