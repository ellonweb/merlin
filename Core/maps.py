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
 
from datetime import datetime
import hashlib
from math import ceil
import re
import sys
from sqlalchemy import *
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates, relation, backref, dynamic_loader, aliased
from sqlalchemy.sql.functions import coalesce, count, current_timestamp, random

from Core.exceptions_ import LoadableError
from Core.config import Config
from Core.paconf import PA
from Core.string import encode
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
        from sqlalchemy.sql.functions import max
        tick = session.query(max(Updates.id)).scalar() or 0
        return tick
    
    @staticmethod
    def midnight_tick():
        now = datetime.utcnow()
        hours = now.hour
        tick = Updates.current_tick() - hours
        return tick
    
    @staticmethod
    def week_tick():
        tick = Updates.current_tick() - (24 * 7)
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
    members = Column(Integer)
    ratio = Column(Float)
    size_rank = Column(Integer)
    score_rank = Column(Integer)
    value_rank = Column(Integer)
    xp_rank = Column(Integer)
    size_growth = Column(Integer)
    score_growth = Column(Integer)
    value_growth = Column(Integer)
    xp_growth = Column(Integer)
    member_growth = Column(Integer)
    size_growth_pc = Column(Float)
    score_growth_pc = Column(Float)
    value_growth_pc = Column(Float)
    xp_growth_pc = Column(Float)
    size_rank_change = Column(Integer)
    score_rank_change = Column(Integer)
    value_rank_change = Column(Integer)
    xp_rank_change = Column(Integer)
    private = Column(Boolean)
    
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
        retstr="%s:%s '%s' (%s) " % (self.x,self.y,self.name,self.planet_loader.filter_by(active=True).count())
        retstr+="Score: %s (%s) " % (self.score,self.score_rank)
        retstr+="Value: %s (%s) " % (self.value,self.value_rank)
        retstr+="Size: %s (%s) " % (self.size,self.size_rank)
        retstr+="XP: %s (%s) " % (self.xp,self.xp_rank)
        return encode(retstr)
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
    age = Column(Integer)
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
    ratio = Column(Float)
    size_rank = Column(Integer)
    score_rank = Column(Integer)
    value_rank = Column(Integer)
    xp_rank = Column(Integer)
    size_growth = Column(Integer)
    score_growth = Column(Integer)
    value_growth = Column(Integer)
    xp_growth = Column(Integer)
    size_growth_pc = Column(Float)
    score_growth_pc = Column(Float)
    value_growth_pc = Column(Float)
    xp_growth_pc = Column(Float)
    size_rank_change = Column(Integer)
    score_rank_change = Column(Integer)
    value_rank_change = Column(Integer)
    xp_rank_change = Column(Integer)
    totalroundroids = Column(Integer)
    totallostroids = Column(Integer)
    totalroundroids_rank = Column(Integer)
    totallostroids_rank = Column(Integer)
    totalroundroids_rank_change = Column(Integer)
    totallostroids_rank_change = Column(Integer)
    totalroundroids_growth = Column(Integer)
    totallostroids_growth = Column(Integer)
    totalroundroids_growth_pc = Column(Integer)
    totallostroids_growth_pc = Column(Integer)
    ticksroiding = Column(Integer)
    ticksroided = Column(Integer)
    tickroids = Column(Integer)
    avroids = Column(Float)
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
        return encode(retstr)
        return retstr
    
    def bravery(self, target):
        bravery = max(0,( min(2,float(target.value)/self.value)-0.1 ) * (min(2,float(target.score)/self.score)-0.2))*10
        return bravery
    
    def calc_xp(self, target, cap=None):
        cap = cap or target.maxcap(self)
        return int(cap * self.bravery(target))
    
    def caprate(self, attacker=None):
        maxcap = PA.getfloat("roids","maxcap")
        mincap = PA.getfloat("roids","mincap")
        if not attacker or not self.value:
            return maxcap
        modifier=(float(self.value)/float(attacker.value))**0.5
        return max(mincap,min(maxcap*modifier, maxcap))
    
    def maxcap(self, attacker=None):
        return int(self.size * self.caprate(attacker))
    
    def resources_per_agent(self, target):
        return min(10000,(target.value * 2000)/self.value)
