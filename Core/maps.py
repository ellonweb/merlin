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
 
import hashlib
from math import ceil
import re
import sys
from time import time
from sqlalchemy import *
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates, relation, backref, dynamic_loader
from sqlalchemy.sql import desc
from sqlalchemy.sql.functions import current_timestamp

from Core.config import Config
from Core.paconf import PA
from Core.db import Base, session

# ########################################################################### #
# #############################    DUMP TABLES    ########################### #
# ########################################################################### #

class Updates(Base):
    __tablename__ = 'updates'
    id = Column(Integer, primary_key=True, autoincrement=False)
    galaxies = Column(Integer)
    planets = Column(Integer)
    alliances = Column(Integer)
    timestamp = Column(DateTime, default=current_timestamp())
    
    @staticmethod
    def current_tick():
        tick = session.query(Updates.id).order_by(desc(Updates.id)).scalar() or 0
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
    def load(x,y, active=True):
        Q = session.query(Galaxy)
        if active is True:
            Q = Q.filter_by(active=True)
        Q = Q.filter_by(x=x, y=y)
        galaxy = Q.first()
        return galaxy
    
    def __str__(self):
        retstr="%s:%s '%s' " % (self.x,self.y,self.name)
        retstr+="Score: %s (%s) " % (self.score,self.score_rank)
        retstr+="Value: %s (%s) " % (self.value,self.value_rank)
        retstr+="Size: %s (%s) " % (self.size,self.size_rank)
        retstr+="XP: %s (%s) " % (self.xp,self.xp_rank)
        return retstr
Galaxy._idx_x_y = Index('galaxy_x_y', Galaxy.x, Galaxy.y, unique=True)
class GalaxyHistory(Base):
    __tablename__ = 'galaxy_history'
    __table_args__ = (UniqueConstraint('x', 'y', 'tick'), {})
    tick = Column(Integer, ForeignKey(Updates.id, ondelete='cascade'), primary_key=True, autoincrement=False)
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
    __table_args__ = (ForeignKeyConstraint(('x', 'y',), (Galaxy.x, Galaxy.y,)), {})
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    x = Column(Integer)
    y = Column(Integer)
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
    vdiff = Column(Integer)
    idle = Column(Integer)
    
    def history(self, tick):
        return self.history_loader.filter_by(tick=tick).first()
    
    def scan(self, type):
        return self.scans.filter_by(scantype=type[0].upper()).order_by(desc(Scan.id)).first()
    
    @staticmethod
    def load(x,y,z, active=True):
        Q = session.query(Planet)
        if active is True:
            Q = Q.filter_by(active=True)
        Q = Q.filter_by(x=x, y=y, z=z)
        planet = Q.first()
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
        bravery = max(0,( min(2,float(target.value)/self.value)-0.1 ) * (min(2,float(target.score)/self.score)-0.2))*10
        return bravery
    
    def calc_xp(self, target, cap=None):
        cap = cap or target.maxcap(self)
        return int(cap * self.bravery(target))
    
    def caprate(self, attacker=None):
        maxcap = PA.getfloat("roids","maxcap")
        if not attacker or not self.value:
            return maxcap
        modifier=(float(self.value)/float(attacker.value))**0.5
        return min(maxcap*modifier, maxcap)
    
    def maxcap(self, attacker=None):
        return int(self.size * self.caprate(attacker))
