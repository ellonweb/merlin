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
from Core.connection import Connection as conn
from Core.actions import Action as parse
from Core.exceptions_ import RebootConnection
import Core.callbacks as cb
import Core.modules
import Hooks

# Redirect stderr to stdout
sys.stderr = sys.stdout

class Merlin(object):
    # Main bot container
    
    def __init__(self):
        try: # break out with Quit exceptions
            
            # Main loop
            while True:
                
                try: # break out with Reconnect exceptions
                    
                    # Reload variables
                    reload(v)
                    
                    # Configure self
                    self.nick = v.nick
                    self.passw = v.passw
                    self.server = v.server
                    self.port = v.port
                    
                    # Connect and pass socket to connection handler
                    self.connect()
                    self.conn = conn(self.sock, self.file)
                    self.conn.connect(self.nick)
                    
                    #####
                    self.run()
                    #####
        #####
    
    def connect(self):
        # Return a socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(300)
        self.sock.connect((self.server, self.port))
        self.file = self.sock.makefile('rb')
    
    def run(self):
        # Run the bot
        #####
        # Initialise the bot with the modules that are supposed to be loaded at startup
        for mod in Hooks.__all__:
            cb.reload_mod(mod)
            
        # The beast begins
        while True:
            # Read the next line
            line = self.conn.read()
            if not line:
                return
            
            # Parse and process the line
            parsed_line = parse(line, self.conn, self.nick, alliance, cb)
            try:
                cb.callback(parsed_line)
                self.nick = parsed_line.botnick
            except SystemExit:
                raise
            except KeyboardInterrupt:
                raise
            except RebootConnection:
                raise
            except:
                open("errorlog.txt", "a").write(asctime()+" Error:\n%s" % format_exc())
                open("errorlog.txt", "a").write("\nArguments that caused error: %s" % parsed_line)
                print "ERROR RIGHT HERE!!"
                print format_exc()
                parsed_line.alert("An exception occured and has been logged.")

if __name__ == "__main__":
    Merlin() # Start the bot here, if we're the main module.
