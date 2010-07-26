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
 
# The generic objects used to send messages to callbacks and such.

import re, time

from Core import Merlin
from Core.exceptions_ import ParseError, ChanParseError, MsgParseError, PNickParseError
from Core.string import encode

PUBLIC_PREFIX  = ("!",)
PRIVATE_PREFIX = ("@",)
NOTICE_PREFIX  = (".","-","~",)
PUBLIC_REPLY  = 1
PRIVATE_REPLY = 2
NOTICE_REPLY  = 3

pnickre = re.compile(r"^:.+!.+@(.+)\.users\.netgamers\.org")

class Message(object):
    # The message object will be passed around to callbacks for inspection and ability to write to the server
    
    _chanerror = False # Will be set to True on failure to parse.
    _msgerror = False # Will be set to True on failure to parse.
    
    def parse(self, line):
        # Parse the irc line
        self.line = line
        self._nick = line.split("!")[0][1:]
        self._hostmask = line.split()[0][1:]
        self._command = line.split()[1]
        self._channel = ""
        
        # Channel
        try:
            chan = ":"+line.split(":")[1] # The ":" is added after the split etc, just to make the .find()s return the right result
            hash = max(chan.find("#"),0) or len(line)
            amp = max(chan.find("&"),0) or len(line)
            if not hash == amp: # There's no # or &, ie both lines returned len(line)
                self._channel = line[min(hash,amp):].split()[0]
            else: # This should almost certainly give the bot's nick
                self._channel = line.split()[2]
        except IndexError:
            self._chanerror = True
        
        # Encoding
        self._nick = encode(self._nick)
        self._hostmask = encode(self._hostmask)
        self._command = encode(self._command)
        self._channel = encode(self._channel)
        
        # Message
        try:
            self._msg = line[line.index(":",1)+1:]
        except ValueError:
            self._msgerror = True
    
    def __str__(self):
        # String representation of the Message object (Namely for debugging purposes)
        try:
            return "[%s] <%s> %s" % (self.get_chan(), self.get_nick(), encode(self.get_msg()))
            return "[%s] <%s> %s" % (self.get_chan(), self.get_nick(), self.get_msg())
        except ParseError:
            return ""
    
    def get_nick(self):
        # Return a parsed nick
        return self._nick
    
    def get_hostmask(self):
        # Return a parsed hostmask
        return self._hostmask
    
    def get_command(self):
        # Return the command
        return self._command

    def get_chan(self):
        # Return a channel. Raises ParseError on failure
        if self._chanerror: # Raise a ParseError: Some RAWs do not containt a target
            raise ChanParseError("Could not parse target.")
        return self._channel
    
    def in_chan(self):
        # Return True if the message was in a channel (as opposed to PM)
        return False if self.get_chan() == Merlin.nick else True
    
    def get_pnick(self):
        #Return the pnick. Raises ParseError on failure
        match = pnickre.search(self.line)
        if not match: # Raise a ParseError: User hasn't authed with P
            raise PNickParseError("Could not parse P-nick.")
        return match.group(1)
    
    def get_msg(self):
        # Return the message part of a line. Raises ParseError on failure        
        if self._msgerror: # Raise a ParseError: Some RAWs do not containt a target
            raise MsgParseError("Could not parse line.")
        return self._msg
    
    def get_prefix(self):
        # Return the prefix used for commands
        return self.get_msg()[0] if self.get_msg() and self.get_msg()[0] in PUBLIC_PREFIX+PRIVATE_PREFIX+NOTICE_PREFIX else None
    
    def reply_type(self):
        # Return the proper way to respond based on the command prefix used
        # Always reply to a PM with a PM, otherwise only ! replies with privmsg
        # Always reply to an @command with a PM
        p = self.get_prefix()
        if p in PUBLIC_PREFIX and self.in_chan():
            return PUBLIC_REPLY
        if p in PRIVATE_PREFIX or not self.in_chan():
            return PRIVATE_REPLY
        if p in NOTICE_PREFIX and self.in_chan():
            return NOTICE_REPLY
    