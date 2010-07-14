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

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import asc
from Core.config import Config
from Core.paconf import PA
from Core.db import session
from Core.maps import Updates, Planet, User, Attack, Galaxy, AttackTarget
from Core.loadable import loadable, route, require_user

class attack(loadable):
    usage = " [ add attackID x:y[:z]] | [ new (eta|landingtick) x:y[:z]] | [ remove attackID x:y[:z]] | list | [ open attackID ]"
    
    @route(r"list",access="member")
    def list(self,message,user,params):
        reply = "Open attacks:"
        
        Q = session.query(Attack)
        Q = Q.filter(Attack.active == True)
        Q = Q.order_by(asc(Attack.landtick))
        
        for attack in Q:
            reply += " %d : %s LT: %d" %(attack.id,attack.comment,attack.landtick)
        
        message.reply(reply)

    @route(r"open\s+(\d+)", access = "member")
    def open(self, message, user, params):
        id = int(params.group(1))
        attack = session.query(Attack).filter_by(id=id).first()
        attack.active = True
        session.commit()
    
    @route(r"add\s+(\d+)\s+(\d+)([. :\-])(\d+)(\3(\d+))?", access = "member")
    def add(self, message, user, params):
        id = int(params.group(1))
        attack = session.query(Attack).filter_by(id=id).first()
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
            
        if params.group(5) is None:
            galaxy = Galaxy.load(*params.group(2,4))
            
            if galaxy is None:
                message.alert("No galaxy with coords %s:%s" % params.group(2,4))
                return
            
            Q = session.query(Planet)
            Q = Q.filter(Planet.active == True)
            Q = Q.filter(Planet.galaxy == galaxy)
            Q = Q.order_by(asc(Planet.z))

            for planet in Q:
                attackTarget = AttackTarget(attack_id=attack.id,planet_id=planet.id)
                session.add(attackTarget)
                session.commit()
                
            message.reply("Added galaxy %s:%s to attack %d" %(params.group(2),params.group(4),attack.id))
        else:
            planet = Planet.load(*params.group(2,4,6))
            if planet is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(2,4,6))
                return
            
            attackTarget = AttackTarget(attack_id=attack.id,planet_id=planet.id)
            session.add(attackTarget)
            session.commit()
            
            message.reply("Added planet %s:%s:%s to attack %d" %(params.group(2),params.group(4),params.group(6),attack.id))
    
    @route(r"new\s+(\d+)\s+(\d+)([. :\-])(\d+)(\3(\d+))?", access = "member")
    def new(self, message, user, params):
        
        tick = Updates.current_tick()
        when = int(params.group(1))
        if when < PA.getint("numbers", "protection"):
            eta = when
            when += tick
        elif when <= tick:
            message.alert("Can not create attacks in the past. You wanted tick %s, but current tick is %s." % (when, tick,))
            return
        else:
            eta = when - tick
        if when > 32767:
            when = 32767
        
        if params.group(5) is None:
            attackComment = "Attack on %s:%s" %(params.group(2),params.group(4))
            galaxy = Galaxy.load(*params.group(2,4))
            
            if galaxy is None:
                message.alert("No galaxy with coords %s:%s" % params.group(2,4))
                return
            
            attack = Attack(landtick=when,comment=attackComment)
            session.add(attack)
            session.commit()
        
            Q = session.query(Planet)
            Q = Q.filter(Planet.active == True)
            Q = Q.filter(Planet.galaxy == galaxy)
            Q = Q.order_by(asc(Planet.z))

            for planet in Q:
                attackTarget = AttackTarget(attack_id=attack.id,planet_id=planet.id)
                session.add(attackTarget)
                session.commit()
        else:
            attackComment = "Attack on %s:%s:%s" %(params.group(2),params.group(4),params.group(6))
            attack = Attack(landtick=when,comment=attackComment)
            session.add(attack)
            session.commit()
            
            planet = Planet.load(*params.group(2,4,6))
            if planet is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(2,4,6))
                return

            attackTarget = AttackTarget(attack_id=attack.id,planet_id=planet.id)
            session.add(attackTarget)
            session.commit()
            
        message.reply(attackComment + " created with id %d"%(attack.id))        
    
    @route(r"remove\s+(\d+)\s+(\d+)([. :\-])(\d+)(\3(\d+))?", access = "member")
    def remove(self, message, user, params):
        id = int(params.group(1))
        attack = session.query(Attack).filter_by(id=id).first()
        if attack is None:
            message.alert("No attack exists with id %d" %(id))
            return
            
        if params.group(5) is None:
            galaxy = Galaxy.load(*params.group(2,4))
            
            if galaxy is None:
                message.alert("No galaxy with coords %s:%s" % params.group(2,4))
                return
            
            Q = session.query(Planet)
            Q = Q.filter(Planet.active == True)
            Q = Q.filter(Planet.galaxy == galaxy)
            Q = Q.order_by(asc(Planet.z))

            for planet in Q:
                attackTarget = session.query(AttackTarget).filter(AttackTarget.planet_id==planet.id).filter(AttackTarget.attack_id==attack.id).first()
                if not attackTarget is None:
                    session.delete(attackTarget)
                    session.commit()
            
            message.reply("Removed galaxy %s:%s from attack %d" %(params.group(2),params.group(4),attack.id))
        else:
            planet = Planet.load(*params.group(2,4,6))
            if planet is None:
                message.alert("No planet with coords %s:%s:%s" % params.group(2,4,6))
                return
            
            attackTarget = session.query(AttackTarget).filter(AttackTarget.planet_id==planet.id).filter(AttackTarget.attack_id==attack.id).first()
            
            if attackTarget is None:
                message.alert("No planet with coords %s:%s:%s was fount in attack %d"%(params.group(2),params.group(4),params.group(6),attack.id))
                return
            
            session.delete(attackTarget)
            session.commit()
            
            message.reply("Removed planet %s:%s:%s from attack %d" %(params.group(2),params.group(4),params.group(6),attack.id))