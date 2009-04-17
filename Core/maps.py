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

import hashlib
from math import ceil
import re
import sys
from time import time
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relation, backref, dynamic_loader
import sqlalchemy.sql as SQL
import sqlalchemy.sql.functions
SQL.f = sys.modules['sqlalchemy.sql.functions']
from .variables import access

Base = declarative_base()

# ########################################################################### #
# #############################    USER TABLES    ########################### #
# ########################################################################### #

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(15)) # pnick
    passwd = Column(String(32))
    active = Column(Boolean, default=True)
    access = Column(Integer)
    planet_id = Column(Integer, ForeignKey('planet.id', deferrable=True, ondelete='set null'))
    email = Column(String(32))
    phone = Column(String(32))
    pubphone = Column(Boolean, default=False) # Asc
    sponsor = Column(String(15)) # Asc
    invites = Column(Integer) # Asc
    quits = Column(Integer) # Asc
    stay = Column(Boolean) # Asc
    emailre = re.compile("^([\w.-]+@[\w.-]+)")
    
    @validates('passwd')
    def valid_passwd(self, key, passwd):
        return User.hasher(passwd)
    @validates('email')
    def valid_email(self, key, email):
        assert self.emailre.match(email)
        return email
    @validates('invites')
    def valid_invites(self, key, invites):
        assert invites > 0
        return invites
    
    @staticmethod
    def hasher(passwd):
        # *Every* user password operation should go through this function
        # This can be easily adapted to use SHA1 instead, or add salts
        return hashlib.md5(passwd).hexdigest()
    
    @staticmethod
    def load(name=None, id=None, passwd=None, exact=True, active=True):
        assert id or name
        session = Session()
        Q = session.query(User)
        if id is not None:
            Q = Q.filter(User.id == id)
        if name is not None:
            if Q.filter(User.name.ilike(name)).count() > 0 or (exact is True):
                Q = Q.filter(User.name.ilike(name))
            else:
                Q = Q.filter(User.name.ilike("%"+name+"%"))
        if passwd is not None:
            Q = Q.filter(User.passwd == User.hasher(passwd))
        if active is True:
            Q = Q.filter(User.active == True)
        user = Q.first()
        session.close()
        return user
def user_access_function(num):
    # Function generator for access check
    def func(self):
        if self.access & num == num:
            return True
    return func
for lvl, num in access.items():
    # Bind user access functions
    setattr(User, "is_"+lvl, user_access_function(num))

class PhoneFriend(Base):
    __tablename__ = 'phonefriends'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    friend_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))

User.phonefriends = relation(User,  secondary=PhoneFriend.__table__,
                                  primaryjoin=PhoneFriend.user_id   == User.id,
                                secondaryjoin=PhoneFriend.friend_id == User.id) # Asc

class Gimp(Base):
    __tablename__ = 'sponsor'
    id = Column(Integer, primary_key=True)
    sponsor_id = Column(Integer, ForeignKey('users.id', ondelete='cascade'))
    name = Column(String(15))
    comment = Column(String(512))
    timestamp = Column(Float, default=time)
    wait = 36 #hours. use 0 for invite mode, -1 for recruitment closed
    
    def hoursleft(self):
        return -ceil((time()-(self.timestamp+(self.wait*60*60)))/60/60)
    
    @staticmethod
    def load(name):
        session = Session()
        Q = session.query(Gimp)
        Q = Q.filter(Gimp.name.ilike(name))
        gimp = Q.first()
        session.close()
        return gimp

Gimp.sponsor = relation(User, primaryjoin=Gimp.sponsor_id==User.id, backref='gimps')

# ########################################################################### #
# #############################    DUMP TABLES    ########################### #
# ########################################################################### #

class Updates(Base):
    __tablename__ = 'updates'
    id = Column(Integer, primary_key=True)
    tick = Column(Integer, unique=True)
    planets = Column(Integer)
    galaxies = Column(Integer)
    alliances = Column(Integer)
    timestamp = Column(DateTime, default=SQL.f.current_timestamp())
    
    @staticmethod
    def current_tick():
        session = Session()
        tick = session.query(SQL.f.max(Updates.tick)).scalar() or 0
        session.close()
        return tick
