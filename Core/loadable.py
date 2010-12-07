# This file is part of Merlin.
# Merlin is the Copyright (C)2008,2009,2010 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
 
# Basic loadable class, the baseclass for most plugins

import re
from Core.exceptions_ import MerlinSystemCall, LoadableError, PrefError, ParseError, ChanParseError, PNickParseError, UserError
from Core.config import Config
from Core.paconf import PA
from Core.db import Session, session
from Core.maps import User, Channel, Command
from Core.chanusertracker import CUT
from Core.messages import PUBLIC_REPLY

# ########################################################################### #
# ##############################    LOADABLE    ############################# #
# ########################################################################### #

class _base(object):
    access = None
    
    def is_user(self, user):
        return isinstance(user, User) and user.is_user()
    
    def user_has_planet(self, user):
        if not self.is_user(user):
            return False
        if user.planet is None:
            return False
        return user.planet.active
    
    def num2short(self,num):
        prefix = ("","-",)[num<0]
        num = abs(num)
        flt2int = lambda x: int(x) if x.is_integer() else x
        try:
            if num/10000000 >= 1:
                return prefix+ str(flt2int(round(num/1000000.0,1)))+"m"
            elif num/10000 >= 1:
                return prefix+ str(flt2int(round(num/1000.0,1)))+"k"
            else:
                return prefix+ str(flt2int(round(num)))
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
    

class loadable(_base):
    # Base loadable class for callbacks
    ""
    usage = None
    alias = None
    param = ""
    trigger = "PRIVMSG"
    routes = None # List of (name, regex, access,)
    robocop = None
    PParseError = "You need to login and set mode +x to use this command"
    AccessError = "You don't have access to this command"
    PrefError = "You must set your planet with !pref to use this command"
    ChanError = "This command may only be used in %s"
    coord = r"(\d+)([. :\-])(\d+)(\2(\d+))?"
    planet_coord = r"(\d+)([. :\-])(\d+)(\2(\d+))"
    govre = re.compile(r"("+ "|".join(PA.options("govs")) +")", re.I)
    racere = re.compile(r"("+ "|".join(PA.options("races")) +")", re.I)
    scanre = re.compile(r"("+ "|".join(PA.options("scans")) +")", re.I)
    true = ["1","yes","y","true","t"]
    false = ["0","no","n","false","f"]
    nulls = ["<>",".","-","?"]
    
    def __new__(cls):
        self = super(loadable, cls).__new__(cls)
        self.name = cls.__name__
        self.doc = cls.__doc__
        
        self.routes = self.routes or []
        self.routes.extend([(name, route._ROUTE, route._ACCESS,) for name, route in sorted(cls.__dict__.items()) if hasattr(route, "_ROUTE") and hasattr(route, "_ACCESS")])
        
        if cls.access in Config.options("Access"):
            self.access = Config.getint("Access", cls.access)
        elif type(cls.access) is int:
            self.access = cls.access
        else:
            self.access = min([route._ACCESS for route in cls.__dict__.values() if hasattr(route, "_ROUTE") and hasattr(route, "_ACCESS")])
        
        return self
    
    def __init__(self):
        cmd = self.name if self.alias is None else "%s|%s"%(self.name,self.alias,)
        self.commandre = re.compile(r"(%s)(\s+.*|$)" %(cmd,), re.I)
        self.helpre = re.compile(r"help %s\s*$" % (cmd,), re.I)
        self.usage = (self.name + self.usage) if self.usage else None
    
    def __call__(self, message):
        self.run(message)
    
    def match(self, message, regex):
        if message.get_msg() and message.get_prefix():
            return regex.match(message.get_msg()[1:])
    
    def router(self, message, command):
        for name, regex, access in self.routes:
            params = regex.match(command)
            if params is None:
                continue
            else:
                break
        else:
            raise ParseError
        
        route = getattr(self, name)
        
        user = self.check_access(message, access)
        if user is None:
            raise UserError
        
        if getattr(route, "_USER", False) is True:
            if self.is_user(user) is False:
                message.get_pnick()
                raise UserError
        
        if getattr(route, "_PLANET", False) is True:
            if self.user_has_planet(user) is False:
                raise PrefError
        
        if getattr(route, "_CHANNEL", None) is not None:
            if self.is_chan(message, route._CHANNEL) is False:
                raise ChanParseError(route._CHANNEL)
        
        return route, name, user, params
    
    def run(self, message):
        m = self.match(message, self.commandre)
        if m is None:
            if self.match(message, self.helpre) is not None:
                self.help(message)
            return
        command = m.group(2)
        
        try:
            route, subcommand, user, params = self.router(message, command)
            
            route(message, user, params)
            
            session = Session()
            session.add(Command(command_prefix = message.get_prefix(),
                                command = self.name,
                                subcommand = subcommand,
                                command_parameters = message.get_msg()[len(m.group(1))+1:].strip(),
                                nick = message.get_nick(),
                                username = "" if user is True else user.name,
                                hostname = message.get_hostmask(),
                                target = message.get_chan() if message.in_chan() else message.get_nick(),))
            session.commit()
            session.close()
            
        except PNickParseError:
            message.alert(self.PParseError)
        except UserError:
            message.alert(self.AccessError)
        except PrefError:
            message.alert(self.PrefError)
        except ChanParseError, e:
            message.alert(self.ChanError%e)
        except ParseError:
            message.alert(self.usage)
    
    def check_access(self, message, access=None, user=None, channel=None):
        access = access or self.access
        if message.in_chan():
            channel = channel or Channel.load(message.get_chan()) or Channel(maxlevel=0, userlevel=0)
            if channel.maxlevel < access and message.reply_type() == PUBLIC_REPLY:
                raise UserError
        else:
            channel = Channel(userlevel=0)
        chan = message.get_chan() if message.in_chan() else None
        user = user or CUT.get_user(message.get_nick(), chan, pnickf=message.get_pnick)
        if self.is_user(user):
            if max(user.access, channel.userlevel) >= access:
                return user
            else:
                raise UserError
        else:
            if channel.userlevel >= access:
                return User()
            elif message.get_pnick():
                raise UserError
    
    def help(self, message):
        try:
            if self.check_access(message) is None:
                raise UserError
            message.reply(self.usage) if self.usage else None
            message.reply(self.doc) if self.doc else None
        except PNickParseError:
            message.alert(self.PParseError)
        except UserError:
            message.alert(self.AccessError)
        return
    
    def is_chan(self, message, chan):
        if message.get_chan().lower() == chan.lower():
            return True
        return False
    
    def get_user_planet(self, user):
        if not self.is_user(user):
            raise PNickParseError
        if not self.user_has_planet(user):
            raise PrefError
        return user.planet
    
    def split_opts(self,params):
        param_dict={}
        for s in params.split():
            a=s.split('=')
            if len(a) != 2:
                continue
            param_dict[a[0].lower()]=a[1]
        return param_dict
    

