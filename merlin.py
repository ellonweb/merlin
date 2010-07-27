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
sys.stderr = sys.stdout

if not 2.6 <= float(sys.version[:3]) < 2.7:
    sys.exit("Python 2.6.x Required")

if __name__ == "__main__":
    # Start the bot here, if we're the main module.
    state = ()
    
    while True:
        # Import the Loader
        # In first run this will do the initial import
        # Later the import is done by a call to .reload(),
        #  but we need to import each time to get the new Loader
        from Core.loader import Loader
        
        from Core import Merlin
        Merlin.attach(*state)
        Merlin.run()
        state = Merlin.detach()