class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, index=True, unique=True)
    x = Column(Integer, primary_key=True, autoincrement=False)
    y = Column(Integer, primary_key=True, autoincrement=False)
    z = Column(Integer, primary_key=True, autoincrement=False)
    #galaxy_coords = ForeignKeyConstraint(('planet.x', 'planet.y'), ('galaxy.x', 'galaxy.y'), deferrable=True)
    planetname = Column(String(20))
    rulername = Column(String(20))
    race = Column(String(3))
    size = Column(Integer)
    score = Column(Integer)
    value = Column(Integer)
    xp = Column(Integer)
    size_rank = Column(Integer)
    score_rank = Column(Integer)
    value_rank = Column(Integer)
    xp_rank = Column(Integer)
    idle = Column(Integer)
    vdiff = Column(Integer)
    
    def history(self, tick):
        return self.history_loader.filter_by(tick=tick).first()
    
    @staticmethod
    def load(x,y,z):
        session = Session()
        Q = session.query(Planet)
        Q = Q.filter_by(x=x, y=y, z=z)
        planet = Q.first()
        session.close()
        return planet
    
    def __str__(self):
        retstr="%s:%s:%s (%s) '%s' of '%s' " % (self.x,self.y,self.z,self.race,self.rulername,self.planetname)
        retstr+="Score: %s (%s) " % (self.score,self.score_rank)
        retstr+="Value: %s (%s) " % (self.value,self.value_rank)
        retstr+="Size: %s (%s) " % (self.size,self.size_rank)
        retstr+="XP: %s (%s) " % (self.xp,self.xp_rank)
        retstr+="Idle: %s " % (self.idle,)
        return retstr
    
    def bravery(self, target):
        victim_val = target.value
        attacker_val = self.value
        victim_score = target.score
        attacker_score = self.score
        bravery = max(0,( min(2,float(victim_val)/attacker_val)-0.4 ) * (min(2,float(victim_score)/attacker_score)-0.6))
        bravery *= 10.0
        return bravery
    
    def maxcap(self):
        return self.size/4
User.planet = relation(Planet, primaryjoin=User.planet_id==Planet.id)
class PlanetHistory(Base):
    __tablename__ = 'planet_history'
    tick = Column(Integer, primary_key=True, autoincrement=False)
    id = Column(Integer, primary_key=True, autoincrement=False)
    planet_history_tick = ForeignKeyConstraint(('planet_history.tick'), ('updates.tick'), deferrable=True, ondelete='cascade')
    #planet_history_id = ForeignKeyConstraint(('planet_history.id'), ('planet.id'), deferrable=True)
    x = Column(Integer)
    y = Column(Integer)
    z = Column(Integer)
    #galaxy_coords = ForeignKeyConstraint(('planet_history.tick', 'planet_history.x', 'planet_history.y'), ('galaxy_history.tick', 'galaxy_history.x', 'galaxy_history.y'), deferrable=True)
    planetname = Column(String(20))
    rulername = Column(String(20))
    race = Column(String(3))
    size = Column(Integer)
    score = Column(Integer)
    value = Column(Integer)
    xp = Column(Integer)
    size_rank = Column(Integer)
    score_rank = Column(Integer)
    value_rank = Column(Integer)
    xp_rank = Column(Integer)
    idle = Column(Integer)
    vdiff = Column(Integer)
Planet.history_loader = dynamic_loader(PlanetHistory, primaryjoin=PlanetHistory.id==Planet.id, foreign_keys=(Planet.id))
class PlanetExiles(Base):
    __tablename__ = 'planet_exiles'
    key = Column(Integer, primary_key=True)
    tick = Column(Integer)
    id = Column(Integer)
    planet_exiles_tick = ForeignKeyConstraint(('planet_exiles.tick'), ('updates.tick'), deferrable=True, ondelete='cascade')
    #planet_exiles_id = ForeignKeyConstraint(('planet_exiles.id'), ('planet.id'), deferrable=True)
    oldx = Column(Integer)
    oldy = Column(Integer)
    oldz = Column(Integer)
    newx = Column(Integer)
    newy = Column(Integer)
    newz = Column(Integer)
