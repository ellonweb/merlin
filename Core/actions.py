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
 
# This determines what the bot can send to the server, and is basically the IRC-API for plugin writers

from Core.connection import Connection
from Core.chanusertracker import CUT
from Core.messages import Message, PUBLIC_REPLY, PRIVATE_REPLY, NOTICE_REPLY

class Action(Message):
    # This object holds the parse, and will enable users to send messages to the server on a higher level
    
    def write(self, text):
        # Write something to the server, the message will be split up by newlines and at 450chars max
        params = text.split(":")[0] + ":"
        text = ":".join(text.split(":")[1:])
        if text:            
            for line in text.split("\n"):
                while line:
                    Connection.write((params + line)[:450])
                    line = line[450 - len(params):]
        else:
            Connection.write(params[:-1])
    
    def privmsg(self, text, target=None):
        # Privmsg someone. Target defaults to the person who triggered this line
        self.write("PRIVMSG %s :%s" % (target or self.get_nick(), text))
    
    def notice(self, text, target=None):
        # If we're opped in a channel in common with the user, we can reply with
        #  CNOTICE instead of NOTICE which doesn't count towards the flood limit.
        if CUT.opped(self.get_chan()) and CUT.nick_in_chan(target or self.get_nick(), self.get_chan()):
            self.write("CNOTICE %s %s :%s" % (target or self.get_nick(), self.get_chan(), text))
        else:
            self.write("NOTICE %s :%s" % (target or self.get_nick(), text))
    
    def reply(self, text):
        if self.get_command() != "PRIVMSG":
            return
        # Caps Lock is cruise control for awesome
        if self.get_msg().isupper():
            text = text.upper()
        # Always reply to a PM with a PM, otherwise only ! replies with privmsg
        # Always reply to an @command with a PM
        reply = self.reply_type()
        if reply == PUBLIC_REPLY:
            self.privmsg(text, self.get_chan())
        if reply == PRIVATE_REPLY:
            self.privmsg(text, self.get_nick())
        if reply == NOTICE_REPLY:
            self.notice(text)
    
    def alert(self, text):
        if self.get_command() != "PRIVMSG":
            return
        # Notice the user, unless it was a PM
        if self.in_chan():
            self.notice(text)
        else:
            self.privmsg(text, self.get_nick())
    
    def topic(self, text, channel=None):
        # Set the topic in a channel
        channel = channel or self.get_chan()
        self.write("TOPIC %s :%s" % (channel, text))
    
    def nick(self, new_nick):
        # Change the bots nick to new_nick
        self.write("NICK %s" % new_nick)
    
    def join(self, target, key=None):
        # Join a channel
        self.write("JOIN %s" % target if not key else "JOIN %s :%s" % (target, key))
    
    def part(self, target, comment=None):
        # Part a channel
        self.write(("PART %s :%s" % (target, comment)) if comment else ("PART %s" % target))
    
    def invite(self, target, channel=None):
        # Invite target to channel
        channel = channel or self.get_chan()
        self.write(("INVITE %s %s" % (target, channel)))
    
    def quit(self, message=None):
        # Quit the bot from the network
        self.write(("QUIT :%s" % message) if message else "QUIT")
    
    def kick(self, target, channel=None, message=None):
        # Make the bot kick someone
        channel = channel or self.get_chan()
        if message:
            self.write("KICK %s %s :%s" % (channel, target, message))
        else:
            self.write("KICK %s %s" % (channel, target))
    