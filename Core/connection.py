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
 
# IRC connection

import re
import socket
import time

from Core.exceptions_ import Reboot
from Core.config import Config
from Core.string import decode, encode, CRLF

class connection(object):
    # Socket/Connection handler
    
    def __init__(self):
        # Socket to handle is provided
        self.ping = re.compile(r"PING\s*:\s*(\S+)", re.I)
        self.pong = re.compile(r"PONG\s*:", re.I)
        self.last = time.time()
    
    def connect(self, nick):
        # Configure socket
        server = Config.get("Connection", "server")
        port = Config.getint("Connection", "port")
        print "%s Connecting... (%s %s)" % (time.asctime(), server, port,)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(330)
        self.sock.connect((server, port,))
        self.write("NICK %s" % (nick,))
        self.write("USER %s 0 * : %s" % (nick, nick,))
        return self.sock
    
    def attach(self, sock=None, nick=None):
        # Attach the socket
        nick = nick or Config.get("Connection", "nick")
        try:
            self.sock = sock or self.connect(nick)
        except socket.error as exc:
            raise Reboot(exc)
        else:
            self.file = self.sock.makefile('rb', 0)

        # WHOIS ourselves in order to setup the CUT
        self.write("WHOIS %s" % nick)
        return self.sock, nick
    
    def disconnect(self, line):
        # Cleanly close sockets
        print "%s Disconnecting IRC... (%s)" % (time.asctime(),line,)
        try:
            self.write("QUIT :%s" % (line,))
        except socket.error:
            pass
        finally:
            self.close()
        return ()
    
    def write(self, line):
        # Write to socket/server
        try:
            ponging = self.pong.match(line)
            if ponging:
                self.sock.send(line + CRLF)
            else:
                while self.last + 1 >= time.time():
                    time.sleep(0.5)
                self.sock.send(encode(line) + CRLF)
                self.last = time.time()
                print "%s >>> %s" % (time.asctime(),line,)
        except socket.error as exc:
            raise Reboot(exc)
    
    def read(self):
        # Read from socket
        try:
            line = decode(self.file.readline())
        except socket.error as exc:
            raise Reboot(exc)
        if line:
            if line[-2:] == CRLF:
                line = line[:-2]
            if line[-1] in CRLF:
                line = line[:-1]
            pinging = self.ping.match(line)
            if pinging:
                self.write("PONG :%s" % pinging.group(1))
                #print "%s <<< PING? PONG!" % (time.asctime(),)
            else:
                print "%s <<< %s" % (time.asctime(),line,)
            return line
        else:
            raise Reboot
    
    def fileno(self):
        # Return act like a file
        return self.sock.fileno()
    
    def close(self):
        # And again...
        return self.sock.close()
    
Connection = connection()