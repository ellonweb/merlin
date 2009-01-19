# This module provides a means for adding and (un)loading modules dynamically

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

import traceback, sys, os
from .variables import admins
from .Core.exceptions_ import LoadFailure, PNickParseError
from .Core.modules import M
callback = M.loadable.callback

@callback('PRIVMSG')
def loadmod(message):
    """Load a module, dynamically."""
    
    msg = message.get_msg()
    if msg[:8] == "!loadmod":
        try:
            if message.get_pnick() in admins:
                for mod in msg.split()[1:]:
                    message.alert(load(mod, message))
            else:
                message.alert("You don't have access for that.")
        except PNickParseError:
            message.alert("You don't have access for that.")

@callback('PRIVMSG')
def addmod(message):
    """Add a module."""

    msg = message.get_msg()
    if msg[:7] == "!addmod":
        try:
            if message.get_pnick() in admins:
                for mod in msg.split()[1:]:
                    open(os.path.join("Hooks/mods.txt"), "a").write(mod)
                    message.alert(load(mod, message))
            else:
                message.alert("You don't have access for that.")
        except PNickParseError:
            message.alert("You don't have access for that.")

def load(mod, message):
    # Stuff is parsed, and we'll try loading the module
    try:
        message.callbackmod.reload_mod(mod)
    except LoadFailure, e:
        return e
    except SyntaxError:
        sys.stderr.write("%s%s" % (traceback.format_exc(), "\n"))
        sys.stderr.flush()
        return "There is a syntax error in your module... Printing traceback to stderr."
    except ImportError, e:
        return e

    return "Module %s loaded successfully." % mod

@callback('PRIVMSG')
def unloadmod(message):
    """Unload a module. Privileged users only. Syntax: !unload name."""

    msg = message.get_msg()
    if msg[:10] == "!unloadmod":
        try:
            if message.get_pnick() in admins:
                for mod in msg.split()[1:]:
                    message.callbackmod.unload_mod(mod)
                    message.alert("Unloaded everything matching %s." % mod)
            else:
                message.alert("You don't have access for that.")
        except PNickParseError:
            message.alert("You don't have access for that.")

@callback('PRIVMSG')
def reload(message):
    """Reload DB. Reload Loadable."""
    
    msg = message.get_msg()
    if msg[:7] == "!reload":
        try:
            if message.get_pnick() in admins:
                # Shortcut for both: !reloadable db
                if "db" in msg:
                    M.reload_db()
                    message.alert("Reloaded the DB mappings.")
                if "loadable" in msg:
                    M.reload_loadable()
                    message.alert("Reloaded the Loadable.")
            else:
                message.alert("You don't have access for that.")
        except PNickParseError:
            message.alert("You don't have access for that.")
