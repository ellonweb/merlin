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
 
# List of package modules
__all__ = [
           "request",
           "parser",
           ]

scans = {
    "P": {"name":"Planet",         "type":"1"},
    "L": {"name":"Landing",        "type":"2"},
    "D": {"name":"Development",    "type":"3"},
    "U": {"name":"Unit",           "type":"4"},
    "N": {"name":"News",           "type":"5"},
    "I": {"name":"Incoming",       "type":"6"},
    "J": {"name":"Jumpgate Probe", "type":"7"},
    "A": {"name":"Advanced Unit",  "type":"8"}
}

requesturl = "http://game.planetarion.com/waves.pl?action=single_scan&scan_type=%s&scan_x=%s&scan_y=%s&scan_z=%s"
