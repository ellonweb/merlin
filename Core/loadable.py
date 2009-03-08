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
from exceptions_ import ParseError, PNickParseError, UserError
import chanusertracker as CUT

# ########################################################################### #
# ##############################    LOADABLE    ############################# #
# ########################################################################### #
class loadable(object):
    ""
    PParseError = "You need to login and set mode +x to use this command"
    AccessError = "You don't have access to this command"
    
    def __init__(self):
        self.access = -1
        self.coordre = re.compile(r"(\d+)[. :\-](\d+)(?:[. :\-](\d+))?")
        self.planet_coordre = re.compile(r"(\d+)[. :\-](\d+)[. :\-](\d+)")
        self.commandre = re.compile(r"^[!|.|\-|~|@]"+self.__class__.__name__,re.IGNORECASE)
        self.paramre = self.commandre
        self.robore = self.paramre
        self.helpre = re.compile(r"^[!|.|\-|~|@]help "+self.__class__.__name__,re.IGNORECASE)
        self.usage = self.__class__.__name__
        self.helptext = self.__doc__
    
    def __call__(self, message):
        self.execute(message)
    
    @staticmethod
    def run_with_access(level=0):
        def wrapper(f):
            def execute(self, message):
                self.access = level
                userparams = loadable.execute(self, message)
                if userparams:
                    f(self, message, *userparams)
            return execute
        return wrapper
    
    @staticmethod
    def with_access(level):
        def wrapper(f):
            def execute(self, message):
                self.access = level
                f(self, message)
            return execute
        return wrapper
    
    @staticmethod
    def run(f):
        def execute(self, message):
            userparams = loadable.execute(self, message)
            if userparams:
                f(self, message, *userparams)
        return execute
    
    def execute(self, message):
        m = self.commandre.search(message.get_msg())
        if not m:
            m = self.helpre.search(message.get_msg())
            if m:
                self.help(message)
            return
        try:
            user = self.has_access(message)
            if not user:
                raise UserError
            m = self.params_match(message)
            if not m:
                raise ParseError
            return user, m
        except PNickParseError:
            message.alert(self.PParseError)
        except UserError:
            message.alert(self.AccessError)
        except ParseError:
            message.alert(self.usage)
        return
    
    def has_access(self, message):
        if self.access == -1:
            return 1
        user = CUT.get_user(message.get_nick(), pnickf=message.get_pnick)
        if user is None:
            raise UserError
        if self.access == 0 or user.access & self.access > 0:
            return user
        return
    
    def params_match(self, message):
        return self.paramre.search(message.get_msg())
    
    def help(self, message):
        try:
            if not self.has_access(message):
                raise UserError
            message.reply(self.usage + "\n" + (self.helptext or ""))
        except PNickParseError:
            message.alert(self.PParseError)
        except UserError:
            message.alert(self.AccessError)
        return
    
    def robocop(self, message):
        m = self.commandre.search(message.get_msg())
        if not m:
            return
        m = self.robore.search(message.get_msg())
        return m
    
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
        except:
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
        except:
            raise ValueError

# ########################################################################### #
# ##############################    CALLBACK    ############################# #
# ########################################################################### #
class function(object):
    def __init__(self, hook, trigger):
        self.__name__ = hook.__name__
        self.hook = hook
        self.trigger = trigger
    def __call__(self, message):
        self.hook(message)
def callback(trigger):
    def wrapper(hook):
        return function(hook, trigger)
    return wrapper
