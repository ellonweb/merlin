# This file is part of Merlin.
# Merlin is the Copyright (C)2008-2009 of Robin K. Hansen, Elliot Rosemarine, Andreas Jacobsen.

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
from Core.exceptions_ import LoadableError, PrefError, ParseError, ChanParseError, PNickParseError, UserError
from Core.config import Config
from Core.paconf import PA
from Core.db import Session
from Core.maps import User, Channel, Command
from Core.chanusertracker import CUT
from Core.messages import PUBLIC_REPLY

# ########################################################################### #
# ##############################    LOADABLE    ############################# #
# ########################################################################### #

class loadable(object):
    # Base loadable class for callbacks
    ""
    usage = ""
    paramre = re.compile("")
    robocop = None
    PParseError = "You need to login and set mode +x to use this command"
    AccessError = "You don't have access to this command"
    PrefError = "You must set your planet with !pref to use this command"
    ChanError = "This command may only be used in %s"
    coordre = re.compile(r"\s*(\d+)([. :\-])(\d+)(\2(\d+))?")
    planet_coordre = re.compile(r"\s*(\d+)([. :\-])(\d+)(\2(\d+))")
    govre = re.compile(r"("+ "|".join(PA.options("govs")) +")", re.I)
    racere = re.compile(r"("+ "|".join(PA.options("races")) +")", re.I)
    scanre = re.compile(r"("+ "|".join(PA.options("scans")) +")", re.I)
    true = ["1","yes","y","true","t"]
    false = ["0","no","n","false","f"]
    nulls = ["<>",".","-","?"]
    
    def __init__(self):
        self.isdecorated()
        self.commandre = re.compile(self.name+r"(\s+.*|$)",re.I)
        self.helpre = re.compile("help "+self.name,re.I)
        self.usage = self.name + self.usage
    
    def isdecorated(self):
        raise LoadableError("You need to decorate your hook")
    
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
            session = Session()
            session.add(Command(command_prefix = message.get_prefix(),
                                command = self.name,
                                command_parameters = message.get_msg()[len(self.name)+1:],
                                nick = message.get_nick(),
                                username = "" if access is True else access.name,
                                hostname = message.get_hostmask(),
                                target = message.get_chan() if message.in_chan() else message.get_nick(),))
            session.commit()
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
    
    @staticmethod
    def require_planet(hook):
        def execute(self, message, user, params):
            if self.is_user(user) and self.get_user_planet(user):
                hook(self, message, user, params)
                return
            elif message.get_pnick():
                raise UserError
        return execute
    
    @staticmethod
    def channel(chan):
        if not chan.find("#") == 0:
            if chan in Config.options("Channels"):
                chan = Config.get("Channels",chan)
            elif chan == "PM":
                chan = Config.get("Connection","nick")
            else:
                raise LoadableError("Invalid channel")
        def wrapper(hook):
            def execute(self, message, user, params):
                if self.is_chan(message, chan):
                    hook(self, message, user, params)
                    return
                else:
                    raise ChanParseError(chan)
            return execute
        return wrapper
    
    def is_user(self, user):
        if isinstance(user, User):
            return True
        return False
    
    def user_has_planet(self, user):
        if not self.is_user(user):
            return False
        if user.planet is None:
            return False
        return user.planet.active
    
    def get_user_planet(self, user):
        if not self.is_user(user):
            raise PNickParseError
        if not self.user_has_planet(user):
            raise PrefError
        return user.planet
    
    def is_chan(self, message, chan):
        if message.get_chan().lower() == chan.lower():
            return True
        return False
    
    @staticmethod
    def module(access=0):
        def wrapper(hook):
            if access in Config.options("Access"):
                acc = Config.getint("Access",access)
            elif type(access) is int:
                acc = access
            else:
                raise LoadableError("Invalid access level")
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
    
    @staticmethod
    def robohci(hook):
        def robocop(self, message):
            hook(self, message, **self.split_opts(message.get_msg()))
            message.alert(True)
        return robocop
    
    def check_access(self, message, user=None, channel=None):
        if message.in_chan():
            channel = channel or Channel.load(message.get_chan()) or Channel(maxlevel=0, userlevel=0)
            if channel.maxlevel < self.access and message.reply_type() == PUBLIC_REPLY:
                raise UserError
        else:
            channel = Channel(userlevel=0)
        user = user or CUT.get_user(message.get_nick(), pnickf=message.get_pnick)
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
        elif type(self.paramre) == dict:
            params = {}
            for key, paramre in self.paramre:
                params[key] = paramre.match(command)
            if {}.fromkeys(params) == params:
                return None
            else:
                return params
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
        flt2int = lambda x: int(x) if x.is_integer() else x
        try:
            if num/10000000 >= 1:
                return str(flt2int(round(num/1000000.0,1)))+"m"
            elif num/10000 >= 1:
                return str(flt2int(round(num/1000.0,1)))+"k"
            else:
                return str(flt2int(round(num)))
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
