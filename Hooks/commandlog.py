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
 
from sqlalchemy.sql import desc
from Core.db import session
from Core.maps import User, Command
from Core.loadable import loadable, route

class commandlog(loadable):
    """Search the bot's command log for use of specified command. Parameters is a % encapsulated list of arguments. For example, to search for someone setting the alliance on a planet in 1:1, do: !commandlog intel %1%1%alliance=%. You can also limit the search to a specific username using the optional user= argument."""
    usage = " <command> [user=<username>] <parameters> | <id>"
    access = "admin"
    
    @route(r"(\w+)\s*(.*)")
    def search3_cmd(self, message, user, params):
        self.execute(message, params.group(1), None, params.group(2))
    
    @route(r"(\w+)(?:\s+user=(\S+))?\s*(.*)")
    def search2_cmd_user(self, message, user, params):
        self.execute(message, params.group(1), params.group(2), params.group(3))
    
    @route(r"user=(\S+)\s*(.*)")
    def search1_user(self, message, user, params):
        self.execute(message, None, params.group(1), params.group(2))
    
    def execute(self, message, cmd, usr, prms):
        if usr is not None:
            spy = User.load(name=usr)
            if spy is None:
                message.reply("No such user '%s'"%(usr,))
                return
        
        Q = session.query(Command)
        Q = Q.filter(Command.command.ilike(cmd)) if cmd else Q
        Q = Q.filter(Command.command_parameters.ilike(prms)) if prms else Q
        Q = Q.filter(Command.username == spy.name) if usr else Q
        Q = Q.order_by(desc(Command.id))
        result = Q[:5]
        
        if len(result) < 1:
            message.reply("No logs matching command '%s' with parameters like '%s'"%(cmd,prms,))
            return
        
        reply = "\n".join(map(lambda c: "[ %5s | %s | %-30s | %-15s | %-15s | %s]" % (c.id, c.command, c.command_parameters.strip(), c.nick, c.username, c.command_time.ctime(),), result))
        message.reply(reply)
    
    @route(r"(\d+)")
    def get_log(self, message, user, params):
        id = params.group(1)
        c = session.query(Command).filter_by(id=id).first()
        if c is None:
            message.reply("ID %s doesn't match a log." % (id,))
            return
        message.reply("[ %5s | %s | %s | %s | %s | %s | %s]" % (c.id, c.command, c.command_parameters.strip(), c.nick, c.username, c.target, c.command_time.ctime(),))
