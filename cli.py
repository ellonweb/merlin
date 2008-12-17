#!/usr/bin/env python
"""
This module is intended for command-line testing.

Usage:
When running the program, the argv is used as a prefix
for every line sent to the bot, and the output is
written to stdout. That's to say, if I call the program like this:
./cli-bot.py :~qebab@qebab.users.netgamers.org PRIVMSG #ascendancy :
It will hang on stdin for input, and when it gets a line it will concatenate
the input with this, so that for instance:
./cli-bot.py :~qebab@qebab.users.netgamers.org PRIVMSG #ascendancy :
> !eff 3k harpy
The line is run as though it was:
:~qebab@qebab.users.netgamers.org PRIVMSG #ascendancy :!eff 3k harpy
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
