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
 
import socket
import traceback

from Core.exceptions_ import Quit, Reboot, Reload

class router(object):
    message = None
    
    def run(self):
        # Import elements of the Core we need after run is called
        #  so they can be reloaded by the loader after this module
        from Core.db import session
        from Core.connection import Connection
        from Core.actions import Action
        from Core.callbacks import Callbacks
        
        # If we've been asked to reload, report if it didn't work
        if self.message is not None:
            self.message.alert("I detect a sudden weakness in the Morphing Grid.")
        
        # Operation loop
        #   Loop to parse every line received over connection
        while True:
            line = Connection.read()
            
            try:
                # Create a new message object
                self.message = Action()
                # Parse the line
                self.message.parse(line)
                # Callbacks
                Callbacks.callback(self.message)
            except (Reload, Reboot, socket.error, Quit):
                raise
            except Exception:
                # Error while executing a callback/mod/hook
                self.message.alert("An exception occured whilst processing your request. Please report the command you used to the bot owner as soon as possible.")
                traceback.print_exc()
                continue
            finally:
                # Remove any uncommitted or unrolled-back state
                session.remove()

Router = router()