Planet._idx_x_y_z = Index('planet_x_y_z', Planet.x, Planet.y, Planet.z)
Galaxy.planets = relation(Planet, order_by=asc(Planet.z), backref="galaxy")
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
GalaxyHistory.planets = relation(PlanetHistory, order_by=asc(PlanetHistory.z), backref="galaxy")
GalaxyHistory.planet_loader = dynamic_loader(PlanetHistory)
class PlanetExiles(Base):
    __tablename__ = 'planet_exiles'
    __table_args__ = (ForeignKeyConstraint(('oldx', 'oldy',), (Galaxy.x, Galaxy.y,)),
                      ForeignKeyConstraint(('newx', 'newy',), (Galaxy.x, Galaxy.y,)), {})
    tick = Column(Integer, ForeignKey(Updates.id, ondelete='cascade'), primary_key=True, autoincrement=False)
    id = Column(Integer, ForeignKey(Planet.id), primary_key=True, autoincrement=False)
    oldx = Column(Integer)
    oldy = Column(Integer)
    oldz = Column(Integer)
    newx = Column(Integer)
    newy = Column(Integer)
    newz = Column(Integer)
Galaxy.outs = relation(PlanetExiles, backref="old", primaryjoin=and_(Galaxy.x==PlanetExiles.oldx, Galaxy.y==PlanetExiles.oldy),
                                    order_by=(desc(PlanetExiles.tick), asc(PlanetExiles.oldz),))
Galaxy.ins = relation(PlanetExiles, backref="new", primaryjoin=and_(Galaxy.x==PlanetExiles.newx, Galaxy.y==PlanetExiles.newy),
                                    order_by=(desc(PlanetExiles.tick), asc(PlanetExiles.newz),))
PlanetExiles.planet = relation(Planet, backref="exiles", order_by=desc(PlanetExiles.tick))

class Alliance(Base):
    __tablename__ = 'alliance'
    id = Column(Integer, primary_key=True)
    active = Column(Boolean)
    name = Column(String(20), index=True)
    alias = Column(String(20))
    size = Column(Integer)
    members = Column(Integer)
    score = Column(Integer)
    points = Column(Integer)
    size_rank = Column(Integer)
    members_rank = Column(Integer)
    score_rank = Column(Integer)
    points_rank = Column(Integer)
    size_avg = Column(Integer)
    score_avg = Column(Integer)
    points_avg = Column(Integer)
    size_avg_rank = Column(Integer)
    score_avg_rank = Column(Integer)
    points_avg_rank = Column(Integer)
    size_growth = Column(Integer)
    score_growth = Column(Integer)
    points_growth = Column(Integer)
    member_growth = Column(Integer)
    size_growth_pc = Column(Float)
    score_growth_pc = Column(Float)
    points_growth_pc = Column(Float)
    size_avg_growth = Column(Integer)
    score_avg_growth = Column(Integer)
    points_avg_growth = Column(Integer)
    size_avg_growth_pc = Column(Float)
    score_avg_growth_pc = Column(Float)
    points_avg_growth_pc = Column(Float)
    size_rank_change = Column(Integer)
    members_rank_change = Column(Integer)
    score_rank_change = Column(Integer)
    points_rank_change = Column(Integer)
    size_avg_rank_change = Column(Integer)
    score_avg_rank_change = Column(Integer)
    points_avg_rank_change = Column(Integer)
    
    def history(self, tick):
        return self.history_loader.filter_by(tick=tick).first()
    
    @staticmethod
    def load(name, alias=True, active=True):
        filters = (
                    Alliance.name.ilike(name),
                    Alliance.name.ilike(name+"%"),
                    Alliance.name.ilike("%"+name+"%"),
                    Alliance.alias.ilike(name),
                    Alliance.alias.ilike(name+"%"),
                    Alliance.alias.ilike("%"+name+"%"),
                    )
        
        Q = session.query(Alliance).filter_by(active=True)
        for filter in filters:
            alliance = Q.filter(filter).first()
            if alliance is not None:
                break
        
        if alliance is not None or active == True:
            return alliance
        
        Q = session.query(Alliance)
        for filter in filters:
            alliance = Q.filter(filter).first()
            if alliance is not None:
                break
        
        return alliance
    
    def __str__(self):
        retstr="'%s' Members: %s (%s) " % (self.name,self.members,self.members_rank)
        retstr+="Score: %s (%s) Avg: %s (%s) " % (self.score,self.score_rank,self.score_avg,self.score_avg_rank)
        retstr+="Points: %s (%s) " % (self.points,self.points_rank)
        retstr+="Size: %s (%s) Avg: %s (%s)" % (self.size,self.size_rank,self.size_avg,self.size_avg_rank)
        return encode(retstr)
        return retstr
