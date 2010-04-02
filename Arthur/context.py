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
 
from django.shortcuts import render_to_response
from django.template import RequestContext

from Core.config import Config
from Core.maps import Slogan

class _menu(object):
    heads = []
    content = {}
    
    def __call__(self, head, sub=None, prefix=False, suffix=""):
        prefix = head if prefix else ""
        
        def wrapper(hook):
            url = ("/%s/%s/%s/"%(prefix,hook.name,suffix,)).replace("//","/")
            
            if head not in self.heads:
                self.heads.append(head)
                self.content[head] = {"hook":hook, "url":url, "subs":[], "content":{}}
                self.content[head]["link"] = hook.name == "links" and not head == Config.get("Alliance", "name")
            if sub is not None:
                self.content[head]["subs"].append(sub)
                self.content[head]["content"][sub] = {"hook":hook, "url":url}
                self.content[head]["content"][sub]["link"] = hook.name == "links"
            
            return hook
        return wrapper
    
    def generate(self, user):
        menu = []
        for head in self.heads:
            if self.content[head]["hook"].check_access(user):
                menu.append([head, self.content[head]["url"], self.content[head]["link"], []])
                
                for sub in self.content[head]["subs"]:
                    if self.content[head]["content"][sub]["hook"].check_access(user):
                        menu[-1][3].append([sub, self.content[head]["content"][sub]["url"], self.content[head]["content"][sub]["link"]])
        
        menu.append(["Logout", "/logout/", []])
        return menu

menu = _menu()

def context(request):
    context = {"name"   : Config.get("Alliance", "name"),
               "slogan" : Config.get("Alliance", "name")
               }
    if request.session is not None:
        slogan, count = Slogan.search("")
        if slogan is not None:
            context["slogan"] = str(slogan)
        context["user"] = request.session.user.name
        context["menu"] = menu.generate(request.session.user)
    return context

def render(tpl, request, **context):
    return render_to_response(tpl, context, RequestContext(request))
