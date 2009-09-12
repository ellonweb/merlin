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
 
from Core.loadable import loadable

@loadable.module()
class bcalc(loadable):
    
    def execute(self, message, user, params):
        
        bcalc = ["http://bcalc.thrud.co.uk/","http://beta.5th-element.org/","http://bcalc.lch-hq.org/index.php",
                 "http://parser.5th-element.org/","http://munin.ascendancy.tv/",
                 "http://pa.xqwzts.com/prod.aspx","http://www.everyday-hero.net/reshack.html",
                 "http://patools.thrud.co.uk/", "http://game.planetarion.com/bcalc.pl"]
        
        message.reply("Bcalcs: "+" | ".join(bcalc))
