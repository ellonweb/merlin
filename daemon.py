# Daemonize a program

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

import os, sys
from variables import nick

UMASK = 0
WORKDIR = "/home/rock/%s/" % (nick,) # This could be any directory
MAXFD = 1024 # Max file descriptors. You probably don't want to touch.

REDIRECT_TO = "io.txt" # Where to write to.

def make_daemon(func): # func can be any callable that takes no parameters.
    """This makes a daemon that will call func and run until it returns."""

    pid = os.fork()

    if pid == 0:

        os.setsid()

        pid = os.fork()

        if pid == 0:
            os.chdir(WORKDIR)
            os.umask(UMASK)

        else:
            os._exit(0)
        
    else:
        os._exit(0)

    fd = os.open(REDIRECT_TO, os.O_RDWR)
    os.dup2(fd,1)
    os.dup2(fd,2)

    return func()
