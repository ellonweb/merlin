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
 
from django.contrib.humanize.templatetags.humanize import intcomma

from Arthur.jinja import filter

@filter
def growth(object, attr):
    word = " points" if attr[:4] != "size" else " roids"
    diff = intcomma(getattr(object, attr+"_growth"))
    pc = str(round(getattr(object, attr+"_growth_pc"),1)) + "%"
    ret = '<div class="growth_%s"><span class='
    if diff < 0:
        ret += '"red"'
    elif diff > 0:
        ret += '"green"'
    else:
        ret += '"yellow"'
    ret += ' title="%s">%s</span></div>'
    ret = ret*2 %("pc", diff+word, pc, "diff", pc, diff,)
    return ret

@filter
def members(object, all=False):
    present = getattr(object, "members")
    diff = getattr(object, "member_growth")
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
def rank(object, attr):
    value = getattr(object, attr+"_rank")
    diff = getattr(object, attr+"_rank_change")
    ret = str(value) + ' <img src='
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
