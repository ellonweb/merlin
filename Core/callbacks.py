# This module handles callbacks

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
from exceptions_ import LoadFailure
from modules import M

callbacks = []

def callback(message):
    # Call a callback given a message object
    cmd = message.get_command()
    for hook in callbacks:
        event, callback = hook[0:2]
        if event == cmd:
            callback(message)

def robocop(message):
    # Call a callback given a robocop message
    for hook in callbacks:
        callback = hook[1]
        if hasattr(callback,"robocop"):
            callback.robocop(message)

def unload_mod(module_name):
    # Unload a module, remove all its callbacks
    cb = callbacks[:]
    for hook in cb:
        mod_name = hook[2]
        if mod_name == module_name:
            callbacks.remove(hook)

def reload_mod(module_name):
    # Reload a module. Entails removing / readding it's callbacks
    new_callbacks = load_callbacks(module_name, load_mod(module_name))
    unload_mod(module_name)
    add_callbacks(module_name, new_callbacks)

def load_mod(module_name):
    # Load a module, and reload it in preparation to add it's callbacks
    return reload(__import__("Hooks." + module_name, globals(), locals(), [''], 1))

def load_callbacks(module_name, mod):# = None):
    # Search through a module or package and collect all it's callbacks
    new_callbacks = []
    if "__all__" in dir(mod):
        for submodule_name in mod.__all__:
            subm = module_name+"."+submodule_name
            new_callbacks += load_callbacks(subm, load_mod(subm))
    else:
        for object in dir(mod):
            callback = getattr(mod, object)
            if isinstance(callback, type) and issubclass(callback, M.loadable.loadable) and (callback is not M.loadable.loadable):
                new_callbacks.append(("PRIVMSG", callback(),))
            if isinstance(callback, M.loadable.function):
                new_callbacks.append((callback.trigger, callback,))
    return new_callbacks

def add_callbacks(module_name, new_callbacks):
    # Add a module or package's callbacks to the global list
    for event, callback in new_callbacks:
        callbacks.append((event, callback, module_name))
