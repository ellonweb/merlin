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

import psycopg2
if not 2.1 <= float(psycopg2.__version__[2:6]):
    sys.exit("psycopg2 2.2.1+ Required")
import sys
import sqlalchemy
if not 6.3 <= float(sqlalchemy.__version__[2:5]) < 7.0:
    sys.exit("SQLAlchemy 0.6.3+ Required")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text, bindparam

from Core.config import Config
from Core.string import encoding

engine = create_engine(Config.get("DB", "URL"), convert_unicode=True, encoding=encoding)#, echo='debug')
if engine.name != "postgresql" or "PostgreSQL 8.4" not in engine.connect().execute(text("SELECT version();")).scalar():
    sys.exit("PostgreSQL 8.4+ Required.")

if encoding != engine.connect().execute(text("SHOW client_encoding;")).scalar().lower():
    sys.exit("Database client encoding needs to be %s." %(encoding,))

# Some constants
true = bindparam("true",True)
false = bindparam("false",False)

Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
