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
 
import select
import time

from Core.exceptions_ import MerlinSystemCall, Reboot, Call999
from Core.loader import Loader
from Core.string import errorlog
from Core.connection import Connection
from Core.actions import Action
from Core.robocop import RoboCop, EmergencyCall
from Core.callbacks import Callbacks

class router(object):
    message = None
    
    def run(self):
        
        # If we've been asked to reload, report if it didn't work
        if Loader.success is False and self.message is not None:
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
                    print "%s Routing error logged." % (time.asctime(),)
                    errorlog("%s - Routing Error: %s\n%s\n" % (time.asctime(),str(e),connection,))
    
    def irc(self):
        # A line from IRC
        # Create a new message object
        self.message = Action()
        # Read the line
        line = Connection.read()
        try:
            # Parse the line
            self.message.parse(line)
            # Callbacks process the line
            Callbacks.callback(self.message)
        except MerlinSystemCall:
            raise
        except Exception:
            # Error while executing a callback/mod/hook
            self.message.alert("An exception occured whilst processing your request. Please report the command you used to the bot owner as soon as possible.")
            raise
    
    def robocop(self):
        # Delete the previous message object
        self.message = None
        # Accept a new RoboCop client
        RoboCop.read()
    
    def client(self, connection):
        # A line from a RoboCop client
        # Create a new message object
        self.message = EmergencyCall(connection)
        # Read the line
        line = connection.read()
        try:
            # Parse the line
            self.message.parse(line)
            # Callbacks process the line
            Callbacks.robocop(self.message)
        except MerlinSystemCall:
            raise
        except Exception:
            # Error while executing a callback/mod/hook
            self.message.alert(False)
            raise

Router = router()