Planet._idx_x_y_z = Index('planet_x_y_z', Planet.x, Planet.y, Planet.z)
Galaxy.planets = relation(Planet, order_by=Planet.z, backref="galaxy")
Galaxy.planet_loader = dynamic_loader(Planet)
class PlanetHistory(Base):
    __tablename__ = 'planet_history'
    __table_args__ = (ForeignKeyConstraint(('x', 'y', 'tick',), (GalaxyHistory.x, GalaxyHistory.y, GalaxyHistory.tick,)), {})
    tick = Column(Integer, ForeignKey(Updates.id, ondelete='cascade'), primary_key=True, autoincrement=False)
    id = Column(Integer, ForeignKey(Planet.id), primary_key=True, autoincrement=False)
    x = Column(Integer)
    y = Column(Integer)
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
GalaxyHistory.planets = relation(PlanetHistory, order_by=PlanetHistory.z, backref="galaxy")
GalaxyHistory.planet_loader = dynamic_loader(PlanetHistory)
class PlanetExiles(Base):
    __tablename__ = 'planet_exiles'
    tick = Column(Integer, ForeignKey(Updates.id, ondelete='cascade'), primary_key=True, autoincrement=False)
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
    def load(name, active=True):
        Q = session.query(Alliance)
        if active is True:
            Q = Q.filter_by(active=True)
        alliance = Q.filter(Alliance.name.ilike(name)).first()
        if alliance is None:
            alliance = Q.filter(Alliance.name.ilike("%"+name+"%")).first()
        return alliance
    
    def __str__(self):
        retstr="'%s' Members: %s (%s) " % (self.name,self.members,self.members_rank)
        retstr+="Score: %s (%s) Avg: %s (%s) " % (self.score,self.score_rank,self.score_avg,self.score_avg_rank)
        retstr+="Size: %s (%s) Avg: %s (%s)" % (self.size,self.size_rank,self.size_avg,self.size_avg_rank)
        return retstr
class AllianceHistory(Base):
    __tablename__ = 'alliance_history'
    tick = Column(Integer, ForeignKey(Updates.id, ondelete='cascade'), primary_key=True, autoincrement=False)
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
# ##########################    EXCALIBUR TABLES    ######################### #
# ########################################################################### #

galaxy_temp = Table('galaxy_temp', Base.metadata,
    Column('id', Integer),
    Column('x', Integer, primary_key=True),
    Column('y', Integer, primary_key=True),
    Column('name', String(64)),
    Column('size', Integer),
    Column('score', Integer),
    Column('value', Integer),
    Column('xp', Integer))
planet_temp = Table('planet_temp', Base.metadata,
    Column('id', Integer),
    Column('x', Integer, primary_key=True),
    Column('y', Integer, primary_key=True),
    Column('z', Integer, primary_key=True),
    Column('planetname', String(20)),
    Column('rulername', String(20)),
    Column('race', String(3)),
    Column('size', Integer),
    Column('score', Integer),
    Column('value', Integer),
    Column('xp', Integer))
alliance_temp = Table('alliance_temp', Base.metadata,
    Column('id', Integer),
    Column('name', String(20), primary_key=True),
    Column('size', Integer),
    Column('members', Integer),
    Column('score', Integer),
    Column('score_rank', Integer),
    Column('size_avg', Integer),
    Column('score_avg', Integer))
planet_new_id_search = Table('planet_new_id_search', Base.metadata,
    Column('id', Integer),
    Column('x', Integer, primary_key=True),
    Column('y', Integer, primary_key=True),
    Column('z', Integer, primary_key=True),
    Column('race', String(3)),
    Column('size', Integer),
    Column('score', Integer),
    Column('value', Integer),
    Column('xp', Integer))
planet_old_id_search = Table('planet_old_id_search', Base.metadata,
    Column('id', Integer),
    Column('x', Integer, primary_key=True),
    Column('y', Integer, primary_key=True),
    Column('z', Integer, primary_key=True),
    Column('race', String(3)),
    Column('size', Integer),
    Column('score', Integer),
    Column('value', Integer),
    Column('xp', Integer),
    Column('vdiff', Integer))

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
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='set null'), index=True)
    email = Column(String(32))
    phone = Column(String(32))
    pubphone = Column(Boolean, default=False) # Asc
    sponsor = Column(String(15)) # Asc
    quits = Column(Integer, default=0) # Asc
    emailre = re.compile("^([\w.-]+@[\w.-]+)")
    
    @validates('passwd')
    def valid_passwd(self, key, passwd):
        return User.hasher(passwd)
    @validates('email')
    def valid_email(self, key, email):
        assert self.emailre.match(email)
        return email
    
    @staticmethod
    def hasher(passwd):
        # *Every* user password operation should go through this function
        # This can be easily adapted to use SHA1 instead, or add salts
        return hashlib.md5(passwd).hexdigest()
    
    @staticmethod
    def load(name=None, id=None, passwd=None, exact=True, active=True):
        assert id or name
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
        return user
