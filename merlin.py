# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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

if not 2.6 <= float(sys.version[:3]) < 3.0:
    sys.exit("Python 2.6.x Required")

from Core.exceptions_ import Quit, Reboot, Reload, Call999

# Redirect stderr to stdout
sys.stderr = sys.stdout

class merlin(object):
    # Main bot container
    nick = None
    irc = None
    robocop = ()
    
    def run(self):
        Connection = None
        try: # break out with Quit exceptions
            
            # Connection loop
            #   Loop back to reset connection
            while True:
                
                try: # break out with Reboot exceptions
                    
                    # Load up configuration
                    from Core.config import Config
                    self.nick = Config.get("Connection", "nick")
                    
                    # Import the Loader
                    # In first run this will do the initial import
                    # Later the import is done by a call to .reboot(),
                    #  but we need to import each time to get the new Loader
                    from Core.loader import Loader
                    
                    # System loop
                    #   Loop back to reload modules
                    while True:
                        
                        try: # break out with Reload exceptions
                            
                            # Collect any garbage remnants that might have been left behind
                            #  from an old loader or backup that wasn't properly dereferenced
                            gc.collect()
                            
                            # Import elements of Core we need
                            # These will have been refreshed by a call to
                            #  either Loader.reboot() or Loader.reload()
                            from Core.db import session
                            from Core.connection import Connection
                            from Core.router import Router
                            from Core.robocop import RoboCop
                            
                            # Attach the IRC connection and configure
                            self.irc = Connection.attach(self.irc, self.nick)
                            # Attach the RoboCop/clients sockets and configure
                            self.robocop = RoboCop.attach(*self.robocop)
                            
                            # Operation loop
                            Router.run()
                            
                        except Call999 as exc:
                            # RoboCop server failed, restart it
                            self.robocop = RoboCop.disconnect(str(exc))
                            continue
                        
                        except Reload:
                            print "%s Reloading..." % (time.asctime(),)
                            # Reimport all the modules
                            Loader.reload(Config)
                            continue
                    
                except Reboot as exc:
                    # Reset the connection first
                    self.irc = Connection.disconnect(str(exc) or "Rebooting")
                    
                    print "%s Rebooting..." % (time.asctime(),)
                    # Reboot the Loader and reimport all the modules
                    Loader.reboot(Config)
                    continue
            
        except (Quit, KeyboardInterrupt, SystemExit) as exc:
            if Connection is None:
                sys.exit(exc)
            Connection.disconnect(str(exc) or "Bye!")
            sys.exit("Bye!")

Merlin = merlin()
if __name__ == "__main__":
    # Start the bot here, if we're the main module.
    Merlin.run()
