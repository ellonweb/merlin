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
from time import asctime
from traceback import format_exc
import variables as v
import Core
from Core.connection import Connection
from Core.actions import Action
from Core.exceptions_ import RebootConnection
import Core.callbacks as Callbacks
import Core.modules
import Hooks

# Redirect stderr to stdout
sys.stderr = sys.stdout

class Merlin(object):
    # Main bot container
    
    def __init__(self):
        try: # break out with Quit exceptions
            
            # Connection loop
            #   Loop back to reset connection
            while True:
                
                try: # break out with Reconnect exceptions
                    
                    # Reload variables
                    reload(v)
                    
                    # Configure self
                    self.nick = v.nick
                    self.passw = v.passw
                    self.alliance = v.alliance
                    self.server = v.server
                    self.port = v.port
                    
                    # Connect and pass socket to (temporary) connection handler
                    self.connect()
                    self.conn = Connection(self.sock, self.file)
                    self.conn.connect(self.nick)
                    
                    # System loop
                    #   Loop back to reboot and reload modules
                    while True:
                        
                        try: # break out with Reboot exceptions
                            
                            # Load in Core modules
                            
                            # Connection handler
                            self.conn = Connection(self.sock, self.file)
                            
                            # Load in Hook modules
                            
                            # Operation loop
                            #   Loop to parse every line received over connection
                            while True:
                                line = self.conn.read()
                                if not line:
                                    raise Reconnect
                                
                                # Parse the line
                                Message = Action(line, self.conn, self.nick, self.alliance, Callbacks)
                                try:
                                    # Callbacks
                                    Callbacks.callback(Message)
                                    self.nick = Message.botnick
                                except Reboot:
                                    raise
                                except Reconnect:
                                    raise
                                except Quit:
                                    raise
                                except KeyboardInterrupt:
                                    raise
                                except:
                                    print "ERROR RIGHT HERE!!"
                                    print format_exc()
                                    parsed_line.alert("An exception occured and has been logged.")
                                    continue
                                
                            
                        except Reboot:
                            print "some message about a reboot"
                            continue
                    
                except Reconnect:
                    print "some message about a reconnect"
                    continue
            
        except Quit:
            pass
        except KeyboardInterrupt:
            pass
        print "some quit message"
        sys.exit()
    
    def connect(self):
        # Return a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(300)
        self.sock.connect((self.server, self.port))
        self.file = self.sock.makefile('rb')
    
    def run(self):
        # Run the bot
        
        # Initialise the bot with the modules that are supposed to be loaded at startup
        for mod in Hooks.__all__:
            cb.reload_mod(mod)
            

if __name__ == "__main__":
    Merlin() # Start the bot here, if we're the main module.
