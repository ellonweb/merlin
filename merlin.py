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

import os
import socket
import sys
from traceback import format_exc

if not 2.6 <= float(sys.version[:3]) < 3.0:
    sys.exit("Python 2.6.x Required")

from Core.exceptions_ import RebootConnection
import Core.callbacks as Callbacks
import Core.modules
import Hooks

# Redirect stderr to stdout
sys.stderr = sys.stdout

class Merlin(object):
    # Main bot container
    
    mods = {"v": "variables", "Connection": "Core.connection", 
            "Action": "Core.actions", "DB": "Core.db", 
            "CUT": "Core.chanusertracker", "loadable": "Core.loadable"}
    
    def __init__(self):
        try: # break out with Quit exceptions
            
            # Connection loop
            #   Loop back to reset connection
            while True:
                
                try: # break out with Reconnect exceptions
                    
                    # Load up the Core
                    # This will be repeated in the System loop
                    self.coreload()
                    
                    # Configure self
                    self.nick = self.v.nick
                    
                    # Connect and pass socket to (temporary) connection handler
                    self.connect()
                    self.conn = self.Connection(self.sock, self.file)
                    print "Connecting..."
                    self.conn.connect(self.nick)
                    self.Message = None
                    
                    # System loop
                    #   Loop back to reboot and reload modules
                    while True:
                        
                        try: # break out with Reboot exceptions
                            
                            # Load up the Core
                            if self.coreload() and self.Message:
                                self.Message.reply("Core reloaded successfully.")
                            
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
                                    raise Reconnect
                                
                                # Parse the line
                                self.Message = self.Action(line, self.conn, self.nick, self.v.alliance, Callbacks)
                                try:
                                    # Callbacks
                                    Callbacks.callback(self.Message)
                                    self.nick = self.Message.botnick
                                except (Reboot, Reconnect, socket.error, Quit, KeyboardInterrupt):
                                    raise
                                except LoadHook, name:
                                    # Load a Hook
                                    try:
                                        mod = self.load("Hooks."+name)
                                        #Callbacks.unloadmod(name)
                                        #Callbacks.addmod(mod)
                                        self.Message.reply("Module %s loaded successfully." % (name,))
                                    except (ImportError, SyntaxError), error:
                                        self.Message.alert("Syntax error in module %s. Printing traceback to stderr." % (name,))
                                except:
                                    # Error while executing a callback/mod/hook
                                    print "ERROR RIGHT HERE!!"
                                    print format_exc()
                                    self.Message.alert("An exception occured and has been logged.")
                                    continue
                                
                            
                        except Reboot:
                            print "Attempting to reload the system..."
                            continue
                    
                except (Reconnect, socket.error), error:
                    print "Reconnecting..."
                    continue
            
        except (Quit, KeyboardInterrupt):
            sys.exit("Bye!")
    
    def connect(self):
        # Return a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(300)
        self.sock.connect((self.v.server, self.v.port))
        self.file = self.sock.makefile('rb')
    
    def load(self, name):
        # Load a module
        return reload(__import__(name, globals(), locals(), [''], 0))
    
    def coreload(self):
        # Reload all Core modules
        try:
            # Temporarily store the new imports
            temp = object()
            for name, path in self.mods.items():
                setattr(temp, name, self.load(path))
            # If no errors occurred during imports,
            #  assign modules to self, everything worked.
            for name in self.mods.keys():
                setattr(self, name, getattr(temp, name))
            return True
        except (ImportError, SyntaxError), error:
            # There was an error importing the modules,
            #  so reset them all back to their previous state.
            for name, path in self.mods:
                if hasattr(self, name):
                    sys.modules[path] = getattr(self, name)
                else:
                    # One of the modules (probably all!) doesn't have a
                    #  previous state. This should only occur during the
                    #  initial imports. Exit and wait to be provided with
                    #  working code! Hehehehehe :D
                    print "Error in initial Core import."
                    print format_exc()
                    sys.exit()
            return False

if __name__ == "__main__":
    Merlin() # Start the bot here, if we're the main module.
