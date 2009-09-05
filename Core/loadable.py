# Basic loadable class, the baseclass for most plugins

# This file is part of Merlin.
 
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
 
# This work is Copyright (C)2008 of Robin K. Hansen, Elliot Rosemarine.
# Individual portions may be copyright by individual contributors, and
# are included in this collective work with permission of the copyright
# owners.

import re
from Core.exceptions_ import LoadableError, ParseError, PNickParseError, UserError
from Core.config import Config
from Core.maps import User, Channel
from Core.chanusertracker import get_user

# ########################################################################### #
# ##############################    LOADABLE    ############################# #
# ########################################################################### #

class loadable(object):
    # Base loadable class for callbacks
    ""
    usage = ""
    paramre = re.compile("")
    PParseError = "You need to login and set mode +x to use this command"
    AccessError = "You don't have access to this command"
    coordre = re.compile(r"\s*(\d+)[. :\-](\d+)(?:[. :\-](\d+))?")
    planet_coordre = re.compile(r"\s*(\d+)[. :\-](\d+)[. :\-](\d+)")
    true = ["1","yes","y","true","t"]
    false = ["0","no","n","false","f"]
    nulls = ["<>",".","-","?"]
    
    def __init__(self):
        self.isdecorated()
        self.commandre = re.compile(self.name+"(.*)",re.I)
        self.helpre = re.compile("help "+self.name,re.I)
        self.usage = self.name + self.usage
    
    def isdecorated(self):
        raise LoadableError
    
    def match(self, message, regexp):
        if message.get_prefix():
            return regexp.match(message.get_msg()[1:])
    
    def run(self, message):
        m = self.match(message, self.commandre)
        if m is None:
            if self.match(message, self.helpre) is not None:
                self.help(message)
            return
        command = m.group(1)
        try:
            access = self.check_access(message)
            if access is None:
                raise UserError
            params = self.check_params(command)
            if params is None:
                raise ParseError
            self.execute(message, access, params)
        except PNickParseError:
            message.alert(self.PParseError)
        except UserError:
            message.alert(self.AccessError)
        except ParseError:
            message.alert(self.usage)
    
    def execute(self, message, user, params):
        pass
    
    @staticmethod
    def require_user(hook):
        def execute(self, message, user, params):
            if self.is_user(user):
                hook(self, message, user, params)
                return
            elif message.get_pnick():
                raise UserError
        return execute
    
    def is_user(self, user):
        if isinstance(user, User):
            return True
        return False
    
    @staticmethod
    def module(access=0):
        def wrapper(hook):
            acc = access if type(access) is int else Config.getint("Access",access)
            class callback(hook):
                name = hook.__name__
                doc = hook.__doc__
                trigger = "PRIVMSG"
                access = acc
                def isdecorated(self):
                    pass
                def __call__(self, message):
                    self.run(message)
            
            callback.__name__ = hook.__name__
            return callback
        return wrapper
    
    @staticmethod
    def system(trigger, command=False, admin=False):
        command = command or admin
        def wrapper(hook):
            trigg = trigger
            class callback(loadable):
                name = hook.__name__
                doc = hook.__doc__
                trigger = trigg
                def isdecorated(self):
                    pass
                def __call__(self, message):
                    if command is True:
                        self.run(message)
                    else:
                        self.execute(message, True, None)
                def execute(self, message, access, params):
                    hook(message)
                def check_access(self, message, user=None, channel=None):
                    if admin is not True:
                        return True
                    if message.get_pnick() in Config.options("Admins"):
                        return True
                    return None
            
            callback.__name__ = hook.__name__
            return callback
        return wrapper
    
    def check_access(self, message, user=None, channel=None):
        if message.in_chan():
            channel = channel or Channel.load(message.get_chan()) or Channel(maxlevel=0, userlevel=0)
            if channel.maxlevel < self.access:
                raise UserError
        else:
            channel = Channel(userlevel=0)
        user = user or get_user(message.get_nick(), pnickf=message.get_pnick)
        if self.is_user(user):
            if max(user.access, channel.userlevel) >= self.access:
                return user
            else:
                raise UserError
        else:
            if channel.userlevel >= self.access:
                return True
            elif message.get_pnick():
                raise UserError
    
    def check_params(self, command):
        if type(self.paramre) == tuple:
            for p in self.paramre:
                m = p.match(command)
                if m is not None:
                    break
            return m
        else:
            return self.paramre.match(command)
    
    def help(self, message):
        try:
            if self.check_access(message) is None:
                raise UserError
            message.reply(self.usage + "\n" + (self.doc or ""))
        except PNickParseError:
            message.alert(self.PParseError)
        except UserError:
            message.alert(self.AccessError)
        return
    
    def split_opts(self,params):
        param_dict={}
        for s in params.split():
            a=s.split('=')
            if len(a) != 2:
                continue
            param_dict[a[0].lower()]=a[1]
        return param_dict
    
    def num2short(self,num):
        try:
            if num/1000000 > 1:
                return str(round(num/1000000.0,1))+"m"
            elif num/1000 > 1:
                return str(round(num/1000.0,1))+"k"
            else:
                return str(round(num))
        except Exception:
            raise ValueError
    
    def short2num(self,short):
        try:
            if short[-1].lower()=='m':
                ret = float(short[:-1]) *1000000
            elif short[-1].lower()=='k':
                ret = float(short[:-1]) *1000
            else:
                ret = float(short)
            return int(ret)
        except Exception:
            raise ValueError