# ########################################################################### #
# ###############################    SYSTEM    ############################## #
# ########################################################################### #

def system(trigger, command=False, admin=False, robocop=False):
    command = command or admin
    def wrapper(hook):
        trigg = trigger
        systemcop = robocop
        class callback(loadable):
            __doc__ = hook.__doc__
            trigger = trigg
            def __call__(loadable, message):
                if command is True:
                    loadable.run(message)
                else:
                    loadable.execute(message, True, None)
            @route()
            def execute(loadable, message, access, params):
                hook(message)
            if systemcop is True:
                @robohci
                def robocop(loadable, message, **kwagrs):
                    hook(message)
            def check_access(loadable, message, access=None, user=None, channel=None):
                if command is not True:
                    return None
                if admin is not True:
                    return True
                if message.get_pnick() in Config.options("Admins"):
                    return True
                return None
        
        callback.__name__ = hook.__name__
        return callback
    return wrapper

# ########################################################################### #
# ###############################    ROUTER    ############################## #
# ########################################################################### #

def route(regex=None, access=0):
    
    if regex is None:
        param = re.compile(loadable.param, re.I)
    elif type(regex) is str:
        param = re.compile(r"\s*%s\s*$"%(regex,), re.I)
    else:
        raise LoadableError("Invalid route regex")
    
    if access in Config.options("Access"):
        access = Config.getint("Access",access)
    elif type(access) is int:
        access = access
    else:
        raise LoadableError("Invalid access level")
    
    def wrapper(execute):
        execute._ROUTE = param
        execute._ACCESS = access
        return execute
    
    return wrapper


# ########################################################################### #
# ###############################    ACCESS    ############################## #
# ########################################################################### #

def require_user(execute):
    execute._USER = True
    return execute

def require_planet(execute):
    execute._USER = True
    execute._PLANET = True
    return execute

def channel(chan):
    if not chan.find("#") == 0:
        if chan in Config.options("Channels"):
            chan = Config.get("Channels",chan)
        elif chan == "PM":
            chan = Config.get("Connection","nick")
        else:
            raise LoadableError("Invalid channel")
    def wrapper(execute):
        execute._CHANNEL = chan
        return execute
    return wrapper

# ########################################################################### #
# ##############################    ROBOCOP    ############################## #
# ########################################################################### #

def robohci(hook):
    def robocop(loadable, message):
        hook(loadable, message, **loadable.split_opts(message.get_msg()))
        message.alert(True)
    return robocop

