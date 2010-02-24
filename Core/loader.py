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
 
import sys
import time
import traceback

mods = ["Core.paconf",
        "Core.connection",
        "Core.db", "Core.maps",
        "Core.chanusertracker",
        "Core.messages", "Core.actions",
        "Core.loadable", "Core.robocop",
        "Core.callbacks", "Core.router",
        ]

class loader(object):
    # Module controller
    success = False
    modules = {}
    
    def init(self):
        # First things first: backup ourselves
        self.backup("Core.config", "Core.loader")
        try:
            # Load all the main modules, they will also be
            #  backed up if they're all loaded successfully.
            self._reload()
        except Exception:
            # They weren't loaded successfully. If this is the first run,
            #  raise the error and exit. Otherwise, the error will be caught
            #  by the calling Loader, which will then .restore() everything.
            print "%s Error in Loader initialization." % (time.asctime(),)
            raise
    
    def reboot(self, Config):
        # If the reboot succeeds, this Loader instance will be
        #  replaced, so this .success is only tested if it fails.
        self.success = False
        try:
            # Reload this module, which will instantiate a new
            #  Loader, which in turn will do all the main loading.
            self.load_module("Core.config", "Core.loader")
            # Check the new loader has a successful status
            if sys.modules["Core.loader"].Loader.success is not True: raise ImportError
        except Exception, e:
            # If the new Loader fails, catch the error and restore everything
            print "%s Reboot failed, reverting to previous." % (time.asctime(),)
            with open(Config.get("Misc","errorlog"), "a") as errorlog:
                errorlog.write("%s - Loader Reboot Error: %s\n\n" % (time.asctime(),e.__str__(),))
                errorlog.write(traceback.format_exc())
                errorlog.write("\n\n\n")
            self.restore(sys)
    
    def reload(self, Config):
        self.success = False
        try:
            # Load all the main modules, they will also be
            #  backed up if they're all loaded successfully.
            self._reload()
        except Exception, e:
            # If the reload fails, catch the error and restore everything
            print "%s Reload failed, reverting to previous." % (time.asctime(),)
            with open(Config.get("Misc","errorlog"), "a") as errorlog:
                errorlog.write("%s - Loader Reload Error: %s\n\n" % (time.asctime(),e.__str__(),))
                errorlog.write(traceback.format_exc())
                errorlog.write("\n\n\n")
            self.restore(sys)
    
    def _reload(self):
        try:
            # Reload everything
            self.load_module(*mods)
        except Exception:
            # Exceptions will be dealt with in init or reload
            raise
        else:
            # Now everything has been (re)loaded, back them up
            # Note that nothing is backed up until after everything has
            #  been successfully reloaded - key transactional functionality.
            self.backup(*mods)
            # We also need to backup the modules used by Callbacks
            # The call to backup could be done in Callbacks, this
            #  is only transaction safe if Callbacks is the last module
            #  loaded though. Doing it here is ugly and hackish but safe.
            self.backup(*sys.modules["Core.callbacks"].Callbacks.modules)
            # Success is tested by the calling Loader or reported to the user
            self.success = True
    
    def load_module(self, *mods):
        # Reload (or import for the first time) the module
        for mod in mods:
            if mod in sys.modules:
                reload(sys.modules[mod])
            else:
                __import__(mod, globals(), locals(), [''], 0)
    
    def backup(self, *mods):
        for mod in mods:
            # Shallow copy of the module's __dict__
            self.modules[mod] = sys.modules[mod].__dict__.copy()
    
    def restore(self, sys):
        # We have to pass sys in, or we'd lose it when we .clear() this module
        for mod in self.modules.keys():
            # Clear the module's __dict__, this is not
            #  strictly neccessary, but good practice.
            sys.modules[mod].__dict__.clear()
            # Copy the old objects from the backup back
            sys.modules[mod].__dict__.update(self.modules[mod])

Loader = loader()
Loader.init()