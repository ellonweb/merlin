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
 
from Arthur.jinja import filter

@filter
def growth(present, past):
    diff = present - past
    ret = '<span class='
    if diff < 0:
        ret += '"red"'
    elif diff > 0:
        ret += '"green"'
    else:
        ret += '"yellow"'
    ret += ' title="' + str(diff) + ' points">'
    ret += str(round((float(diff) / past * 100),1) if past else present)
    ret += '%</span>'
    return ret

@filter
def growth_roid(present, past):
    diff = present - past
    ret = '<span class='
    if diff < 0:
        ret += '"red"'
    elif diff > 0:
        ret += '"green"'
    else:
        ret += '"yellow"'
    ret += ' title="' + str(diff) + ' roids">'
    ret += str(round((float(diff) / past * 100),1) if past else present)
    ret += '%</span>'
    return ret

@filter
def growth_members(present, past, all=False):
    diff = present - past
    ret = '<span class='
    if diff < 0:
        ret += '"red"'
    elif diff > 0:
        ret += '"green"'
    else:
        ret += '"yellow"'
    ret += ' title="' + str(diff) + ' members">'
    if all and diff != 0:
        ret += '<span class="white">(</span>'
        ret += str(diff)
        ret += '<span class="white">)</span> '
    ret += str(present)
    ret += '</span>'
    return ret

@filter
def growth_rank_image(present, past):
    diff = present - past
    ret = '<img src='
    if diff > 0:
        ret += '"/static/down.gif"'
    elif diff < 0:
        ret += '"/static/up.gif"'
    else:
        ret += '"/static/nonemover.gif"'
    ret += ' title='
    if diff > 0:
        ret += '"Down %s places"' %(diff,)
    elif diff < 0:
        ret += '"Up %s places"' %(-diff,)
    else:
        ret += '"Non mover"'
    ret += ' />'
    return ret