class Galaxy(Base):
    __tablename__ = 'galaxy'
    id = Column(Integer, index=True, unique=True)
    x = Column(Integer, primary_key=True, autoincrement=False)
    y = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(64))
    size = Column(Integer)
    score = Column(Integer)
    value = Column(Integer)
    xp = Column(Integer)
    size_rank = Column(Integer)
    score_rank = Column(Integer)
    value_rank = Column(Integer)
    xp_rank = Column(Integer)
    
    def history(self, tick):
        return self.history_loader.filter_by(tick=tick).first()
    
    def planet(self, z):
        return self.planet_loader.filter_by(z=z).first()
    
    @staticmethod
    def load(x,y):
        session = Session()
        Q = session.query(Galaxy)
        Q = Q.filter_by(x=x, y=y)
        galaxy = Q.first()
        session.close()
        return galaxy
    
    def __str__(self):
        retstr="%s:%s '%s' " % (self.x,self.y,self.name)
        retstr+="Score: %s (%s) " % (self.score,self.score_rank)
        retstr+="Value: %s (%s) " % (self.value,self.value_rank)
        retstr+="Size: %s (%s) " % (self.size,self.size_rank)
        retstr+="XP: %s (%s) " % (self.xp,self.xp_rank)
        return retstr
Planet.galaxy = relation(Galaxy, primaryjoin=and_(Galaxy.x==Planet.x, Galaxy.y==Planet.y), foreign_keys=(Planet.x, Planet.y), backref=backref('planets', primaryjoin=and_(Planet.x==Galaxy.x, Planet.y==Galaxy.y), foreign_keys=(Planet.x, Planet.y)))
Galaxy.planet_loader = dynamic_loader(Planet, primaryjoin=and_(Planet.x==Galaxy.x, Planet.y==Galaxy.y), foreign_keys=(Galaxy.x, Galaxy.y))
class GalaxyHistory(Base):
    __tablename__ = 'galaxy_history'
    tick = Column(Integer, primary_key=True, autoincrement=False)
    id = Column(Integer, primary_key=True, autoincrement=False)
    galaxy_history_tick = ForeignKeyConstraint(('galaxy_history.tick'), ('updates.tick'), deferrable=True, ondelete='cascade')
    #galaxy_history_id = ForeignKeyConstraint(('galaxy_history.id'), ('galaxy.id'), deferrable=True)
    x = Column(Integer)
    y = Column(Integer)
    name = Column(String(64))
    size = Column(Integer)
    score = Column(Integer)
    value = Column(Integer)
    xp = Column(Integer)
    size_rank = Column(Integer)
    score_rank = Column(Integer)
    value_rank = Column(Integer)
    xp_rank = Column(Integer)
    def planet(self, z):
        return self.planet_loader.filter_by(z=z).first()
