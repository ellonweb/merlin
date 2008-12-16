# IRC connection

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

import socket, re, time

CRLF = "\r\n"

class Connection(object):
	# No description necessary
	
	def __init__(self, serv, port):
		# Get a server and a port -> establish a connection to it
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.settimeout(300)
		self.server = serv
		self.port = port
		self.ping = re.compile(r"PING\s*:\s*(\S+)", re.I)
		self.pong = re.compile(r"PONG\s*:", re.I)
		self.last = time.time()
	
	def connect(self):
		# Connect
		self.sock.connect((self.server, self.port))
		self.file = self.sock.makefile('rb')
	
	def write(self, line):
		# Write to socket/server
		ponging = self.pong.search(line)
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
			pinging = self.ping.search(line)
			if pinging:
				self.write("PONG :%s" % pinging.group(1))
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
	