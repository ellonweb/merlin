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
 
import sys
import sqlalchemy

if len(sys.argv) > 2 and sys.argv[1] == "--migrate":
    round = sys.argv[2]
    if sqlalchemy.__version__ != "0.5.7":
        print "Migration requires SQLA 0.5.7 which isn't available yet."
        print "You can get the neccessary changes from ticket #1576 (see TODO) or downloading the trunk."
        print "Once you've done that, delete this code to proceed."
        sys.exit()
else:
    round = None
    print "To migrate from an old round use: createdb.py --migrate <previous_round>"

from sqlalchemy.sql import text, bindparam
from Core.db import session
if round:
    print "Moving tables to '%s' schema"%(round,)
    session.execute(text("ALTER SCHEMA public RENAME TO %s;" % (round,)))
    session.execute(text("CREATE SCHEMA public;"))
    session.commit()
    session.close()

from Core.db import Base
print "Importing database models"
from Core.maps import Channel

print "Creating tables"
Base.metadata.create_all()

print "Setting up default channels"
from Core.config import Config
for chan, name in Config.items("Channels"):
    session.add(Channel(name=name,userlevel=100,maxlevel=1000))
session.commit()
session.close()

if round:
    print "Migrating users/friends"
    session.execute(text("INSERT INTO users (id, name, alias, passwd, active, access, email, phone, pubphone, sponsor, quits, available_cookies, carebears, last_cookie_date) SELECT id, name, alias, passwd, active, access, email, phone, pubphone, sponsor, quits, available_cookies, carebears, last_cookie_date FROM %s.users;" % (round,)))
    session.execute(text("SELECT setval('users_id_seq',(SELECT max(id) FROM users));"))
    session.execute(text("INSERT INTO phonefriends (user_id, friend_id) SELECT user_id, friend_id FROM %s.phonefriends;" % (round,)))
    print "Migrating slogans/quotes"
    session.execute(text("INSERT INTO slogans (text) SELECT text FROM %s.slogans;" % (round,)))
    session.execute(text("INSERT INTO quotes (text) SELECT text FROM %s.quotes;" % (round,)))
    print "Migrating props/votes/cookies"
    session.execute(text("INSERT INTO invite_proposal (id,active,proposer_id,person,created,closed,vote_result,comment_text) SELECT id,active,proposer_id,person,created,closed,vote_result,comment_text FROM %s.invite_proposal;" % (round,)))
    session.execute(text("INSERT INTO kick_proposal (id,active,proposer_id,person_id,created,closed,vote_result,comment_text) SELECT id,active,proposer_id,person_id,created,closed,vote_result,comment_text FROM %s.kick_proposal;" % (round,)))
    session.execute(text("SELECT setval('proposal_id_seq',(SELECT max(id) FROM (SELECT id FROM invite_proposal UNION SELECT id FROM kick_proposal) AS proposals));"))
    session.execute(text("INSERT INTO prop_vote (vote,carebears,prop_id,voter_id) SELECT vote,carebears,prop_id,voter_id FROM %s.prop_vote;" % (round,)))
    session.execute(text("INSERT INTO cookie_log (log_time,year,week,howmany,giver_id,receiver_id) SELECT log_time,year,week,howmany,giver_id,receiver_id FROM %s.cookie_log;" % (round,)))
    print "Migrating smslog"
    session.execute(text("INSERT INTO sms_log (sender_id,receiver_id,phone,sms_text) SELECT sender_id,receiver_id,phone,sms_text FROM %s.sms_log;" % (round,)))
    session.commit()
    session.close()

print "Inserting ship stats"
import shipstats
shipstats.main()
