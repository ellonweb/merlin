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
 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from Core.maps import Updates, Target, Attack
from Arthur.context import menu, render
from Arthur.loadable import loadable, load

@menu("Attacks")
@load
class attack(loadable):
    access = "half"
    
    def execute(self, request, user, message=None):
        return HttpResponseRedirect("/")

@load
class view(loadable):
    access = "half"
    
    def execute(self, request, user, id, message=None):
        attack = Attack.load(id)
        if attack is None or not attack.active:
            return HttpResponseRedirect(reverse("attacks"))
        
        show_jgps = attack.landtick <= Updates.current_tick() + Attack._active_ticks/3
        
        group = []
        scans = []
        for planet in attack.planets:
            group.append((planet, [], [],))
            if planet.scan("P"):
                group[-1][1].append(planet.scan("P"))
                scans.append(planet.scan("P"))
            
            if planet.scan("D"):
                group[-1][1].append(planet.scan("D"))
                scans.append(planet.scan("D"))
            
            if planet.scan("A") or planet.scan("U"):
                group[-1][1].append(planet.scan("A") or planet.scan("U"))
                scans.append(planet.scan("A") or planet.scan("U"))
            
            if show_jgps and planet.scan("J"):
                group[-1][1].append(planet.scan("J"))
                scans.append(planet.scan("J"))
            
            bookings = dict([(target.tick, target,) for target in planet.bookings.filter(Target.tick.between(attack.landtick, attack.landtick+4))])
            for tick in xrange(attack.landtick, attack.landtick+5):
                group[-1][2].append((tick, bookings.get(tick) or (False if show_jgps else None),))
        
        return render("attack.tpl", request, attack=attack, message=message, group=group, scans=scans, intel=user.is_member())