class AllianceHistory(Base):
    __tablename__ = 'alliance_history'
    tick = Column(Integer, ForeignKey(Updates.id, ondelete='cascade'), primary_key=True, autoincrement=False)
    id = Column(Integer, ForeignKey(Alliance.id), primary_key=True, autoincrement=False)
    name = Column(String(20))
    size = Column(Integer)
    members = Column(Integer)
    score = Column(Integer)
    points = Column(Integer)
    size_rank = Column(Integer)
    members_rank = Column(Integer)
    score_rank = Column(Integer)
    points_rank = Column(Integer)
    size_avg = Column(Integer)
    score_avg = Column(Integer)
    points_avg = Column(Integer)
    size_avg_rank = Column(Integer)
    score_avg_rank = Column(Integer)
    points_avg_rank = Column(Integer)
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
    Column('points', Integer),
    Column('score_rank', Integer),
    Column('size_avg', Integer),
    Column('score_avg', Integer),
    Column('points_avg', Integer))
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
    _sms_modes = {"C":"Clickatell", "G":"GoogleVoice", "R":"Retard", "E":"Email",}
    id = Column(Integer, primary_key=True)
    name = Column(String(15)) # pnick
    alias = Column(String(15))
    passwd = Column(String(32))
    active = Column(Boolean, default=True)
    access = Column(Integer)
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='set null'), index=True)
    email = Column(String(32))
    emailre = re.compile(r"^([\w.-]+@[\w.-]+)")
    phone = Column(String(48))
    pubphone = Column(Boolean, default=False) # Asc
    _smsmode = Column(Enum(*_sms_modes.keys(), name="smsmode"))
    sponsor = Column(String(15)) # Asc
    quits = Column(Integer, default=0) # Asc
    available_cookies = Column(Integer, default=0)
    carebears = Column(Integer, default=0)
    last_cookie_date = Column(DateTime)
    fleetcount = Column(Integer, default=0)
    fleetcomment = Column(String(512))
    fleetupdated = Column(Integer, default=0)
    levels = filter(lambda lev: not lev[0] == "galmate", sorted(Config.items("Access"), key=lambda acc: int(acc[1]), reverse=True))
    
    def is_user(self):
        return self in session
    
    @property
    def level(self):
        if not self.active:
            return None
        for level, access in self.levels:
            if self.access >= int(access):
                return level
        return "galmate"
    
    @level.setter
    def level(self, value):
        if value in (True, False,):
            self.active = bool(value)
        else:
            self.access = Config.getint("Access", value)
    
    @property
    def smsmode(self):
        return User._sms_modes.get(self._smsmode)
    @smsmode.setter
    def smsmode(self, mode):
        self._smsmode = mode[0].upper()
    @validates('_smsmode')
    def valid_smsmode(self, key, mode):
        assert mode in User._sms_modes or mode is None
        return mode
    
    @property
    def gimps(self):
        return session.query(User.name).filter(User.sponsor == self.name).all()
    
    @property
    def mums(self):
        from sqlalchemy.sql.functions import sum
        Q = session.query(User.name, sum(Cookie.howmany).label("gac"))
        Q = Q.join(Cookie.giver)
        Q = Q.filter(Cookie.receiver == self)
        Q = Q.group_by(User.name)
        Q = Q.order_by(desc("gac"))
        return Q.all()
    
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
    def load(name=None, id=None, passwd=None, exact=True, active=True, access=0):
        assert id or name
        Q = session.query(User)
        if active is True:
            if access in Config.options("Access"):
                access = Config.getint("Access",access)
            elif type(access) is int:
                pass
            else:
                raise LoadableError("Invalid access level")
            Q = Q.filter(User.active == True).filter(User.access >= access)
        if id is not None:
            user = Q.filter(User.id == id).first()
        if name is not None:
            for filter in (
                            User.name.ilike(name),
                            User.name.ilike(name+"%"),
                            User.alias.ilike(name),
                            User.alias.ilike(name+"%"),
                            User.name.ilike("%"+name+"%"),
                            User.alias.ilike("%"+name+"%"),
                            ):
                user = Q.filter(filter).first()
                if user is not None or exact is True:
                    break
        if (user and passwd) is not None:
            user = user if user.passwd == User.hasher(passwd) else None
        return user
    
    def has_ancestor(self, possible_ancestor):
        ancestor = User.load(name=self.sponsor, access="member")
        if ancestor is not None:
            if ancestor.name.lower() == possible_ancestor.lower():
                return True
            else:
                return ancestor.has_ancestor(possible_ancestor)
        elif self.sponsor == Config.get("Connection", "nick"):
            return False
        else:
            return None
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

