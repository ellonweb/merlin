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
 
import select
import socket
import time
import traceback

from Core.exceptions_ import MerlinSystemCall, Reboot, Call999
from Core.config import Config
from Core.connection import Connection
from Core.db import session
from Core.actions import Action
from Core.callbacks import Callbacks
from Core.robocop import RoboCop, EmergencyCall

class router(object):
    message = None
    
    def run(self):
        
        # If we've been asked to reload, report if it didn't work
        if self.message is not None:
            self.message.alert("I detect a sudden weakness in the Morphing Grid.")
        
        # Operation loop
        #   Loop to parse every line received over the connections
        while True:
            
            # Generate a list of connections ready to read
            inputs = select.select([Connection, RoboCop]+RoboCop.clients, [], [], 330)[0]
            
            # None of the inputs are ready to read, the IRC
            #  socket has timed out, so reboot and reconnect
            if len(inputs) == 0:
                raise Reboot("Timed out.")
            
            # Loop over the connections that are ready to read
            for connection in inputs:
                
                try:
                    if connection == Connection:
                        self.irc()
                    if connection == RoboCop:
                        self.robocop()
                    if connection in RoboCop.clients:
                        self.client(connection)
                except MerlinSystemCall:
                    raise
                except Exception, e:
                    with open(Config.get("Misc","errorlog"), "a") as errorlog:
                        errorlog.write("\n\n\n%s - Error: %s\nUNKNOWN ERROR\n" % (time.asctime(),e.__str__(),))
                        errorlog.write(traceback.format_exc())
                finally:
                    # Remove any uncommitted or unrolled-back state
                    session.remove()
    
    def irc(self):
        # Read, parse and evaluate an IRC line
        try:
            # Create a new message object
            self.message = Action()
            # Parse the line
            line = Connection.read()
            self.message.parse(line)
            # Callbacks
            Callbacks.callback(self.message)
        
        except socket.error as exc:
            raise Reboot(exc)
        except MerlinSystemCall:
            raise
        except Exception:
            # Error while executing a callback/mod/hook
            self.message.alert("An exception occured whilst processing your request. Please report the command you used to the bot owner as soon as possible.")
            raise
    
    def robocop(self):
        # Accept a new RoboCop client
        try:
            self.message = None
            RoboCop.read()
        except socket.error as exc:
            raise Call999(exc)
    
    def client(self, connection):
        # Read, parse and evaluate a line from a RoboCop client
        try:
            # Create a new message object
            self.message = EmergencyCall(connection)
            # Parse the line
            line = connection.read()
            if line is None:
                return
            self.message.parse(line)
            # Callbacks
            Callbacks.robocop(self.message)
        
        except socket.error as exc:
            connection.disconnect()
        except Exception:
            # Error while executing a callback/mod/hook
            self.message.alert()
            raise

Router = router()