PlanetHistory.galaxy = relation(GalaxyHistory, primaryjoin=and_(GalaxyHistory.tick==PlanetHistory.tick, GalaxyHistory.x==PlanetHistory.x, GalaxyHistory.y==PlanetHistory.y), foreign_keys=(PlanetHistory.tick, PlanetHistory.x, PlanetHistory.y), backref=backref('planets', primaryjoin=and_(PlanetHistory.tick==GalaxyHistory.tick, PlanetHistory.x==GalaxyHistory.x, PlanetHistory.y==GalaxyHistory.y), foreign_keys=(PlanetHistory.tick, PlanetHistory.x, PlanetHistory.y)))
Galaxy.history_loader = dynamic_loader(GalaxyHistory, primaryjoin=GalaxyHistory.id==Galaxy.id, foreign_keys=(Galaxy.id))
GalaxyHistory.planet_loader = dynamic_loader(PlanetHistory, primaryjoin=and_(PlanetHistory.tick==GalaxyHistory.tick, PlanetHistory.x==GalaxyHistory.x, PlanetHistory.y==GalaxyHistory.y), foreign_keys=(GalaxyHistory.tick, GalaxyHistory.x, GalaxyHistory.y))
class Alliance(Base):
    __tablename__ = 'alliance'
    id = Column(Integer, index=True, unique=True)
    name = Column(String(20), primary_key=True)
    size = Column(Integer)
    members = Column(Integer)
    score = Column(Integer)
    size_rank = Column(Integer)
    members_rank = Column(Integer)
    score_rank = Column(Integer)
    size_avg = Column(Integer)
    score_avg = Column(Integer)
    size_avg_rank = Column(Integer)
    score_avg_rank = Column(Integer)
    
    def history(self, tick):
        return self.history_loader.filter_by(tick=tick).first()
    
    @staticmethod
    def load(name):
        session = Session()
        Q = session.query(Alliance)
        alliance = Q.filter(Alliance.name.ilike(name)).first()
        if alliance is None:
            alliance = Q.filter(Alliance.name.ilike("%"+name+"%")).first()
        session.close()
        return alliance
    
    def __str__(self):
        retstr="'%s' Members: %s (%s) " % (self.name,self.members,self.members_rank)
        retstr+="Score: %s (%s) Avg: %s (%s) " % (self.score,self.score_rank,self.score_avg,self.score_avg_rank)
        retstr+="Size: %s (%s) Avg: %s (%s)" % (self.size,self.size_rank,self.size_avg,self.size_avg_rank)
        return retstr
class AllianceHistory(Base):
    __tablename__ = 'alliance_history'
    tick = Column(Integer, primary_key=True, autoincrement=False)
    id = Column(Integer, primary_key=True, autoincrement=False)
    alliance_history_tick = ForeignKeyConstraint(('alliance_history.tick'), ('updates.tick'), deferrable=True, ondelete='cascade')
    #alliance_history_id = ForeignKeyConstraint(('alliance_history.id'), ('alliance.id'), deferrable=True)
    name = Column(String(20))
    size = Column(Integer)
    members = Column(Integer)
    score = Column(Integer)
    size_rank = Column(Integer)
    members_rank = Column(Integer)
    score_rank = Column(Integer)
    size_avg = Column(Integer)
    score_avg = Column(Integer)
    size_avg_rank = Column(Integer)
    score_avg_rank = Column(Integer)
Alliance.history_loader = dynamic_loader(AllianceHistory, primaryjoin=AllianceHistory.id==Alliance.id, foreign_keys=(Alliance.id))

# ########################################################################### #
# ############################    INTEL TABLE    ############################ #
# ########################################################################### #

class Intel(Base):
    __tablename__ = 'intel'
    planet_id = Column(Integer, primary_key=True, autoincrement=False)
    alliance_id = Column(Integer, index=True)
    nick = Column(String(20))
    fakenick = Column(String(20))
    defwhore = Column(Boolean, default=False)
    covop = Column(Boolean, default=False)
    scanner = Column(Boolean, default=False)
    dists = Column(Integer)
    bg = Column(String(25))
    gov = Column(String(20))
    relay = Column(Boolean, default=False)
    reportchan = Column(String(30))
    comment = Column(String(512))
    def __str__(self):
        ret = "" 
        if self.nick:
            ret += " nick=%s" % (self.nick,)
        if self.alliance is not None:
            ret += " alliance=%s" % (self.alliance.name,)
        if self.fakenick:
            ret += "fakenick=%s"%(self.fakenick,)
        if self.defwhore:
            ret += "defwhore=%s"%(self.defwhore,)
        if self.covop:
            ret += "covop=%s"%(self.covop,)
        if self.scanner:
            ret += "scanner=%s"%(self.scanner,)
        if self.dists:
            ret += "dists=%s"%(self.dists,)
        if self.bg:
            ret += "bg=%s"%(self.bg,)
        if self.gov:
            ret += "gov=%s"%(self.gov,)
        if self.relay:
            ret += "relay=%s"%(self.relay,)
        if self.reportchan:
            ret += "reportchan=%s"%(self.reportchan,)
        if self.comment:
            ret += "comment=%s"%(self.comment,)
        return ret