class Arthur(Base):
    __tablename__ = 'session'
    key = Column(String(40), primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='set null'))
    expire = Column(DateTime)
    @staticmethod
    def load(key, now=None):
        Q = session.query(Arthur)
        if now is not None:
            Q = Q.filter(Arthur.expire > now)
        auth = Q.filter(Arthur.key == key).first()
        if auth is not None and auth.user is not None and auth.user.active == True:
            return auth
        else:
            return None
Arthur.user = relation(User)

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

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True)
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
    amps = Column(Integer, default=0)
    dists = Column(Integer, default=0)
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
        if self.amps:
            ret += " amps=%s"%(self.amps,)
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
        return encode(ret)
        return ret
Planet.intel = relation(Intel, uselist=False, backref="planet")
Galaxy.intel = relation(Intel, Planet.__table__, order_by=asc(Planet.z))
Intel.alliance = relation(Alliance)
#Planet.alliance = relation(Alliance, Intel.__table__, uselist=False, viewonly=True, backref="planets")
Planet.alliance = association_proxy("intel", "alliance")
Alliance.planets = relation(Planet, Intel.__table__, order_by=(asc(Planet.x), asc(Planet.y), asc(Planet.z)), viewonly=True)

# ########################################################################### #
# #############################    BOOKINGS    ############################## #
# ########################################################################### #

class Target(Base):
    __tablename__ = 'target'
    __table_args__ = (UniqueConstraint('planet_id','tick'), {})
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'), index=True)
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'), index=True)
    tick = Column(Integer)
User.bookings = dynamic_loader(Target, backref="user")
Planet.bookings = dynamic_loader(Target, backref="planet", order_by=(asc(Target.tick)))
Galaxy.bookings = dynamic_loader(Target, Planet.__table__)
#Alliance.bookings = dynamic_loader(Target, Intel.__table__)

class Attack(Base):
    __tablename__ = 'attack'
    id = Column(Integer, primary_key=True)
    landtick = Column(Integer)
    comment = Column(Text)
    _active_ticks = 12
    
    def addPlanet(self, planet):
        if planet in self.planets:
            return
        if planet.intel and planet.alliance and planet.alliance.name == Config.get("Alliance","name"):
            return
        self.planets.append(planet)
        return True
    
    def removePlanet(self, planet):
        if planet in self.planets:
            self.planets.remove(planet)
            return True
    
    def addGalaxy(self, galaxy):
        for planet in galaxy.planets:
            if planet.active:
                self.addPlanet(planet)
    
    def removeGalaxy(self, galaxy):
        for planet in galaxy.planets:
            if planet.active:
                self.removePlanet(planet)
    
    @staticmethod
    def load(id):
        Q = session.query(Attack)
        Q = Q.filter_by(id=id)
        attack = Q.first()
        return attack
    
    @property
    def link(self):
        return "%sattack/%d/" %(Config.get("URL","arthur"), self.id,)
    
    @property
    def active(self):
        return self.landtick >= Updates.current_tick() - Attack._active_ticks
    
    def __str__(self):
        reply = "Attack %d LT: %d %s | %s | Planets: "%(self.id,self.landtick,self.comment,self.link,)
        reply+= ", ".join(map(lambda p: "%s:%s:%s" %(p.x,p.y,p.z,), self.planets))
        return encode(reply)
        return reply
    

