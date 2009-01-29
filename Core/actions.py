# This determines what the bot can send to the server, and is basically the IRC-API for plugin writers

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

import messages
from exceptions_ import ParseError

class Action(messages.Message):
    # This object holds the parse, and will enable users to send messages to the server on a higher level
    
    def __init__(self, line, conn, nick, alliance, callbackmod):
        # The object takes a line as a parameter
        messages.Message.__init__(self, line, nick, alliance)
        self.connection = conn
        self.callbackmod = callbackmod
    
    def write(self, text):
        # Write something to the server, the message will be split up by newlines and at 450chars max
        params = text.split(":")[0] + ":"
        text = ":".join(text.split(":")[1:])
        if text:            
            for line in text.split("\n"):
                while line:
                    self.connection.write((params + line)[:(450 - len(params))])
                    line = line[(450 - len(params)):]
        else:
            self.connection.write(params[:-1])
        print
    
    def privmsg(self, text, target=None):
        # Privmsg someone. Target defaults to the person who triggered this line
        self.write("PRIVMSG %s :%s" % (target or self.get_nick(), text))
    
    def notice(self, text, target=None):
        # As above
        self.write("NOTICE %s :%s" % (target or self.get_nick(), text))
    
    def reply(self, text):
        # Always reply to a PM with a PM, otherwise only ! replies with privmsg
        if self.get_chan()[0] not in ("#","&") or self.get_msg()[0] not in (".","-","~"):
            self.privmsg(text, self.reply_target())
        else:
            self.notice(text)
    
    def alert(self, text):
        # Notice the user, unless it was a PM
        if self.get_chan()[0] != "#":
            self.privmsg(text, self.reply_target())
        else:
            self.notice(text)
    
    def topic(self, text, target=None):
        # Set the topic in a channel
        if target and not "#" in target:
            target = "#" + target
        if not target:
            target = self.get_chan()
            
            if not "#" in target:
                raise ValueError("Not a valid channelname!")
        self.write("TOPIC %s :%s" % (target, text))
    
    def nick(self, new_nick):
        # Change the bots nick to new_nick
        self.write("NICK %s" % new_nick)
        self.botnick = new_nick
    
    def join(self, target, key=None):
        # Join a channel
        self.write("JOIN %s" % target if not key else "JOIN %s :%s" % (target, key))
    
    def part(self, target, comment=None):
        # Part a channel
        self.write(("PART %s :%s" % (target, comment)) if comment else ("PART %s" % target))
    
    def invite(self, target, channel=None):
        # Invite target to channel
        self.write(("INVITE %s %s" % (target, channel)) if channel else ("INVITE %s %s" % (target, self.get_chan())))
    
    def quit(self, message=None):
        # Quit the bot from the network
        self.write(("QUIT :%s" % message) if message else "QUIT")
        
    def kick(self, target, channel=None, message=None):
        # Make the bot kick someone
        if channel and message:
            self.write("KICK %s %s :%s" % (channel, target, message))
        elif channel:
            self.write("KICK %s %s" % (channel, target))
        else:
            self.write("KICK %s %s" % (self.get_chan(), target))
    
    def __str__(self):
        # String representation of the Action object (Namely for debugging purposes)
        try:
            return "[%s] <%s> %s" % (self.get_chan(), self.get_nick(), self.get_msg())
        except ParseError:
            return ""
    