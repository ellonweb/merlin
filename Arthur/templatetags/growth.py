from django import template

register = template.Library()

@register.filter
def growth(present, past):
    return str(float(present - past) / past * 100)+"%"