class AttackTarget(Base):
    __tablename__ = 'attack_target'
    id = Column(Integer, primary_key=True)
    attack_id = Column(Integer, ForeignKey(Attack.id, ondelete='cascade'))
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'))
Attack.planets = relation(Planet, secondary=AttackTarget.__table__,
                                primaryjoin=AttackTarget.attack_id==Attack.id,
                              secondaryjoin=AttackTarget.planet_id==Planet.id, order_by=(asc(Planet.x), asc(Planet.y), asc(Planet.z)))

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
                ship = Q.filter(Ship.name.ilike(name+"%")).first()
            if ship is None and name[-1].lower()=="s":
                ship = Q.filter(Ship.name.ilike(name[:-1]+"%")).first()
            if ship is None and name[-3:].lower()=="ies":
                ship = Q.filter(Ship.name.ilike(name[:-3]+"%")).first()
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
    __table_args__ = (UniqueConstraint('pa_id','tick'), {})
    _scan_types = sorted(PA.options("scans"), cmp=lambda x,y: cmp(PA.getint(x, "type"), PA.getint(y, "type")))
    id = Column(Integer, primary_key=True)
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'), index=True)
    scantype = Column(Enum(*_scan_types, name="scantype"))
    tick = Column(Integer)
    pa_id = Column(String(32), index=True)
    group_id = Column(String(32), index=True)
    scanner_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    
    @property
    def type(self):
        return PA.get(self.scantype,"name")
    
    @property
    def link(self):
        return Config.get("URL","viewscan") % (self.pa_id,)
    
    def ship_count(self, cloak):
        if self.scantype not in ("U","A",):
            return
        
        count = 0
        for unitscan in self.units:
            count += unitscan.amount if cloak else unitscan.visible
        
        return count
    
    def ship_value(self):
        if self.scantype not in ("U","A",):
            return
        
        value = 0
        for unitscan in self.units:
            value += unitscan.amount * unitscan.ship.total_cost / 100
        
        return value
    
    def bcalc(self, target):
        if self.scantype not in ("U","A",):
            return
        
        bcalc = Config.get("URL","bcalc")
        for unitscan in self.units:
            bcalc += "%s_1_%d=%d&" % (("att", "def",)[target], unitscan.ship_id - 1, unitscan.amount,)
        bcalc += "%s_planet_value_1=%d&" % (("att", "def",)[target], self.planet.value,)
        bcalc += "%s_planet_score_1=%d&" % (("att", "def",)[target], self.planet.score,)
        
        if target:
            pscan = self.planet.scan("P")
            if pscan and pscan.planetscan.size == self.planet.size:
                bcalc += "def_metal_asteroids=%d&" % (pscan.planetscan.roid_metal,)
                bcalc += "def_crystal_asteroids=%d&" % (pscan.planetscan.roid_crystal,)
                bcalc += "def_eonium_asteroids=%d&" % (pscan.planetscan.roid_eonium,)
            else:
                bcalc += "def_metal_asteroids=%d&" % (self.planet.size,)
            
            dscan = self.planet.scan("D")
            if dscan:
                bcalc += "def_structures=%d&" % (dscan.devscan.total,)
        
        return bcalc
    
    @property
    def total_hostile(self):
        if self.scantype not in ("J",):
            return
        return sum([fleet.fleet_size for fleet in self.fleets if fleet.mission.lower() == "attack"])
    
    @property
    def total_hostile_fleets(self):
        if self.scantype not in ("J",):
            return
        return len([fleet for fleet in self.fleets if fleet.mission.lower() == "attack"])
    
    @property
    def total_friendly(self):
        if self.scantype not in ("J",):
            return
        return sum([fleet.fleet_size for fleet in self.fleets if fleet.mission.lower() == "defend"])
    
    @property
    def total_friendly_fleets(self):
        if self.scantype not in ("J",):
            return
        return len([fleet for fleet in self.fleets if fleet.mission.lower() == "defend"])
    
    def fleet_overview(self):
        if self.scantype not in ("J",):
            return
        
        from sqlalchemy.sql.functions import min, sum
        f=aliased(FleetScan)
        a=aliased(FleetScan)
        d=aliased(FleetScan)
        
        Q = session.query(f.landing_tick, f.landing_tick - min(Scan.tick),
                            count(a.id), coalesce(sum(a.fleet_size),0),
                            count(d.id), coalesce(sum(d.fleet_size),0))
        Q = Q.join(f.scan)
        Q = Q.filter(f.scan == self)
        
        Q = Q.outerjoin((a, and_(a.id==f.id, a.mission.ilike("Attack"))))
        Q = Q.outerjoin((d, and_(d.id==f.id, d.mission.ilike("Defend"))))

        Q = Q.group_by(f.landing_tick)
        Q = Q.order_by(asc(f.landing_tick))
        return Q.all()
    
    def __str__(self):
        p = self.planet
        ph = p.history(self.tick)
        
        head = "%s on %s:%s:%s " % (self.type,p.x,p.y,p.z,)
        pa_id = self.pa_id
        pa_id = encode(self.pa_id)
        id_tick = "(id: %s, pt: %s)" % (pa_id,self.tick,)
        vdiff = p.value-ph.value if ph else None
        id_age_value = "(id: %s, age: %s, value diff: %s)" % (pa_id,Updates.current_tick()-self.tick,vdiff)
        
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
    _requestable = [(type, PA.get(type, "name"),) for type in Scan._scan_types if PA.getboolean(type, "request")]
    id = Column(Integer, primary_key=True)
    requester_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    planet_id = Column(Integer, ForeignKey(Planet.id, ondelete='cascade'), index=True)
    scantype = Column(Enum(*Scan._scan_types, name="scantype"))
    dists = Column(Integer)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='set null'))
    active = Column(Boolean, default=True)
    tick = Column(Integer,default=Updates.current_tick)
    
    @staticmethod
    def load(id, active=True):
        Q = session.query(Request)
        Q = Q.filter_by(active = True) if active == True else Q
        request = Q.filter_by(id = id).first()
        return request
        
    @property
    def link(self):
        return Config.get("URL", "reqscan") % (PA.get(self.scantype, "type"), self.target.x, self.target.y, self.target.z,)
    
    @property
    def type(self):
        return PA.get(self.scantype,"name")
    
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
    
    @property
    def size(self):
        return self.roid_metal + self.roid_crystal + self.roid_eonium
    
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
    
    def travel_str(self):
        return "eta -%s" %(self.travel,)
    
    def infra_str(self):
        level = self.infrastructure
        if level==0:
            return "20 constructions"
        if level==1:
            return "50 constructions"
        if level==2:
            return "100 constructions"
        if level==3:
            return "150 constructions"
        if level==4:
            return "250 constructions"
    
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
            return "Landing"
        if level==2:
            return "Development"
        if level==3:
            return "Unit"
        if level==4:
            return "News"
        if level==5:
            return "Incoming"
        if level==6:
            return "JGP"
        if level==7:
            return "Advanced Unit"
    
    def core_str(self):
        return ("1000","3500","6000","9000","12000")[self.core] + " ept"
    
    def covop_str(self):
        level = self.covert_op
        if level==0:
            return "Research hack"
        if level==1:
            return "Lower stealth"
        if level==2:
            return "Blow up roids"
        if level==3:
            return "Blow up ships"
        if level==4:
            return "Blow up guards"
        if level==5:
            return "Blow up amps/dists"
        if level==6:
            return "Resource hacking (OMG!)"
        if level==7:
            return "Blow up strucs"
    
    def mining_str(self):
        level = self.mining
        if level==0:
            return "100 roids (scanner!)"
        if level==1:
            return "200 roids"
        if level==2:
            return "300 roids"
        if level==3:
            return "500 roids"
        if level==4:
            return "750 roids"
        if level==5:
            return "1k roids"
        if level==6:
            return "1250 roids"
        if level==7:
            return "1500 roids"
        if level==8:
            return "Jan 1. 1900"
        if level==9:
            return "2500 roids"
        if level==10:
            return "3000 roids"
        if level==11:
            return "3500 roids"
        if level==12:
            return "4500 roids"
        if level==13:
            return "5500 roids"
        if level==14:
            return "6500 roids"
        if level==15:
            return "8000 roids"
        if level==16:
            return "top10 or dumb"
    
    @property
    def total(self):
        total = self.light_factory+self.medium_factory+self.heavy_factory
        total+= self.wave_amplifier+self.wave_distorter
        total+= self.metal_refinery+self.crystal_refinery+self.eonium_refinery
        total+= self.research_lab+self.finance_centre+self.security_centre
        return total
        
    def __str__(self):
        reply = " Travel: %s, Infrajerome: %s, Hulls: %s," % (self.travel_str(),self.infra_str(),self.hulls_str(),)
        reply+= " Waves: %s, Core: %s, Covop: %s, Mining: %s" % (self.waves_str(),self.core_str(),self.covop_str(),self.mining_str(),)
        reply+= "\n"
        reply+= "Structures: LFac: %s, MFac: %s, HFac: %s, Amp: %s," % (self.light_factory,self.medium_factory,self.heavy_factory,self.wave_amplifier,)
        reply+= " Dist: %s, MRef: %s, CRef: %s, ERef: %s," % (self.wave_distorter,self.metal_refinery,self.crystal_refinery,self.eonium_refinery,)
        reply+= " ResLab: %s (%s%%), FC: %s, Sec: %s (%s%%)" % (self.research_lab,int(float(self.research_lab)/self.total*100),self.finance_centre,self.security_centre,int(float(self.security_centre)/self.total*100),)
        return reply
