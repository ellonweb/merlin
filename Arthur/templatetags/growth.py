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
 
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
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
    ret += str(round((float(diff) / past * 100),2))
    ret += '%</span>'
    return mark_safe(ret)

@register.filter
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
    ret += str(round((float(diff) / past * 100),2))
    ret += '%</span>'
    return mark_safe(ret)

@register.filter
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
    return mark_safe(ret)
