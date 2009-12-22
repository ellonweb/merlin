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
 
import socket
import time

from Core.config import Config

class server(object):
    # Robocop server
    sock = None
    socks = []
    clients = []
    
    def connect(self):
        # Configure socket
        port = Config.getint("Misc", "robocop")
        print "%s RoboCop... (%s)" % (time.asctime(), port,)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(30)
        self.sock.bind(("127.0.0.1", port,))
        self.sock.listen(5)
        return self.sock
    
    def attach(self, sock=None, socks=[]):
        # Attach the sockets
        self.sock = sock or self.connect()
        self.socks = socks
        self.clients = map(client, socks)
        return self.sock, self.socks
    
    def extend(self, sock):
        self.socks.append(sock)
        self.clients.append(client(sock))
    
    def disconnect(self, line):
        # Cleanly close sockets
        print "%s Resetting RoboCop... (%s)" % (time.asctime(),line,)
        self.close()
        self.sock = None
        return self.sock, self.socks
    
    def read(self):
        # Read from socket
        sock, addr = self.sock.accept()
        self.extend(sock)
        print "%s <<< ROBOCOP CONNECT %s" % (time.asctime(),addr,)
    
    def fileno(self):
        # Return act like a file
        return self.sock.fileno()
    
    def close(self):
        # And again...
        return self.sock.close()
    
RoboCop = server()

class client(object):
    # Robocop client
    def __init__(self, sock):
        self.sock = sock
    
    def read(self):
        # Read from socket
        pass
    
    def fileno(self):
        # Return act like a file
        return self.sock.fileno()