Scan.devscan = relation(DevScan, uselist=False, backref="scan")

class UnitScan(Base):
    __tablename__ = 'unitscan'
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey(Scan.id, ondelete='cascade'))
    ship_id = Column(Integer, ForeignKey(Ship.id, ondelete='cascade'))
    amount = Column(Integer)
    
    @property
    def visible(self):
        return self.amount if self.ship.type.lower() != "cloak" else 0
    
    def __str__(self):
        return "%s %s" % (self.ship.name, self.amount,)
Scan.units = relation(UnitScan, backref="scan", order_by=asc(UnitScan.ship_id))
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
    
    @property
    def eta(self):
        return self.landing_tick - self.scan.tick
    
    def __str__(self):
        p = self.owner
        return encode("(%s:%s:%s %s | %s %s %s)" % (p.x,p.y,p.z,self.fleet_name,self.fleet_size,self.mission,self.eta,))
        return "(%s:%s:%s %s | %s %s %s)" % (p.x,p.y,p.z,self.fleet_name,self.fleet_size,self.mission,self.eta,)
Scan.fleets = relation(FleetScan, backref="scan", order_by=asc(FleetScan.landing_tick))
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

# ########################################################################### #
# #########################    QUOTES AND SLOGANS    ######################## #
# ########################################################################### #

