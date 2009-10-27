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
        ret += '"static/down.gif"'
    elif diff < 0:
        ret += '"static/up.gif"'
    else:
        ret += '"static/nonemover.gif"'
    ret += ' title='
    if diff > 0:
        ret += '"Down %s places"' %(diff,)
    elif diff < 0:
        ret += '"Up %s places"' %(-diff,)
    else:
        ret += '"Non mover"'
    ret += ' />'
    return mark_safe(ret)
