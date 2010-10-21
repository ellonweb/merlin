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
 
from django.http import HttpResponse

from Core.exceptions_ import UserError
from Core.config import Config
from Core.maps import Updates, Slogan
from Arthur.jinja import jinja

class _menu(object):
    heads = []
    content = {}
    
    def __call__(self, head, sub=None, prefix=False, suffix=""):
        pre = prefix
        
        def wrapper(hook):
            prefix = hook.__module__.split(".")[1] if pre else ""
            url = ("/%s/%s/%s/"%(prefix,hook.name,suffix,)).replace("//","/")
            
            if head not in self.heads:
                self.heads.append(head)
                self.content[head] = {"hook":hook, "url":url, "subs":[], "content":{}}
                self.content[head]["link"] = hook.name == "links" and not head == Config.get("Alliance", "name")
            if sub is not None:
                self.content[head]["subs"].append(sub)
                self.content[head]["content"][sub] = {"hook":hook, "url":url}
                self.content[head]["content"][sub]["link"] = hook.name == "links" and not head == Config.get("Alliance", "name")
            
            return hook
        return wrapper
    
    def generate(self, user):
        menu = []
        for head in self.heads:
            try:
                if self.content[head]["hook"].check_access(user):
                    menu.append([head, self.content[head]["url"], self.content[head]["link"], []])
                    
                    for sub in self.content[head]["subs"]:
                        try:
                            if self.content[head]["content"][sub]["hook"].check_access(user):
                                menu[-1][3].append([sub, self.content[head]["content"][sub]["url"], self.content[head]["content"][sub]["link"]])
                        except UserError:
                            continue
            except UserError:
                continue
        
        if user.is_user():
            menu.append(["Logout", "/logout/", []])
        else:
            menu.append(["Login", "/login/", []])
        return menu

menu = _menu()

def base_context(request):
    context = {"name"   : Config.get("Alliance", "name"),
               "slogan" : Config.get("Alliance", "name"),
               "tick"   : Updates.current_tick(),
               }
    if getattr(request, "user", None) is not None:
        context["user"] = request.user
        context["menu"] = menu.generate(request.user)
    if getattr(request, "session", None) is not None:
        slogan, count = Slogan.search("")
        if slogan is not None:
            context["slogan"] = str(slogan)
    return context

def render(template, request, **context):
    context = dict(base_context(request).items() + context.items())
    return HttpResponse(jinja.get_template(template).render(context))
