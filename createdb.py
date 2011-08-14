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
 
import sys
import sqlalchemy
from sqlalchemy.exc import DBAPIError, IntegrityError, ProgrammingError
from sqlalchemy.sql import text, bindparam
from Core.config import Config
from Core.db import Base, session
import shipstats

if len(sys.argv) > 2 and sys.argv[1] == "--migrate":
    round = sys.argv[2]
    if round.isdigit():
        round = "r"+round
elif len(sys.argv) > 1 and sys.argv[1] == "--new":
    round = None
else:
    print "To setup a database for a new Merlin install: createdb.py --new"
    print "To migrate without saving previoud round data: createdb.py --migrate temp"
    print "To migrate from an old round use: createdb.py --migrate <previous_round>"
    sys.exit()

if round:
    print "Moving tables to '%s' schema"%(round,)
    try:
        session.execute(text("ALTER SCHEMA public RENAME TO %s;" % (round,)))
    except ProgrammingError:
        print "Oops! Either you don't have permission to modify schemas or you already have a backup called '%s'" % (round,)
        session.rollback()
        sys.exit()
    else:
        session.commit()
    finally:
        session.close()

print "Importing database models"
from Core.maps import Channel

print "Creating schema and tables"
try:
    session.execute(text("CREATE SCHEMA public;"))
except ProgrammingError:
    print "A public schema already exists, but this is completely normal"
    session.rollback()
else:
    session.commit()
finally:
    session.close()

Base.metadata.create_all()

print "Setting up default channels"
userlevel = Config.get("Access", "member")
maxlevel = Config.get("Access", "admin")
gallevel = Config.get("Access", "galmate")
for chan, name in Config.items("Channels"):
    try:
        channel = Channel(name=name)
        if chan != "public":
            channel.userlevel = userlevel
            channel.maxlevel = maxlevel
        else:
            channel.userlevel = gallevel
            channel.maxlevel = gallevel
        session.add(channel)
        session.flush()
    except IntegrityError:
        print "Channel '%s' already exists" % (channel.name,)
        session.rollback()
    else:
        print "Created '%s' with access (%s|%s)" % (channel.name, channel.userlevel, channel.maxlevel,)
        session.commit()
session.close()

if round:
    print "Migrating data:"
    try:
        print "  - users/friends"
        session.execute(text("INSERT INTO users (id, name, alias, passwd, active, access, url, email, phone, pubphone, _smsmode, sponsor, quits, available_cookies, carebears, last_cookie_date, fleetcount) SELECT id, name, alias, passwd, active, access, url, email, phone, pubphone, _smsmode::varchar::smsmode, sponsor, quits, available_cookies, carebears, last_cookie_date, 0 FROM %s.users;" % (round,)))
        session.execute(text("SELECT setval('users_id_seq',(SELECT max(id) FROM users));"))
        session.execute(text("INSERT INTO phonefriends (user_id, friend_id) SELECT user_id, friend_id FROM %s.phonefriends;" % (round,)))
        print "  - slogans/quotes"
        session.execute(text("INSERT INTO slogans (text) SELECT text FROM %s.slogans;" % (round,)))
        session.execute(text("INSERT INTO quotes (text) SELECT text FROM %s.quotes;" % (round,)))
        print "  - props/votes/cookies"
        session.execute(text("INSERT INTO invite_proposal (id,active,proposer_id,person,created,closed,vote_result,comment_text) SELECT id,active,proposer_id,person,created,closed,vote_result,comment_text FROM %s.invite_proposal;" % (round,)))
        session.execute(text("INSERT INTO kick_proposal (id,active,proposer_id,person_id,created,closed,vote_result,comment_text) SELECT id,active,proposer_id,person_id,created,closed,vote_result,comment_text FROM %s.kick_proposal;" % (round,)))
        session.execute(text("SELECT setval('proposal_id_seq',(SELECT max(id) FROM (SELECT id FROM invite_proposal UNION SELECT id FROM kick_proposal) AS proposals));"))
        session.execute(text("INSERT INTO prop_vote (vote,carebears,prop_id,voter_id) SELECT vote,carebears,prop_id,voter_id FROM %s.prop_vote;" % (round,)))
        session.execute(text("INSERT INTO cookie_log (log_time,year,week,howmany,giver_id,receiver_id) SELECT log_time,year,week,howmany,giver_id,receiver_id FROM %s.cookie_log;" % (round,)))
        print "  - smslog"
        session.execute(text("INSERT INTO sms_log (sender_id,receiver_id,phone,sms_text,mode) SELECT sender_id,receiver_id,phone,sms_text,mode FROM %s.sms_log;" % (round,)))
    except DBAPIError, e:
        print "An error occurred during migration: %s" %(str(e),)
        session.rollback()
        print "Reverting to previous schema"
        session.execute(text("DROP SCHEMA public CASCADE;"))
        session.execute(text("ALTER SCHEMA %s RENAME TO public;" % (round,)))
        session.commit()
        sys.exit()
    else:
        session.commit()
    finally:
        session.close()

if round == "temp":
    print "Deleting temporary schema"
    session.execute(text("DROP SCHEMA temp CASCADE;"))
    session.commit()
    session.close()

print "Inserting ship stats"
shipstats.main()
