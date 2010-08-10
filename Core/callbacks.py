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
 
# This module handles callbacks

import os
import socket
import sys
import time
from Core.exceptions_ import MerlinSystemCall
from Core.loader import Loader
from Core.string import errorlog
from Core.db import session
from Core.loadable import loadable

class callbacks(object):
    use_init_all = True
    # Modules/Callbacks/Hooks controller
    modules = []
    callbacks = {}
    robocops = {}
    
    def init(self):
        # Load in everything in /Hooks/
        self.load_package("Hooks")
        # Tell the Loader to back up the modules we've used
        # The backup call is currently done in Loader._reload() for
        #  better transactional safety, despite this being more elegant.
        #Loader.backup(*self.modules)
    
    def load_package(self, path):
        if self.use_init_all:
        # Using __init__'s __all__ to detect module list
            # Load the current module/package
            package = self.load_module(path)
            if "__all__" in dir(package):
            # Package pointing to more modules/subpackages
                for subpackage in package.__all__:
                    # Cycle through __all__ and load each item
                    self.load_package(path+"."+subpackage)
            else:
                # Search the module for callbacks to hook in
                self.hook_module(package)
        else:
        # Loading everything available, for future use
            # Generate an iterator with all file contents of /Hooks/
            for package, subpackages, modules in os.walk(path):
            # Cycle through each directory
                for module in modules:
                # Cycle through each module
                    # Check the file is a valid module we want to hook in
                    if module != "__init__.py" and module[-3:] == ".py" and len(module) > 3:
                        # Load the module
                        module = self.load_module(package.replace("\\",".")+"."+module[:-3])
                        # Search the module for callbacks to hook in
                        self.hook_module(module)
    
    def load_module(self, mod):
        # Keep a list of all modules imported so Loader can back them up
        self.modules.append(mod)
        Loader.load_module(mod)
        return sys.modules[mod]
    
    def hook_module(self, mod):
        for object in dir(mod):
            # Iterate over objects in the module
            callback = getattr(mod, object)
            if isinstance(callback, type) and issubclass(callback, loadable) and (callback is not loadable):
                # loadable.loadable
                self.add_callback(callback.trigger, callback(),)
    
    def add_callback(self, event, callback):
        # Add the callback to the dictionary of callbacks
        # {event: [callback,..]}
        if self.callbacks.has_key(event):
            self.callbacks[event]+= [callback,]
        else:
            self.callbacks[event] = [callback,]
        
        # Store the callback again for RoboCop if
        #  it has an executable robocop method
        if callable(callback.robocop):
            self.robocops[callback.name] = callback
    
    def callback(self, message):
        # Call back a hooked module
        event = message.get_command()
        # Check we have some callbacks stored for this event,
        if self.callbacks.has_key(event):
            # cycle through them
            for callback in self.callbacks[event]:
                # and call each one, passing in the message
                try:
                    callback(message)
                except (MerlinSystemCall, socket.error):
                    raise
                except Exception, e:
                    # Error while executing a callback/mod/hook
                    message.alert("Error in module '%s'. Please report the command you used to the bot owner as soon as possible." % (callback.name,))
                    errorlog("%s - IRC Callback Error: %s\n%s\n" % (time.asctime(),str(e),message,))
                finally:
                    # Remove any uncommitted or unrolled-back state
                    session.remove()
    
    def robocop(self, message):
        # Call back a hooked robocop module
        command = message.get_command()
        # Check we have a callback stored for this command,
        if self.robocops.has_key(command):
            callback = self.robocops[command]
            # and call it, passing in the message
            try:
                callback.robocop(message)
            except (MerlinSystemCall, socket.error):
                raise
            except Exception, e:
                # Error while executing a callback/mod/hook
                message.alert(False)
                errorlog("%s - RoboCop Callback Error: %s\n%s\n" % (time.asctime(),str(e),message,))
            finally:
                # Remove any uncommitted or unrolled-back state
                session.remove()

Callbacks = callbacks()
Callbacks.init()