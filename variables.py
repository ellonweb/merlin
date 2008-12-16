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

# IRC info
nick = "Bot"
passw = "passwd"
server = "irc.netgamers.org"
port = 6667

# Admins for special commands
admins = ("ellonweb",)

# DB info, e.g.
#  postgres://user:password@host:port/database
#  mysql://user:password@host:port/database
# http://www.sqlalchemy.org/docs/05/dbengine.html#create-engine-url-arguments
# Don't use SQLite!
DBeng = "sqlite:///testdb.sqlite"

# Channels
channels = {
	'private'	: "#ascendancy", # priv channel needed for !inviteme
}

# Access levels
access = {
	'member'	: 1, # member access needed for !inviteme
	'scanner'	: 2,
	'intel'		: 4,
	'dc'		: 8,
	'bc'		: 16,
	'hc'		: 32,
	'admin'		: 64
}

# User Tracking
usercache = "join" # on command or on join

# Address for RoBoCoP socket
robocop = "../RoBoCoP"