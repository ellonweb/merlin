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
from math import ceil
from time import time
import hashlib
from .variables import access

Base = declarative_base()

# This PhoneFriend table is a slightly hackish solution (as is the relation defined in User), but it works.
# Many2Many relations do not work with declarative, so it has to be defined just as the table.
# However, string alternatives for column attributes only work when using declarative.
# The former problem is unlikely to be fixed (requires some major changes in design), the latter is more likely:
# [03:25] <zzzeek__> its a straightforward feature add to have the table name work within the string version
# Keep an eye on CHANGES to see if this is ever implemented.
# There is another option, which I haven't looked into yet:
# [03:24] <zzzeek__> its not documented but you could set primaryjoin to be a callable which returns the correct result
PhoneFriend = Table('phonefriends', Base.metadata, 
	Column('user_id', Integer, ForeignKey("users.id", ondelete='cascade')),
	Column('friend_id', Integer, ForeignKey("users.id", ondelete='cascade'))
)
class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True)
	name = Column(String) # pnick
	passwd = Column(String)
	active = Column(Boolean, default=True)
	access = Column(Integer)
	#planet_id - reference to planet_canon - on delete cascade
	email = Column(String)
	phone = Column(String)
	pubphone = Column(Boolean, default=False) # Asc
	phonefriends = relation("User", secondary=PhoneFriend, primaryjoin=PhoneFriend.c.user_id==id,
									secondaryjoin=PhoneFriend.c.friend_id==id) # Asc
	sponsor = Column(String) # Asc
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
	


class Gimp(Base):
	__tablename__ = 'sponsor'
	
	id = Column(Integer, primary_key=True)
	sponsor_id = Column(Integer, ForeignKey(User.id, ondelete='cascade'))
	sponsor = relation(User, primaryjoin=sponsor_id==User.id, backref=backref('gimps', order_by=id))
	name = Column(String)
	comment = Column(Text)
	timestamp = Column(Float)
	wait = 36 #hours. use 0 for invite mode, -1 for recruitment closed
	
	def __init__(self, sponsor, name, comment):
		self.sponsor_id = sponsor.id
		self.name = name
		self.comment = comment
		self.timestamp = time()
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
	


class Ship(Base):
	__tablename__ = 'ships'
	
	id = Column(Integer, primary_key=True)
	name = Column(String)
	class_ = Column(String)
	t1 = Column(String)
	t2 = Column(String)
	t3 = Column(String)
	type = Column(String)
	init = Column(Integer)
	guns = Column(Integer)
	armor = Column(Integer)
	damage = Column(Integer)
	empres = Column(Integer)
	metal = Column(Integer)
	crystal = Column(Integer)
	eonium = Column(Integer)
	total_cost = Column(Integer)
	race = Column(String)
	
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
