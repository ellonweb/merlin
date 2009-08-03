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

import sys
import time
from traceback import format_exc

mods = ["Core.connection", "Core.db", "Core.maps", "Core.chanusertracker",
        "Core.messages", "Core.actions", "Core.loadable", "Core.paconf", "Core.callbacks"]

class loader(object):
    # Module controller
    
    def reboot(self):
        self.success = self.load_modules(["Core.loader", "Core.config"])
    
    def reload(self):
        self.success = self.load_modules()
    
    def load_modules(self, mods = mods):
        # Reload everything in the provided list
        try:
            # Temporarily store the new imports
            temp = {}
            for mod in mods:
                temp[mod] = self.load(mod)
        except (ImportError, SyntaxError) as exc:
            # There was an error importing the modules,
            #  so reset them all back to their previous state.
            for mod in mods:
                if hasattr(self, mod):
                    sys.modules[mod] = getattr(self, mod)
                else:
                    # One of the modules (probably all!) doesn't have a
                    #  previous state. This should only occur during the
                    #  initial imports. Exit and wait to be provided with
                    #  working code! Hehehehehe :D
                    print "%s Error in initial Core import." % (time.asctime(),)
                    print format_exc()
                    sys.exit()
            print "%s Error in Core, reverted to previous." % (time.asctime(),)
            print format_exc()
            return False
        else:
            # If no errors occurred during imports,
            #  assign modules to self, everything worked.
            for mod in mods:
                setattr(self, mod, temp[mod])
            return True
    
    def load(self, name):
        # Load a module
        return reload(__import__(name, globals(), locals(), [''], 0))

Loader = loader()