Planet.user = relation(User, uselist=False, backref="planet")
def user_access_function(num):
    # Function generator for access check
    def func(self):
        if self.access >= num:
            return True
    return func
for lvl, num in Config.items("Access"):
    # Bind user access functions
    setattr(User, "is_"+lvl, user_access_function(int(num)))

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
    def load(name, session=None):
        s = session or Session()
        Q = s.query(Gimp)
        Q = Q.filter(Gimp.name.ilike(name))
        gimp = Q.first()
        s.close() if session is None else None
        return gimp

Gimp.sponsor = relation(User, primaryjoin=Gimp.sponsor_id==User.id, backref='gimps')
'''

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String(150))
    userlevel = Column(Integer)
    maxlevel = Column(Integer)
    
    @staticmethod
    def load(name):
        Q = session.query(Channel)
        channel = Q.filter(Channel.name.ilike(name)).first()
        return channel

# ########################################################################### #
# ############################    INTEL TABLE    ############################ #
# ########################################################################### #

class Intel(Base):
    __tablename__ = 'intel'
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'), primary_key=True, autoincrement=False)
    alliance_id = Column(Integer, ForeignKey(Alliance.id, ondelete='set null'), index=True)
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
            ret += " fakenick=%s"%(self.fakenick,)
        if self.defwhore:
            ret += " defwhore=%s"%(self.defwhore,)
        if self.covop:
            ret += " covop=%s"%(self.covop,)
        if self.scanner:
            ret += " scanner=%s"%(self.scanner,)
        if self.dists:
            ret += " dists=%s"%(self.dists,)
        if self.bg:
            ret += " bg=%s"%(self.bg,)
        if self.gov:
            ret += " gov=%s"%(self.gov,)
        if self.relay:
            ret += " relay=%s"%(self.relay,)
        if self.reportchan:
            ret += " reportchan=%s"%(self.reportchan,)
        if self.comment:
            ret += " comment=%s"%(self.comment,)
        return ret
Planet.intel = relation(Intel, uselist=False, backref="planet")
Galaxy.intel = relation(Intel, Planet.__table__, order_by=Planet.z)
Intel.alliance = relation(Alliance)
#Planet.alliance = relation(Alliance, Intel.__table__, uselist=False, viewonly=True, backref="planets")
Planet.alliance = association_proxy("intel", "alliance")
Alliance.planets = relation(Planet, Intel.__table__, order_by=(Planet.x, Planet.y, Planet.z), viewonly=True)

# ########################################################################### #
# #############################    BOOKINGS    ############################## #
# ########################################################################### #

class Target(Base):
    __tablename__ = 'target'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), index=True)
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'), index=True)
    tick = Column(Integer)
    unique = UniqueConstraint('planet_id','tick')
User.bookings = dynamic_loader(Target, backref="user")
Planet.bookings = dynamic_loader(Target, backref="planet")
Galaxy.bookings = dynamic_loader(Target, Planet.__table__)
#Alliance.bookings = dynamic_loader(Target, Intel.__table__)

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
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'), index=True)
    scantype = Column(String(1))
    tick = Column(Integer)
    pa_id = Column(String(32), index=True, unique=True)
    group_id = Column(String(32))
    scanner_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    
    def __str__(self):
        p = self.planet
        head = "%s on %s:%s:%s " % (PA.get(self.scantype,"name"),p.x,p.y,p.z,)
        id_tick = "(id: %s, pt: %s)" % (self.pa_id,self.tick,)
        id_age_value = "(id: %s, age: %s, value diff: %s)" % (self.pa_id,Updates.current_tick()-self.tick,p.value-p.history(self.tick).value)
        if self.scantype in ("P",):
            return head + id_tick + str(self.planetscan)
        if self.scantype in ("D",):
            return head + id_tick + str(self.devscan)
        if self.scantype in ("U","A",):
            return head + id_age_value + " " + " | ".join(map(str,self.units))
        if self.scantype == "J":
            return head + id_tick + " " + " | ".join(map(str,self.fleets))
        if self.scantype == "N":
            return head + Config.get("URL","viewscan") % (self.pa_id,)
Planet.scans = dynamic_loader(Scan, backref="planet")
Scan.scanner = relation(User, backref="scans")

class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'), index=True)
    scantype = Column(String(1))
    dists = Column(Integer)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='set null'))
Request.user = relation(User, backref="requests")
Request.target = relation(Planet)
Request.scan = relation(Scan)

class PlanetScan(Base):
    __tablename__ = 'planetscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='cascade'))
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
    def __str__(self):
        reply = " Roids: (m:%s, c:%s, e:%s) |" % (self.roid_metal,self.roid_crystal,self.roid_eonium,)
        reply+= " Resources: (m:%s, c:%s, e:%s) |" % (self.res_metal,self.res_crystal,self.res_eonium,)
        reply+= " Hidden: %s | Agents: %s | Guards: %s" % (self.prod_res,self.agents,self.guards,)
        return reply
Scan.planetscan = relation(PlanetScan, uselist=False, backref="scan")

class DevScan(Base):
    __tablename__ = 'devscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='cascade'))
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
    def infra_str(self):
        level = self.infrastructure
        if level==0:
            return "10 constructions"
        if level==1:
            return "20 constructions"
        if level==2:
            return "50 constructions"
        if level==3:
            return "100 constructions"
        if level==4:
            return "150 constructions"
    
    def hulls_str(self):
        level = self.hulls
        if level==1:
            return "FI/CO"
        if level==2:
            return "FR/DE"
        if level==3:
            return "CR/BS"
    
    def waves_str(self):
        level = self.waves
        if level==0:
            return "Planet"
        if level==1:
            return "Surface"
        if level==2:
            return "Technology"
        if level==3:
            return "Unit"
        if level==4:
            return "News"
        if level==5:
            return "Fleet"
        if level==6:
            return "JGP"
        if level==7:
            return "Advanced Unit"
    
    def covop_str(self):
        level = self.covert_op
        if level==0:
            return "Research Hack"
        if level==1:
            return "Raise Stealth"
        if level==2:
            return "Blow up roids"
        if level==3:
            return "Blow up shits"
        if level==4:
            return "Blow up Amps/Dists"
        if level==5:
            return "Resource hacking (OMG!)"
        if level==6:
            return "Blow up Strucs"
    
    def mining_str(self):
        level = self.mining+1
        if level==0:
            return "50 roids"
        if level==1:
            return "100 roids (scanner!)"
        if level==2:
            return "200 roids"
        if level==3:
            return "300 roids"
        if level==4:
            return "500 roids"
        if level==5:
            return "750 roids"
        if level==6:
            return "1k roids"
        if level==7:
            return "1250 roids"
        if level==8:
            return "1500 roids"
        if level==9:
            return "Jan 1. 1900"
        if level==10:
            return "2500 roids"
        if level==11:
            return "3000 roids"
        if level==12:
            return "3500 roids"
        if level==13:
            return "4500 roids"
        if level==14:
            return "5500 roids"
        if level==15:
            return "6500 roids"
        if level==16:
            return "8000 roids"
        if level==17:
            return "top10 or dumb"
    
    def total(self):
        total = self.light_factory+self.medium_factory+self.heavy_factory
        total+= self.wave_amplifier+self.wave_distorter
        total+= self.metal_refinery+self.crystal_refinery+self.eonium_refinery
        total+= self.research_lab+self.finance_centre+self.security_centre
        return total
        
    def __str__(self):
        reply = " Travel: %s, Infrajerome: %s, Hulls: %s," % (self.travel,self.infra_str(),self.hulls_str(),)
        reply+= " Waves: %s, Core: %s, Covop: %s, Mining: %s" % (self.waves_str(),self.core,self.covop_str(),self.mining_str(),)
        reply+= "\n"
        reply+= " Structures: LFac: %s, MFac: %s, HFac: %s, Amp: %s," % (self.light_factory,self.medium_factory,self.heavy_factory,self.wave_amplifier,)
        reply+= " Dist: %s, MRef: %s, CRef: %s, ERef: %s," % (self.wave_distorter,self.metal_refinery,self.crystal_refinery,self.eonium_refinery,)
        reply+= " ResLab: %s (%s%%), FC: %s, Sec: %s (%s%%)" % (self.research_lab,int(float(self.research_lab)/self.total()*100),self.finance_centre,self.security_centre,int(float(self.security_centre)/self.total()*100),)
        return reply
Scan.devscan = relation(DevScan, uselist=False, backref="scan")

class UnitScan(Base):
    __tablename__ = 'unitscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='cascade'))
    ship_id = Column(Integer, ForeignKey(Ship.id, ondelete='cascade'))
    amount = Column(Integer)
    def __str__(self):
        return "%s %s" % (self.ship.name, self.amount,)
Scan.units = relation(UnitScan, backref="scan")
UnitScan.ship = relation(Ship)

class FleetScan(Base):
    __tablename__ = 'fleetscan'
    __table_args__ = (UniqueConstraint('owner_id','target_id','fleet_size','fleet_name','landing_tick','mission'), {})
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='cascade'))
    owner_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'))
    target_id = Column(Integer, ForeignKey(Planet.id, ondelete='set null'))
    fleet_size = Column(Integer)
    fleet_name = Column(String(24))
    launch_tick = Column(Integer)
    landing_tick = Column(Integer)
    mission = Column(String(7))
    def __str__(self):
        p = self.owner
        return "(%s:%s:%s %s | %s %s %s)" % (p.x,p.y,p.z,self.fleet_name,self.fleet_size,self.mission,self.landing_tick-self.scan.tick,)
Scan.fleets = relation(FleetScan, backref="scan")
FleetScan.owner = relation(Planet, primaryjoin=FleetScan.owner_id==Planet.id)
FleetScan.target = relation(Planet, primaryjoin=FleetScan.target_id==Planet.id)

class CovOp(Base):
    __tablename__ = 'covop'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='cascade'))
    covopper_id = Column(Integer, ForeignKey(Planet.id, ondelete='set null'))
    target_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'))
Scan.covops = relation(CovOp, backref="scan")
CovOp.covopper = relation(Planet, primaryjoin=CovOp.covopper_id==Planet.id)
CovOp.target = relation(Planet, primaryjoin=CovOp.target_id==Planet.id)

# ########################################################################### #
# ############################    PENIS CACHE    ############################ #
# ########################################################################### #

class epenis(Base):
    __tablename__ = 'epenis'
    rank = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), index=True)
    penis = Column(Integer)
User.epenis = relation(epenis, uselist=False)
User.penis = association_proxy("epenis", "penis")
class galpenis(Base):
    __tablename__ = 'galpenis'
    rank = Column(Integer, primary_key=True)
    galaxy_id = Column(Integer, ForeignKey(Galaxy.id, ondelete='cascade'), index=True)
    penis = Column(Integer)
Galaxy.galpenis = relation(galpenis, uselist=False)
Galaxy.penis = association_proxy("galpenis", "penis")
class apenis(Base):
    __tablename__ = 'apenis'
    rank = Column(Integer, primary_key=True)
    alliance_id = Column(Integer, ForeignKey(Alliance.id, ondelete='cascade'), index=True)
    penis = Column(Integer)
Alliance.apenis = relation(apenis, uselist=False)
Alliance.penis = association_proxy("apenis", "penis")
