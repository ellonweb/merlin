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
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates, relation, backref, dynamic_loader
import sqlalchemy.sql as SQL
import sqlalchemy.sql.functions
SQL.f = sys.modules['sqlalchemy.sql.functions']
from .variables import access

Base = declarative_base()

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

class Galaxy(Base):
    __tablename__ = 'galaxy'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
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
class GalaxyHistory(Base):
    __tablename__ = 'galaxy_history'
    tick = Column(Integer, ForeignKey(Updates.id, deferrable=True, ondelete='cascade'), primary_key=True, autoincrement=False)
    id = Column(Integer, ForeignKey(Galaxy.id), primary_key=True, autoincrement=False)
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
Galaxy.history_loader = dynamic_loader(GalaxyHistory, backref="current")

class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    x = Column(Integer, ForeignKey(Galaxy.x))
    y = Column(Integer, ForeignKey(Galaxy.y))
    z = Column(Integer)
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
    
    def scan(self, type):
        return self.scans.filter_by(scantype=type[0].upper()).order_by(SQL.desc(Scan.id)).first()
    
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
Planet2Galaxy = and_(Galaxy.x==Planet.x,
                     Galaxy.y==Planet.y)
Planet.galaxy = relation(Galaxy, backref="planets", primaryjoin=Planet2Galaxy)
Galaxy.planet_loader = dynamic_loader(Planet, primaryjoin=Planet2Galaxy)
class PlanetHistory(Base):
    __tablename__ = 'planet_history'
    tick = Column(Integer, ForeignKey(Updates.id, deferrable=True, ondelete='cascade'), ForeignKey(GalaxyHistory.tick, deferrable=True), primary_key=True, autoincrement=False)
    id = Column(Integer, ForeignKey(Planet.id), primary_key=True, autoincrement=False)
    x = Column(Integer, ForeignKey(GalaxyHistory.x))
    y = Column(Integer, ForeignKey(GalaxyHistory.y))
    z = Column(Integer)
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
Planet.history_loader = dynamic_loader(PlanetHistory, backref="current")
Planet2GalaxyH = and_(GalaxyHistory.x==PlanetHistory.x,
                      GalaxyHistory.y==PlanetHistory.y,
                      GalaxyHistory.tick==PlanetHistory.tick)
PlanetHistory.galaxy = relation(GalaxyHistory, backref="planets", primaryjoin=Planet2GalaxyH)
GalaxyHistory.planet_loader = dynamic_loader(PlanetHistory, primaryjoin=Planet2GalaxyH)
class PlanetExiles(Base):
    __tablename__ = 'planet_exiles'
    tick = Column(Integer, ForeignKey(Updates.id, deferrable=True, ondelete='cascade'), primary_key=True, autoincrement=False)
    id = Column(Integer, ForeignKey(Planet.id), primary_key=True, autoincrement=False)
    oldx = Column(Integer)
    oldy = Column(Integer)
    oldz = Column(Integer)
    newx = Column(Integer)
    newy = Column(Integer)
    newz = Column(Integer)

class Alliance(Base):
    __tablename__ = 'alliance'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    name = Column(String(20), index=True)
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
    tick = Column(Integer, ForeignKey(Updates.id, deferrable=True, ondelete='cascade'), primary_key=True, autoincrement=False)
    id = Column(Integer, ForeignKey(Alliance.id), primary_key=True, autoincrement=False)
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
Alliance.history_loader = dynamic_loader(AllianceHistory, backref="current")

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
    planet_id = Column(Integer, ForeignKey(Planet.id, deferrable=True, ondelete='set null'), index=True, unique=True)
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
Planet.user = relation(User, uselist=False, backref="planet")
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
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    friend_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))

User.phonefriends = relation(User,  secondary=PhoneFriend.__table__,
                                  primaryjoin=PhoneFriend.user_id   == User.id,
                                secondaryjoin=PhoneFriend.friend_id == User.id) # Asc
PhoneFriend.user = relation(User, primaryjoin=PhoneFriend.user_id==User.id)
PhoneFriend.friend = relation(User, primaryjoin=PhoneFriend.friend_id==User.id)

'''
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
'''

# ########################################################################### #
# ############################    INTEL TABLE    ############################ #
# ########################################################################### #

class Intel(Base):
    __tablename__ = 'intel'
    planet_id = Column(Integer, ForeignKey(Planet.id), primary_key=True, autoincrement=False)
    alliance_id = Column(Integer, ForeignKey(Alliance.id), index=True)
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
Planet.intel = relation(Intel, uselist=False, backref="planet")
Intel.alliance = relation(Alliance)
#Planet.alliance = relation(Alliance, Intel.__table__, uselist=False, viewonly=True, backref="planets")
Alliance.planets = relation(Planet, Intel.__table__, viewonly=True)

