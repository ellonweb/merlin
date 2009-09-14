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
 
print "Importing database models"
from Core.db import Base, session
from Core.maps import Channel

print "Creating tables"
Base.metadata.create_all()

print "Setting up home channel"
from Core.config import Config
session.add(Channel(name=Config.get("Channels","home"),userlevel=100,maxlevel=1000))
session.commit()
session.close()

# in future add migrate code here
# will require a second engine for the old db

print "Inserting ship stats"
import shipstats
shipstats.main()
