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
 
from Core.exceptions_ import LoadableError, UserError
from Core.config import Config
from Core.db import Session
from Core.maps import PageView
from Arthur.context import render

# ########################################################################### #
# ##############################    LOADABLE    ############################# #
# ########################################################################### #

class loadable(object):
    access = 0
    
    def __new__(cls):
        self = super(loadable, cls).__new__(cls)
        self.name = cls.__name__
        
        if cls.access in Config.options("Access"):
            self.access = Config.getint("Access", cls.access)
        elif type(cls.access) is int:
            self.access = cls.access
        else:
            raise LoadableError("Invalid access level")
        
        return self
    
    def __call__(self, request, **kwargs):
        return self.run(request, **kwargs)
    
    def run(self, request, **kwargs):
        user = request.session.user
        
        try:
            if self.check_access(user) is not True:
                raise UserError
            
            response = self.execute(request, user, **kwargs)
            
            session = Session()
            session.add(PageView(page = self.name,
                                 full_request = request.get_full_path(),
                                 username = user.name,
                                 session = request.session.key,
                                 hostname = request.get_host(),))
            session.commit()
            
            return response
        
        except UserError:
            return render("login.tpl", request, msg="Fuck off.")
    
    def execute(self, request, user, **kwargs):
        pass
    
    def check_access(self, user):
        if user.access >= self.access:
            return True
        else:
            return False
    
