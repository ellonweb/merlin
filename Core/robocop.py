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
 
import socket
import time

from Core.exceptions_ import Call999
from Core.config import Config
from Core.string import CRLF
from Core.actions import Action

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
        try:
            self.sock = sock or self.connect()
        except socket.error as exc:
            raise Call999(exc)
        else:
            self.socks = socks
            self.clients = map(client, socks)
        return self.sock, self.socks
    
    def extend(self, sock):
        # Attach the new client
        self.socks.append(sock)
        self.clients.append(client(sock))
    
    def remove(self, client):
        # Remove the new client
        self.socks.remove(client.sock)
        self.clients.remove(client)
    
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
        print "%s <<< :%s CONNECT" % (time.asctime(),self.clients[-1].host(),)
    
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
        # Basic attach
        self.sock = sock
        self.file = self.sock.makefile('rb', 0)
        try:
            self._host = (self.sock.getpeername()[1],self.fileno(),)
        except socket.error:
            self._host = (None,self.fileno(),)
    
    def host(self):
        return "RoboCop!%s/%s"%self._host
    
    def __repr__(self):
        return super(client, self).__repr__().replace("client", "client (%s)"%(self.host(),))
    
    def disconnect(self):
        # Cleanly close sockets
        print "%s <<< :%s DISCONNECT" % (time.asctime(),self.host(),)
        self.close()
        RoboCop.remove(self)
    
    def write(self, line):
        # Write to socket/server
        self.sock.send(line + CRLF)
        print "%s >>> %s :%s" % (time.asctime(),self.host(),line,)
    
    def read(self):
        # Read from socket
        try:
            line = self.file.readline()
        except socket.error:
            line = None
        if line:
            if line[-2:] == CRLF:
                line = line[:-2]
            if line[-1] in CRLF:
                line = line[:-1]
            # All this just to print a pretty log message...
            print "%s <<< :%s %s%s" % (time.asctime(), self.host(), line.split(None,1)[0].upper(),
                                       " :"+" ".join(line.split(None,1)[1:]) if len(line.split())-1 else "",)
            return line
        else:
            self.disconnect()
    
    def fileno(self):
        # Return act like a file
        return self.sock.fileno()
    
    def close(self):
        # And again...
        return self.sock.close()

class EmergencyCall(Action):
    # A modified Message/Action object for dealing with RoboCop
    
    def __init__(self, client):
        self.client = client
    
    def parse(self, line):
        # RoboCop uses a much simpler protocol than IRC!
        self.line = line
        self._hostmask = self.client.host()
        self._command = line.split(None, 1)[0]
        self._msg = " ".join(line.split(None, 1)[1:])
    
    def __str__(self):
        # String representation of the Message object (Namely for debugging purposes)
        return "[%s] <%s> %s" % (self.get_hostmask(), self.get_command(), self.get_msg())
    
    def reply(self, text):
        # Reply here will be used to reply to the client, not IRC!
        self.client.write(text)
    
    def alert(self, success):
        # This should be called if an error occurs while
        #  executing a callback or if it completes successfully
        self.reply(("OK %s" if success else "ERROR %s") % (self.line,))

class push(object):
    # Robocop message pusher
    def __init__(self, line, **kwargs):
        line = " ".join([line] + map(lambda i: "%s=%s"%i, kwargs.items()))
        port = Config.getint("Misc", "robocop")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        sock.connect(("127.0.0.1", port,))
        sock.send(line + CRLF)
    
