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

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relation, backref
from sqlalchemy.sql.functions import current_timestamp, max
from math import ceil
from time import time
import hashlib
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
	planet_id = Column(Integer, ForeignKey('planet.id', ondelete='set null'))
	email = Column(String(32))
	phone = Column(String(32))
	pubphone = Column(Boolean, default=False) # Asc
	sponsor = Column(String(15)) # Asc
	invites = Column(Integer) # Asc
	quits = Column(Integer) # Asc
	stay = Column(Boolean) # Asc
	
	@validates('passwd')
	def valid_passwd(self, key, passwd):
		return User.hasher(passwd)
	@validates('email')
	def valid_email(self, key, email):
		#assert some_regex match email
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
	def load(id=None, name=None, passwd=None, exact=True, active=True):
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
	timestamp = Column(DateTime, default=current_timestamp())
	@staticmethod
	def current_tick():
		session = Session()
		tick = session.query(max(Updates.tick)).scalar() or 0
		session.close()
		return tick
class Planet(Base):
	__tablename__ = 'planet'
	id = Column(Integer, index=True, unique=True)
	x = Column(Integer, primary_key=True)
	y = Column(Integer, primary_key=True)
	z = Column(Integer, primary_key=True)
	galaxy_coords = ForeignKeyConstraint(('planet.x', 'planet.y'), ('galaxy.x', 'galaxy.y'), deferrable=True)
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
User.planet = relation(Planet, primaryjoin=User.planet_id==Planet.id)
class PlanetHistory(Base):
	__tablename__ = 'planet_history'
	tick = Column(Integer, ForeignKey('updates.tick', deferrable=True, ondelete='cascade'), primary_key=True)
	id = Column(Integer, ForeignKey('planet.id', deferrable=True), primary_key=True)
	x = Column(Integer)
	y = Column(Integer)
	z = Column(Integer)
	galaxy_coords = ForeignKeyConstraint(('planet_history.tick', 'planet_history.x', 'planet_history.y'), ('galaxy_history.tick', 'galaxy_history.x', 'galaxy_history.y'), deferrable=True)
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
class PlanetExiles(Base):
	__tablename__ = 'planet_exiles'
	key = Column(Integer, primary_key=True)
	tick = Column(Integer, ForeignKey('updates.tick', deferrable=True, ondelete='cascade'))
	id = Column(Integer, ForeignKey('planet.id', deferrable=True))
	oldx = Column(Integer)
	oldy = Column(Integer)
	oldz = Column(Integer)
	newx = Column(Integer)
	newy = Column(Integer)
	newz = Column(Integer)
class Galaxy(Base):
	__tablename__ = 'galaxy'
	id = Column(Integer, index=True, unique=True)
	x = Column(Integer, primary_key=True)
	y = Column(Integer, primary_key=True)
	name = Column(String(64))
	size = Column(Integer)
	score = Column(Integer)
	value = Column(Integer)
	xp = Column(Integer)
	size_rank = Column(Integer)
	score_rank = Column(Integer)
	value_rank = Column(Integer)
	xp_rank = Column(Integer)
Planet.galaxy = relation(Galaxy, primaryjoin=and_(Galaxy.x==Planet.x, Galaxy.y==Planet.y), foreign_keys=(Planet.x, Planet.y), backref=backref('planets', primaryjoin=and_(Planet.x==Galaxy.x, Planet.y==Galaxy.y), foreign_keys=(Planet.x, Planet.y)))
class GalaxyHistory(Base):
	__tablename__ = 'galaxy_history'
	tick = Column(Integer, ForeignKey('updates.tick', deferrable=True, ondelete='cascade'), primary_key=True)
	id = Column(Integer, ForeignKey('galaxy.id', deferrable=True), primary_key=True)
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
PlanetHistory.galaxy = relation(GalaxyHistory, primaryjoin=and_(GalaxyHistory.tick==PlanetHistory.tick, GalaxyHistory.x==PlanetHistory.x, GalaxyHistory.y==PlanetHistory.y), foreign_keys=(PlanetHistory.tick, PlanetHistory.x, PlanetHistory.y), backref=backref('planets', primaryjoin=and_(PlanetHistory.tick==GalaxyHistory.tick, PlanetHistory.x==GalaxyHistory.x, PlanetHistory.y==GalaxyHistory.y), foreign_keys=(PlanetHistory.tick, PlanetHistory.x, PlanetHistory.y)))
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
class AllianceHistory(Base):
	__tablename__ = 'alliance_history'
	tick = Column(Integer, ForeignKey('updates.tick', deferrable=True, ondelete='cascade'), primary_key=True)
	id = Column(Integer, ForeignKey('alliance.id', deferrable=True), primary_key=True)
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
	def load(id=None, name=None):
		assert id or name
		session = Session()
		Q = session.query(Ship)
		if id is not None:
			Q = Q.filter(Ship.id == id)
		if name is not None:
			if Q.filter(Ship.name.ilike(name)).count() > 0:
				Q = Q.filter(Ship.name.ilike(name))
			elif Q.filter(Ship.name.ilike("%"+name+"%")) > 0 or (name[-1].lower()!="s"):
				Q = Q.filter(Ship.name.ilike("%"+name+"%"))
			else:
				Q = Q.filter(Ship.name.ilike("%"+name[:-1]+"%"))
		ship = Q.first()
		session.close()
		return ship
