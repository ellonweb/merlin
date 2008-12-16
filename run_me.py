#!/usr/local/bin/python

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

# ########################################################################### #
# This file should be named as the name of your bot, in lowercase.            #
# The bot can only restart itself if this is file is named correctly.         #
# The bot can be identified in a list of processes by the name of this file.  #
# ########################################################################### #

import sys, socket, daemon, merlin
from Core.exceptions_ import RebootConnection
from time import sleep
from traceback import format_exc
from subprocess import Popen
from variables import nick

try:
	daemon.make_daemon(merlin.Bot) # Bot now running as daemon.
except socket.error:
	print format_exc()
	sleep(30)
except RebootConnection:
	pass
sys.exit(Popen(["./%s.py" % (nick.lower(),)]))
