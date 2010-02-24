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
 
# SQLAlchemy DB interface

import sys
import sqlalchemy
if not 5.7 <= float(sqlalchemy.__version__[2:5]) < 6.0:
    sys.exit("SQLAlchemy 0.5.7+ Required")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text, bindparam

from Core.config import Config

engine = create_engine(Config.get("DB", "URL"))#, echo='debug')
if engine.name != "postgres" or "PostgreSQL 8.4" not in engine.connect().execute(text("SELECT version();")).scalar():
    sys.exit("PostgreSQL 8.4+ Required.")

# Some constants
true = bindparam("true",True)
false = bindparam("false",False)

Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