Planet.intel = relation(Intel, primaryjoin=Intel.planet_id==Planet.id, foreign_keys=(Planet.id,))
Intel.planet = relation(Planet, primaryjoin=Planet.id==Intel.planet_id, foreign_keys=(Intel.planet_id,))
Intel.alliance = relation(Alliance, primaryjoin=Alliance.id==Intel.alliance_id, foreign_keys=(Intel.alliance_id,))
Planet.alliance = relation(Alliance, secondary=Intel.__table__, primaryjoin=Intel.planet_id==Planet.id, secondaryjoin=Alliance.id==Intel.alliance_id, foreign_keys=(Intel.planet_id, Intel.alliance_id), uselist=False)
Alliance.planets = relation(Planet, secondary=Intel.__table__, primaryjoin=Intel.alliance_id==Alliance.id, secondaryjoin=Planet.id==Intel.planet_id, foreign_keys=(Intel.planet_id, Intel.alliance_id))

# ########################################################################### #
# ###############################    SCANS    ############################### #
# ########################################################################### #

class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer)
    planet_id = Column(Integer, index=True)
    scantype = Column(String(1))
    dists = Column(Integer)
    scan_id = Column(String(32))

class Scan(Base):
    __tablename__ = 'scan'
    id = Column(String(32), primary_key=True)
    planet_id = Column(Integer, index=True)
    scantype = Column(String(1))
    tick = Column(Integer)
    group_id = Column(String(32))
    scanner_id = Column(Integer)

class PlanetScan(Base):
    __tablename__ = 'planetscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(String(32), index=True)
    planet_id = Column(Integer, index=True)
    tick = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    roid_metal = Column(Integer)
    roid_crystal = Column(Integer)
    roid_eonium = Column(Integer)
    res_metal = Column(Integer)
    res_crystal = Column(Integer)
    res_eonium = Column(Integer)
    factory_usage_light = Column(String(7))
    factory_usage_medium = Column(String(7))
    factory_usage_heavy = Column(String(7))
    prod_res = Column(Integer)
    agents = Column(Integer)
    guards = Column(Integer)

class DevScan(Base):
    __tablename__ = 'devscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(String(32), index=True)
    planet_id = Column(Integer, index=True)
    tick = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    light_factory = Column(Integer)
    medium_factory = Column(Integer)
    heavy_factory = Column(Integer)
    wave_amplifier = Column(Integer)
    wave_distorter = Column(Integer)
    metal_refinery = Column(Integer)
    crystal_refinery = Column(Integer)
    eonium_refinery = Column(Integer)
    research_lab = Column(Integer)
    finance_centre = Column(Integer)
    security_centre = Column(Integer)
    travel = Column(Integer)
    infrastructure = Column(Integer)
    hulls = Column(Integer)
    waves = Column(Integer)
    core = Column(Integer)
    covert_op = Column(Integer)
    mining = Column(Integer)

class UnitScan(Base):
    __tablename__ = 'unitscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(String(32), index=True)
    planet_id = Column(Integer, index=True)
    tick = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    ship_id = Column(Integer)
    amount = Column(Integer)

# ########################################################################### #
# #############################    BOOKINGS    ############################## #
# ########################################################################### #

class Target(Base):
    __tablename__ = 'target'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    planet_id = Column(Integer, index=True)
    tick = Column(Integer)
