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
 
# IRC connection

import re
import socket
import time
from Core.config import Config

CRLF = "\r\n"

class connection(object):
    # Socket/Connection handler
    
    def __init__(self):
        # Socket to handle is provided
        self.ping = re.compile(r"PING\s*:\s*(\S+)", re.I)
        self.pong = re.compile(r"PONG\s*:", re.I)
        self.last = time.time()
    
    def connect(self):
        # Configure socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(330)
        self.sock.connect((Config.get("Connection", "server"), Config.getint("Connection", "port"),))
        self.write("NICK %s" % (Config.get("Connection", "nick"),))
        self.write("USER %s 0 * : %s" % (Config.get("Connection", "nick"), Config.get("Connection", "nick"),))
        self.file = self.sock.makefile('rb')
    
    def attach(self, sock, file):
        # Attach the socket
        self.sock = sock
        self.file = file
    
    def detach(self):
        return self.sock, self.file
    
    def disconnect(self, line):
        # Cleanly close sockets
        try:
            self.write("QUIT %s" % (line,))
        except socket.error:
            pass
        else:
            self.sock.close()
            self.file.close()
    
    def write(self, line):
        # Write to socket/server
        ponging = self.pong.match(line)
        if ponging:
            self.sock.send(line + CRLF)
        else:
            while self.last + 1 >= time.time():
                time.sleep(0.5)
            self.sock.send(line + CRLF)
            self.last = time.time()
            print "%s >>> %s" % (time.asctime(),line,)
    
    def read(self):
        # Read from socket
        line = self.file.readline()
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
    
    def fileno(self):
        # Return act like a file
        return self.sock.fileno()
    
    def isatty(self):
        # Same as above
        return self.sock.isatty()
    
    def close(self):
        # And again...
        return self.sock.close()
    
Connection = connection()