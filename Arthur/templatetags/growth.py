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
from jinja2 import contextfilter

from Core.paconf import PA
from Core.maps import Planet
from Arthur.jinja import filter

@filter
def growth(object, attr):
    word = " points" if attr[:4] != "size" else " roids"
    diff = getattr(object, attr+"_growth") or 0
    pc = str(round(getattr(object, attr+"_growth_pc") or 0,1)) + "%"
    ret = '<div class="growth_%s"><span class='
    if diff < 0:
        ret += '"red"'
    elif diff > 0:
        ret += '"green"'
    else:
        ret += '"yellow"'
    ret += ' title="%s">%s</span></div>'
    ret = ret*2 %("pc", intcomma(diff)+word, pc, "diff", pc, intcomma(diff),)
    return ret

@filter
@contextfilter
def absgrowth(context, object, attr):
    present = bashcap(context, object, attr)
    diff = getattr(object, attr+"_growth") or 0
    pc = str(round(getattr(object, attr+"_growth_pc") or 0,1)) + "%"
    ret = '%s (<span class='
    if diff < 0:
        ret += '"red"'
    elif diff > 0:
        ret += '"green"'
    else:
        ret += '"yellow"'
    ret += ' title="%s">%s</span>)'
    ret = ret %(present, pc, intcomma(diff),)
    return ret

@filter
@contextfilter
def bashcap(context, target, attr):
    present = getattr(target, attr)
    if not isinstance(target, Planet) or attr not in ("value","score","size",):
        return intcomma(present)
    attacker = context['user'].planet
    if not attacker:
        return intcomma(present)
    
    if attr == "size":
        ret = '<span title="%s XP/roid * %s roids (%s%%) = %s XP">%s</span>'
        return ret %(round(attacker.bravery(target),2),
                     target.maxcap(attacker),
                     round(target.caprate(attacker),2),
                     intcomma(attacker.calc_xp(target)),
                     intcomma(present),
                     )
    else:
        ret = '<span class="%s" title="%s%%">%s</span>'
        limit = PA.getfloat("bash", attr)
        fraction = 1.0 * present / getattr(attacker, attr)
        return ret %("white" if fraction >= limit else "orange",
                     round(fraction*100,2),
                     intcomma(present),
                     )

@filter
def members(object, all=False):
    present = getattr(object, "members")
    diff = getattr(object, "member_growth") or 0
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
    diff = getattr(object, attr+"_rank_change") or 0
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
