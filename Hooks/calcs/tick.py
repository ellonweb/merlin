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
 
from datetime import datetime, timedelta
from Core.loadable import loadable, route
from Core.maps import Updates

class tick(loadable):
    
    @route("")
    def current(self, message, user, params):
        tick = Updates.load()
        if tick is None:
            message.reply("Ticks haven't started yet, go back to masturbating.")
        else:
            message.reply(str(tick))
    
    @route("(\d+)")
    def tick(self, message, user, params):
        tick = Updates.load(params.group(1)) or Updates.current_tick()
        if tick is None:
            message.reply("Ticks haven't started yet, go back to masturbating.")
        elif isinstance(tick, Updates):
            message.reply(str(tick))
        else:
            diff = int(params.group(1)) - tick
            now = datetime.utcnow()
            seconds = 0
            retstr = ""
            if diff > 0:
                
                if diff > 24:
                    days = (diff-1)/24
                    seconds += days*24*60*60
                    retstr += "%sd " % (days,)
                
                if diff > 1:
                    hours = (diff-1)%24
                    seconds += hours*60*60
                    retstr += "%sh " % (hours,)
                
                mins = 60 - now.minute
                seconds += mins *60
                retstr += "%sm" % (mins,)
                
                retstr = "Tick %s is expected to happen in %s" % (params.group(1), retstr,)
            
            elif diff < 0:
                
                if diff < -23:
                    days = (-diff)/24
                    seconds -= days*24*60*60
                    retstr += "%sd " % (days,)
                    
                if diff < -1:
                    hours = (-diff)%24
                    seconds -= hours*60*60
                    retstr += "%sh " % (hours,)
                    
                mins = now.minute
                seconds -= mins*60
                retstr += "%sm" % (mins,)
                
                retstr = "Tick %s was expected to happen %s ago but was not been scraped" % (params.group(1), retstr,)
            
            time = now + timedelta(seconds=seconds)
            retstr += " (%s)" % (time.strftime("%a %d/%m %H:%M"),)
            message.reply(retstr)