Target.user = relation(User, primaryjoin=User.id==Target.user_id, foreign_keys=(Target.user_id))
Target.planet = relation(Planet, primaryjoin=Planet.id==Target.planet_id, foreign_keys=(Target.planet_id))
User.bookings_loader = dynamic_loader(Target, primaryjoin=Target.user_id==User.id, foreign_keys=(Target.user_id))
Planet.bookings_loader = dynamic_loader(Target, primaryjoin=Target.planet_id==Planet.id, foreign_keys=(Target.planet_id))
Galaxy.bookings_loader = dynamic_loader(Target, secondary=Planet.__table__, primaryjoin=and_(Planet.x==Galaxy.x, Planet.y==Galaxy.y), secondaryjoin=Target.planet_id==Planet.id, foreign_keys=(Planet.id, Planet.x, Planet.y))
Alliance.bookings_loader = dynamic_loader(Target, secondary=Intel.__table__, primaryjoin=Intel.alliance_id==Alliance.id, secondaryjoin=Target.planet_id==Intel.planet_id, foreign_keys=(Intel.planet_id, Intel.alliance_id))
def bookings(self, tick=None):
    if tick is not None:
        return self.bookings_loader.filter_by(tick=tick).all()
    else:
        return self.bookings_loader.filter(Target.tick > Updates.current_tick()).all()
User.bookings = bookings
Planet.bookings = bookings
Galaxy.bookings = bookings
Alliance.bookings = bookings
del bookings

# ########################################################################### #
# ############################    PENIS CACHE    ############################ #
# ########################################################################### #

class epenis(Base):
    __tablename__ = 'epenis'
    rank = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    penis = Column(Integer)
User.epenis = relation(epenis, primaryjoin=epenis.user_id==User.id, foreign_keys=(User.id,))
class galpenis(Base):
    __tablename__ = 'galpenis'
    rank = Column(Integer, primary_key=True)
    galaxy_id = Column(Integer, index=True)
    penis = Column(Integer)
Galaxy.galpenis = relation(galpenis, primaryjoin=galpenis.galaxy_id==Galaxy.id, foreign_keys=(Galaxy.id,))
class apenis(Base):
    __tablename__ = 'apenis'
    rank = Column(Integer, primary_key=True)
    alliance_id = Column(Integer, index=True)
    penis = Column(Integer)
Alliance.apenis = relation(apenis, primaryjoin=apenis.alliance_id==Alliance.id, foreign_keys=(Alliance.id,))

# ########################################################################### #
# #############################    SHIP TABLE    ############################ #
# ########################################################################### #

class Ship(Base):
    __tablename__ = 'ships'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    class_ = Column(String(10))
    t1 = Column(String(10))
    t2 = Column(String(10))
    t3 = Column(String(10))
    type = Column(String(5))
    init = Column(Integer)
    guns = Column(Integer)
    armor = Column(Integer)
    damage = Column(Integer)
    empres = Column(Integer)
    metal = Column(Integer)
    crystal = Column(Integer)
    eonium = Column(Integer)
    total_cost = Column(Integer)
    race = Column(String(10))
    
    @staticmethod
    def load(name=None, id=None):
        assert id or name
        session = Session()
        Q = session.query(Ship)
        if id is not None:
            ship = Q.filter_by(Ship.id == id).first()
        if name is not None:
            ship = Q.filter(Ship.name.ilike(name)).first()
            if ship is None:
                ship = Q.filter(Ship.name.ilike("%"+name+"%")).first()
            if ship is None and name[-1].lower()=="s":
                ship = Q.filter(Ship.name.ilike("%"+name[:-1]+"%")).first()
            if ship is None and name[-3:].lower()=="ies":
                ship = Q.filter(Ship.name.ilike("%"+name[:-3]+"%")).first()
        session.close()
        return ship
    
    def __str__(self):
        reply="%s (%s) is class %s | Target 1: %s |"%(self.name,self.race[:3],self.class_,self.t1)
        if self.t2:
            reply+=" Target 2: %s |"%(self.t2,)
        if self.t3:
            reply+=" Target 3: %s |"%(self.t3,)
        reply+=" Type: %s | Init: %s |"%(self.type,self.init)
        reply+=" EMPres: %s |"%(self.empres,)
        if self.type=='Emp':
            reply+=" Guns: %s |"%(self.guns,)
        else:
            reply+=" D/C: %s |"%((self.damage*10000)/self.total_cost,)
        reply+=" A/C: %s"%((self.armor*10000)/self.total_cost,)
        return reply