class Slogan(Base):
    __tablename__ = 'slogans'
    id = Column(Integer, primary_key=True)
    text = Column(String(512))
    @staticmethod
    def search(text):
        text = text or ""
        Q = session.query(Slogan)
        Q = Q.filter(Slogan.text.ilike("%"+text+"%")).order_by(random())
        return Q.first(), Q.count()
    def __str__(self):
        return encode(self.text)
        return self.text

class Quote(Base):
    __tablename__ = 'quotes'
    id = Column(Integer, primary_key=True)
    text = Column(String(512))
    @staticmethod
    def search(text):
        text = text or ""
        Q = session.query(Quote)
        Q = Q.filter(Quote.text.ilike("%"+text+"%")).order_by(random())
        return Q.first(), Q.count()
    def __str__(self):
        return encode(self.text)
        return self.text

# ########################################################################### #
# ##############################    DEFENCE    ############################## #
# ########################################################################### #

class UserFleet(Base):
    __tablename__ = 'user_fleet'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    ship_id = Column(Integer, ForeignKey(Ship.id, ondelete='cascade'))
    ship_count = Column(Integer)
User.fleets = dynamic_loader(UserFleet, backref="user")
UserFleet.ship = relation(Ship)

class FleetLog(Base):
    __tablename__ = 'fleet_log'
    id = Column(Integer, primary_key=True)
    taker_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    user_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    ship_id = Column(Integer, ForeignKey(Ship.id, ondelete='cascade'))
    ship_count = Column(Integer)
    tick = Column(Integer)
FleetLog.taker = relation(User, primaryjoin=FleetLog.taker_id==User.id)
User.fleetlogs = dynamic_loader(FleetLog, backref="user", primaryjoin=User.id==FleetLog.user_id, order_by=desc(FleetLog.id))
FleetLog.ship = relation(Ship)

