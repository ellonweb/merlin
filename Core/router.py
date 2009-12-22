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
import traceback

from Core.exceptions_ import Quit, Reboot, Reload, Call999

class router(object):
    message = None
    
    def run(self):
        # Import elements of the Core we need after run is called
        #  so they can be reloaded by the loader after this module
        from Core.connection import Connection
        from Core.db import session
        from Core.actions import Action
        from Core.callbacks import Callbacks
        from Core.robocop import RoboCop
        
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
                
                # Finally we are ready to read from the connection
                line = connection.read()
                if line is None:
                    continue
                
                try:
                    # Create a new message object
                    self.message = Action()
                    # Parse the line
                    self.message.parse(line)
                    # Callbacks
                    Callbacks.callback(self.message)
                except (Reload, Reboot, Quit):
                    raise
                except socket.error as exc:
                    # Deal with the socket error differently
                    #  depending on which connection it came from
                    if connection == Connection:
                        raise Reboot(exc)
                    if connection == RoboCop:
                        raise Call999(exc)
                    if connection in RoboCop.clients:
                        pass
                except Exception:
                    # Error while executing a callback/mod/hook
                    self.message.alert("An exception occured whilst processing your request. Please report the command you used to the bot owner as soon as possible.")
                    self.message = None
                    traceback.print_exc()
                    continue
                else:
                    # Remove the old message
                    self.message = None
                finally:
                    # Remove any uncommitted or unrolled-back state
                    session.remove()

Router = router()