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
 
"""
This module is intended for command-line testing.

Usage:
When running the program, the argv is used as a prefix
for every line sent to the bot, and the output is
written to stdout. That's to say, if I call the program like this:
./cli.py :qebab!qebab@qebab.users.netgamers.org PRIVMSG #ascendancy :
./cli.py :ell!ellonweb@ellonweb.users.netgamers.org PRIVMSG #ascendancy :
It will hang on stdin for input, and when it gets a line it will concatenate
the input with this, so that for instance:
./cli.py :qebab!qebab@qebab.users.netgamers.org PRIVMSG #ascendancy :
> !eff 3k harpy
The line is run as though it was:
:qebab!qebab@qebab.users.netgamers.org PRIVMSG #ascendancy :!eff 3k harpy

Once running, you might need to run these two commands:
!debug M.CUT.Channels['#ascendancy'] = M.CUT.Channel('#ascendancy')
!debug M.CUT.Channels['#ascendancy'].addnick(message.get_nick())
"""

import merlin
import Core.connection as connection
import sys
from variables import *

class PhonyConnection(connection.Connection):
    """Used for testing purposes."""
    
    def __init__(self):
        pass
    
    def connect(self):
        
        return

    def write(self, line):

        print line

    def read(self):

        sys.stdout.write("> ")
        return " ".join(sys.argv[1:]) + sys.stdin.readline()
    
class Cli(merlin.Bot):

    def __init__(self):

        self.details = {"nick": nick, "pass": passw}
        self.conn = PhonyConnection()

if __name__ == "__main__":

    Cli().run()
