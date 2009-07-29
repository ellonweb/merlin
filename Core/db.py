# SQLAlchemy DB interface

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

import sys
import sqlalchemy
if not 5.4 <= float(sqlalchemy.__version__[2:5]) < 6.0:
    sys.exit("SQLAlchemy 0.5.4+ Required")
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
import sqlalchemy.sql as SQL
import sqlalchemy.sql.functions
SQL.f = sys.modules['sqlalchemy.sql.functions']
from .variables import DBeng

engine = create_engine(DBeng)#, echo='debug')
if engine.name != "postgres" or "PostgreSQL 8.4" not in engine.connect().execute(text("SELECT version();")).scalar():
    sys.exit("PostgreSQL 8.4+ Required.")

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

if __name__ == "__main__":
    import maps
    Base.metadata.create_all()