# ########################################################################### #
# #########################    PROPS AND COOKIES    ######################### #
# ########################################################################### #

class Cookie(Base):
    __tablename__ = 'cookie_log'
    id = Column(Integer, primary_key=True)
    log_time = Column(DateTime, default=current_timestamp())
    year = Column(Integer)
    week = Column(Integer)
    howmany = Column(Integer)
    giver_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    receiver_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
User.cookies = dynamic_loader(Cookie, primaryjoin=User.id==Cookie.receiver_id, backref="receiver")
Cookie.giver = relation(User, primaryjoin=Cookie.giver_id==User.id)

class Invite(Base):
    __tablename__ = 'invite_proposal'
    id = Column(Integer, Sequence('proposal_id_seq'), primary_key=True, server_default=text("nextval('proposal_id_seq')"))
    active = Column(Boolean, default=True)
    proposer_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    person = Column(String(15))
    created = Column(DateTime, default=current_timestamp())
    closed = Column(DateTime)
    vote_result = Column(String(7))
    comment_text = Column(Text)
    type = "invite"
Invite.proposer = relation(User)

class Kick(Base):
    __tablename__ = 'kick_proposal'
    id = Column(Integer, Sequence('proposal_id_seq'), primary_key=True, server_default=text("nextval('proposal_id_seq')"))
    active = Column(Boolean, default=True)
    proposer_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    person_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    created = Column(DateTime, default=current_timestamp())
    closed = Column(DateTime)
    vote_result = Column(String(7))
    comment_text = Column(Text)
    type = "kick"
Kick.proposer = relation(User, primaryjoin=Kick.proposer_id==User.id)
Kick.kicked = relation(User, primaryjoin=Kick.person_id==User.id)
Kick.person = association_proxy("kicked", "name")

class Suggestion(Base):
    __tablename__ = 'suggestion_proposal'
    id = Column(Integer, Sequence('proposal_id_seq'), primary_key=True, server_default=text("nextval('proposal_id_seq')"))
    active = Column(Boolean, default=True)
    proposer_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    created = Column(DateTime, default=current_timestamp())
    closed = Column(DateTime)
    vote_result = Column(String(7))
    comment_text = Column(Text)
    type = "suggestion"
Suggestion.proposer = relation(User)

class Vote(Base):
    __tablename__ = 'prop_vote'
    id = Column(Integer, primary_key=True)
    vote = Column(String(7))
    carebears = Column(Integer)
    prop_id = Column(Integer)
    voter_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
User.votes = dynamic_loader(Vote, backref="voter")
Invite.votes = dynamic_loader(Vote, foreign_keys=(Vote.prop_id,), primaryjoin=Invite.id==Vote.prop_id)
Kick.votes = dynamic_loader(Vote, foreign_keys=(Vote.prop_id,), primaryjoin=Kick.id==Vote.prop_id)
Suggestion.votes = dynamic_loader(Vote, foreign_keys=(Vote.prop_id,), primaryjoin=Suggestion.id==Vote.prop_id)

# ########################################################################### #
# ################################    LOGS    ############################### #
# ########################################################################### #

class Command(Base):
    __tablename__ = 'command_log'
    id = Column(Integer, primary_key=True)
    command_prefix = Column(String(1))
    command = Column(String(20))
    subcommand = Column(String(20))
    command_parameters = Column(String(512))
    nick = Column(String(15))
    username = Column(String(15))
    hostname = Column(String(100))
    target = Column(String(150))
    command_time = Column(DateTime, default=current_timestamp())

class PageView(Base):
    __tablename__ = 'arthur_log'
    id = Column(Integer, primary_key=True)
    page = Column(String(20))
    full_request = Column(String(512))
    username = Column(String(15))
    session = Column(String(32))
    planet_id = Column(Integer)
    hostname = Column(String(100))
    request_time = Column(DateTime, default=current_timestamp())

class SMS(Base):
    __tablename__ = 'sms_log'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    receiver_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
    phone = Column(String(48))
    sms_text = Column(String(160))
    mode = Column(String(12))
SMS.sender = relation(User, primaryjoin=SMS.sender_id==User.id)
SMS.receiver = relation(User, primaryjoin=SMS.receiver_id==User.id)
