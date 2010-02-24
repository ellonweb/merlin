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
 
# The standard exceptions used by Merlin

class MerlinError(Exception):
    pass

class MerlinSystemCall(MerlinError):
    pass

class Quit(MerlinSystemCall):
    pass

class Reboot(MerlinSystemCall):
    pass

class Reload(MerlinSystemCall):
    pass

class Call999(MerlinSystemCall):
    pass

class LoadableError(MerlinError):
    pass

class PrefError(LoadableError):
    pass

class ParseError(MerlinError):
    pass

class ChanParseError(ParseError):
    pass

class MsgParseError(ParseError):
    pass

class PNickParseError(ParseError):
    pass

class UserError(MerlinError):
    pass
