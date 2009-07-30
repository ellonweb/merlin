# Merlin Core

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

import socket
import sys
from traceback import format_exc

if not 2.6 <= float(sys.version[:3]) < 3.0:
    sys.exit("Python 2.6.x Required")

from Core.exceptions_ import Quit, Reboot, Reload
from Core.loader import Loader
#import Core.callbacks as Callbacks
#import Core.modules
#import Hooks

# Redirect stderr to stdout
sys.stderr = sys.stdout

class Merlin(object):
    # Main bot container
    
    mods = {"Connection": "Core.connection", 
            "Action": "Core.actions", "DB": "Core.db", 
            "CUT": "Core.chanusertracker", "loadable": "Core.loadable"}
    
    def __init__(self):
        try: # break out with Quit exceptions
            
            # Connection loop
            #   Loop back to reset connection
            while True:
                
                try: # break out with Reboot exceptions
                    
                    # Reload everything
                    Loader.reboot()
                    from Core.loader import Loader
                    
                    # Load up configuration
                    from Core.config import Config
                    self.nick = Config.get("Connection", "nick")
                    
                    # Connect using raw socket
                    print "Connecting..."
                    self.connect()
                    self.Message = None
                    
                    # System loop
                    #   Loop back to reload modules
                    while True:
                        
                        try: # break out with Reload exceptions
                            
                            # Load up the Core
                            Loader.reload()
                            
                            # If we've been asked to reload, report if it worked
                            if self.Message is not None:
                                if Loader.success: self.Message.reply("Core reloaded successfully.")
                                else: self.Message.reply("Error reloading the core.")
                            
                            # Connection handler
                            self.conn = self.Connection(self.sock, self.file)
                            
                            # Configure Core
                            self.conn.write("WHOIS %s" % nick)
                            
                            # Load in Hook modules
                            for mod in Hooks.__all__:
                                Callbacks.reload_mod(mod)
                            
                            # Operation loop
                            #   Loop to parse every line received over connection
                            while True:
                                line = self.conn.read()
                                if not line:
                                    raise Reboot
                                
                                # Parse the line
                                self.Message = self.Action(line, self.conn, self.nick, self.v.alliance, Callbacks)
                                try:
                                    # Callbacks
                                    Callbacks.callback(self.Message)
                                    self.nick = self.Message.botnick
                                except (Reload, Reboot, socket.error, Quit, KeyboardInterrupt):
                                    raise
                                except:
                                    # Error while executing a callback/mod/hook
                                    print "ERROR RIGHT HERE!!"
                                    print format_exc()
                                    self.Message.alert("An exception occured and has been logged.")
                                    continue
                                
                            
                        except Reload:
                            print "Attempting to reload the system..."
                            continue
                    
                except (Reboot, socket.error) as exc:
                    print "Rebooting..."
                    continue
            
        except (Quit, KeyboardInterrupt):
            sys.exit("Bye!")
    
    def connect(self):
        # Configure socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(300)
        self.sock.connect((Config.get("Connection", "server"), Config.get("Connection", "port"),))
        self.sock.send("NICK %s\r\n" % (self.nick,))
        self.sock.send("USER %s 0 * : %s\r\n" % (self.nick, self.nick,))
        self.file = self.sock.makefile('rb')
    
if __name__ == "__main__":
    Merlin() # Start the bot here, if we're the main module.
