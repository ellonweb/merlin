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
 
from jinja2 import Environment, FileSystemLoader

from Arthur.templatetags.url import URLReverserExtension
jinja = Environment(extensions=["jinja2.ext.with_", "jinja2.ext.do", URLReverserExtension], loader=FileSystemLoader('Arthur/templates'))

def filter(f):
    jinja.filters[f.__name__] = f
    return f

from django.template.defaultfilters import default, force_escape, linebreaks
filter(default)
filter(force_escape)
filter(linebreaks)
from django.contrib.humanize.templatetags.humanize import intcomma
filter(intcomma)

from Arthur.templatetags import general, growth
