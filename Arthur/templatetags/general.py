# This file is part of Merlin/Arthur.
# Merlin/Arthur is the Copyright (C)2009,2010 of Elliot Rosemarine.

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
 
from Core.config import Config
from Arthur.jinja import filter

@filter
def intel(user):
    return getattr(user, "is_" + Config.get("Arthur", "intel"))()

@filter
def scans(user):
    return getattr(user, "is_" + Config.get("Arthur", "scans"))()

@filter
def percent(value, total):
    fraction = float(value) / total if total else 0
    return "%s%%" % (round(fraction * 100, 1),)

@filter
def and_percent(value, total):
    fraction = float(value) / total if total else 0
    return "%s (%s%%)" % (value, round(fraction * 100, 1),)

@filter
def change(diff):
    if diff is None:
        return ""
    ret = '<span class='
    if diff < 0:
        ret += '"red"'
    elif diff > 0:
        ret += '"green"'
    else:
        ret += '"yellow"'
    ret += '>%s</span>' % (diff,)
    return ret