# ########################################################################### #
# #############################    BOOKINGS    ############################## #
# ########################################################################### #

class Target(Base):
    __tablename__ = 'target'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True)
    planet_id = Column(Integer, ForeignKey(Planet.id), ForeignKey(Intel.planet_id), index=True)
    tick = Column(Integer)
    unique = UniqueConstraint('planet_id','tick')
User.bookings = dynamic_loader(Target, backref="user")
Planet.bookings = dynamic_loader(Target, backref="planet")
Galaxy.bookings = dynamic_loader(Target, Planet.__table__, primaryjoin=Planet2Galaxy)
Alliance.bookings = dynamic_loader(Target, Intel.__table__)

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

# ########################################################################### #
# ###############################    SCANS    ############################### #
# ########################################################################### #

class Scan(Base):
    __tablename__ = 'scan'
    id = Column(Integer, primary_key=True)
    planet_id = Column(Integer, ForeignKey(Planet.id), index=True)
    scantype = Column(String(1))
    tick = Column(Integer)
    pa_id = Column(String(32), index=True, unique=True)
    group_id = Column(String(32))
    scanner_id = Column(Integer, ForeignKey(User.id))
Planet.scans = dynamic_loader(Scan, backref="planet")
Scan.scanner = relation(User, backref="scans")

class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, ForeignKey(User.id))
    planet_id = Column(Integer, ForeignKey(Planet.id), index=True)
    scantype = Column(String(1))
    dists = Column(Integer)
    scan_id = Column(Integer, ForeignKey(Scan.id))
Request.user = relation(User, backref="requests")
Request.target = relation(Planet)
Request.scan = relation(Scan)

class PlanetScan(Base):
    __tablename__ = 'planetscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id))
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
Scan.planetscan = relation(PlanetScan, uselist=False)

class DevScan(Base):
    __tablename__ = 'devscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id))
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
Scan.devscan = relation(DevScan, uselist=False)

class UnitScan(Base):
    __tablename__ = 'unitscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id))
    ship_id = Column(Integer, ForeignKey(Ship.id))
    amount = Column(Integer)
Scan.units = relation(UnitScan)
UnitScan.ship = relation(Ship)

class FleetScan(Base):
    __tablename__ = 'fleetscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id))
    owner_id = Column(Integer, ForeignKey(Planet.id))
    target_id = Column(Integer, ForeignKey(Planet.id))
    fleet_size = Column(Integer)
    fleet_name = Column(String(24))
    launch_tick = Column(Integer)
    landing_tick = Column(Integer)
    mission = Column(String(7))
    unique = UniqueConstraint('owner_id','target_id','fleet_size','fleet_name','landing_tick','mission')
Scan.fleets = relation(FleetScan)
FleetScan.owner = relation(Planet, primaryjoin=FleetScan.owner_id==Planet.id)
FleetScan.target = relation(Planet, primaryjoin=FleetScan.target_id==Planet.id)

class CovOp(Base):
    __tablename__ = 'covop'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id))
    covopper_id = Column(Integer, ForeignKey(Planet.id))
    target_id = Column(Integer, ForeignKey(Planet.id))
Scan.covops = relation(CovOp)
CovOp.covopper = relation(Planet, primaryjoin=CovOp.covopper_id==Planet.id)
CovOp.target = relation(Planet, primaryjoin=CovOp.target_id==Planet.id)

# ########################################################################### #
# ############################    PENIS CACHE    ############################ #
# ########################################################################### #

class epenis(Base):
    __tablename__ = 'epenis'
    rank = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), index=True)
    penis = Column(Integer)
User.epenis = relation(epenis, uselist=False)
User.penis = association_proxy("epenis", "penis")
class galpenis(Base):
    __tablename__ = 'galpenis'
    rank = Column(Integer, primary_key=True)
    galaxy_id = Column(Integer, ForeignKey(Galaxy.id), index=True)
    penis = Column(Integer)
Galaxy.galpenis = relation(galpenis, uselist=False)
Galaxy.penis = association_proxy("galpenis", "penis")
class apenis(Base):
    __tablename__ = 'apenis'
    rank = Column(Integer, primary_key=True)
    alliance_id = Column(Integer, ForeignKey(Alliance.id), index=True)
    penis = Column(Integer)
Alliance.apenis = relation(apenis, uselist=False)
Alliance.penis = association_proxy("apenis", "penis")
