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
 
from django.core.urlresolvers import reverse, NoReverseMatch

from jinja2 import nodes
from jinja2.ext import Extension

class URLReverserExtension(Extension):
    tags = set(["url"])
    
    def parse(self, parser):
        
        lineno = parser.stream.next().lineno
        args = [parser.parse_expression()]
        
        while parser.stream.current.type != 'block_end':
            parser.stream.skip_if('comma')
            args.append(parser.parse_expression())
        node = nodes.Output([self.call_method('generate', args)])
        node.set_lineno(lineno)
        return node
    
    def generate(self, url, *args):
        return reverse(url, args=args)
