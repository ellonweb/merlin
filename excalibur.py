#!/usr/local/bin/python

import re, sys, time, traceback, urllib2
from variables import urlPlanet, urlGalaxy, urlAlliance
import Core.db as DB
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import text, bindparam

planet_new_id_search = Table('planet_new_id_search', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('x', Integer, primary_key=True),
    Column('y', Integer, primary_key=True),
    Column('z', Integer, primary_key=True),
    Column('race', String(3)),
    Column('size', Integer),
    Column('score', Integer),
    Column('value', Integer),
    Column('xp', Integer))
planet_old_id_search = Table('planet_old_id_search', DB.Maps.Base.metadata,
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
planet_size_rank = Table('planet_size_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('size', Integer),
    Column('size_rank', Integer, primary_key=True))
planet_score_rank = Table('planet_score_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('score', Integer),
    Column('score_rank', Integer, primary_key=True))
planet_value_rank = Table('planet_value_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('value', Integer),
    Column('value_rank', Integer, primary_key=True))
planet_xp_rank = Table('planet_xp_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('xp', Integer),
    Column('xp_rank', Integer, primary_key=True))
galaxy_size_rank = Table('galaxy_size_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('size', Integer),
    Column('size_rank', Integer, primary_key=True))
galaxy_score_rank = Table('galaxy_score_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('score', Integer),
    Column('score_rank', Integer, primary_key=True))
galaxy_value_rank = Table('galaxy_value_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('value', Integer),
    Column('value_rank', Integer, primary_key=True))
galaxy_xp_rank = Table('galaxy_xp_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('xp', Integer),
    Column('xp_rank', Integer, primary_key=True))
alliance_size_rank = Table('alliance_size_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('size', Integer),
    Column('size_rank', Integer, primary_key=True))
alliance_members_rank = Table('alliance_members_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('members', Integer),
    Column('members_rank', Integer, primary_key=True))
alliance_size_avg_rank = Table('alliance_size_avg_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('size_avg', Integer),
    Column('size_avg_rank', Integer, primary_key=True))
alliance_score_avg_rank = Table('alliance_score_avg_rank', DB.Maps.Base.metadata,
    Column('id', Integer),
    Column('score_avg', Integer),
    Column('score_avg_rank', Integer, primary_key=True))


planet_new_id_search.drop(checkfirst=True)
planet_old_id_search.drop(checkfirst=True)
planet_size_rank.drop(checkfirst=True)
planet_score_rank.drop(checkfirst=True)
planet_value_rank.drop(checkfirst=True)
planet_xp_rank.drop(checkfirst=True)
galaxy_size_rank.drop(checkfirst=True)
galaxy_score_rank.drop(checkfirst=True)
galaxy_value_rank.drop(checkfirst=True)
galaxy_xp_rank.drop(checkfirst=True)
alliance_size_rank.drop(checkfirst=True)
alliance_members_rank.drop(checkfirst=True)
alliance_size_avg_rank.drop(checkfirst=True)
alliance_score_avg_rank.drop(checkfirst=True)
planet_new_id_search.create()
planet_old_id_search.create()
planet_size_rank.create()
planet_score_rank.create()
planet_value_rank.create()
planet_xp_rank.create()
galaxy_size_rank.create()
galaxy_score_rank.create()
galaxy_value_rank.create()
galaxy_xp_rank.create()
alliance_size_rank.create()
alliance_members_rank.create()
alliance_size_avg_rank.create()
alliance_score_avg_rank.create()

last_tick = DB.Maps.Updates.current_tick()

session = DB.Session()

t_start=time.time()
t1=t_start

while True:
    try:

        try:
            planets = urllib2.urlopen(urlPlanet)
            galaxies = urllib2.urlopen(urlGalaxy)
            alliances = urllib2.urlopen(urlAlliance)
        except Exception, e:
            print "Failed gathering dump files."
            print e.__str__()
            time.sleep(300)
            continue

        planets.readline();planets.readline();planets.readline();
        tick=planets.readline()
        m=re.search(r"tick:\s+(\d+)",tick,re.I)
        if not m:
            print "Invalid tick: '%s'" % (tick,)
            time.sleep(120)
            continue
        planet_tick=int(m.group(1))
        print "Planet dump for tick %s" % (planet_tick,)
        planets.readline();planets.readline();planets.readline();

        galaxies.readline();galaxies.readline();galaxies.readline();
        tick=galaxies.readline()
        m=re.search(r"tick:\s+(\d+)",tick,re.I)
        if not m:
            print "Invalid tick: '%s'" % (tick,)
            time.sleep(120)
            continue
        galaxy_tick=int(m.group(1))
        print "Galaxy dump for tick %s" % (galaxy_tick,)
        galaxies.readline();galaxies.readline();galaxies.readline();

        alliances.readline();alliances.readline();alliances.readline();
        ptick=alliances.readline()
        m=re.search(r"tick:\s+(\d+)",tick,re.I)
        if not m:
            print "Invalid tick: '%s'" % (tick,)
            time.sleep(120)
            continue
        alliance_tick=int(m.group(1))
        print "Alliance dump for tick %s" % (alliance_tick,)
        alliances.readline();alliances.readline();alliances.readline();

        if not (planet_tick == galaxy_tick  == alliance_tick):
            print "Varying ticks found, sleeping"
            print "Planet: %s, Galaxy: %s, Alliance: %s" % (planet_tick,galaxy_tick,alliance_tick)
            time.sleep(30)
            continue
        if not planet_tick > last_tick:
            print "Stale ticks found, sleeping"            
            time.sleep(60)
            continue

        t2=time.time()-t1
        print "Loaded dumps from webserver in %.3f seconds" % (t2,)
        t1=time.time()

        session.execute(DB.Maps.Planet.__table__.delete())
        session.execute(DB.Maps.Galaxy.__table__.delete())
        session.execute(DB.Maps.Alliance.__table__.delete())

        planet_insert = "INSERT INTO planet (x, y, z, planetname, rulername, race, size, score, value, xp) "
        galaxy_insert = "INSERT INTO galaxy (x, y, name, size, score, value, xp) "
        alliance_insert = "INSERT INTO alliance (score_rank, name, size, members, score, size_avg, score_avg) "

        p_list = []
        g_list = []
        a_list = []

        for line in planets:
            p=line.strip().split("\t")
            p_list.append("SELECT %s, %s, %s, '%s', '%s', '%s', %s, %s, %s, %s" % (p[0], p[1], p[2], p[3].strip("\""), p[4].strip("\""), p[5], p[6], p[7], p[8], p[9],))
        planet_insert = unicode(''.join((planet_insert, ' UNION ALL '.join(p_list),";",)), encoding='latin-1')

        for line in galaxies:
            g=line.strip().split("\t")
            g_list.append("SELECT %s, %s, '%s', %s, %s, %s, %s" % (g[0], g[1], g[2].strip("\""), g[3], g[4], g[5], g[6],))
        galaxy_insert = unicode(''.join((galaxy_insert, ' UNION ALL '.join(g_list),";",)), encoding='latin-1')

        for line in alliances:
            a=line.strip().split("\t")
            a_list.append("SELECT %s, '%s', %s, %s, %s, %s, %s" % (a[0], a[1].strip("\""), a[2], a[3], a[4], int(a[2])/int(a[3]), int(a[4])/int(a[3]),))
        alliance_insert = unicode(''.join((alliance_insert, ' UNION ALL '.join(a_list),";",)), encoding='latin-1')

        session.execute(text(planet_insert))
        session.execute(text(galaxy_insert))
        session.execute(text(alliance_insert))

        t2=time.time()-t1
        print "Inserted dumps in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##############################    PLANETS    ############################## #
# ########################################################################### #

        session.execute(text("UPDATE planet SET id = (SELECT id FROM planet_history WHERE planet.rulername = planet_history.rulername AND planet.planetname = planet_history.planetname AND planet_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))

        t2=time.time()-t1
        print "Copy planet ids from history in %.3f seconds" % (t2,)
        t1=time.time()

        while last_tick > 0:
            def load_planet_id_search():
                session.execute(planet_new_id_search.delete())
                session.execute(planet_old_id_search.delete())
                if session.execute(text("INSERT INTO planet_new_id_search (id, x, y, z, race, size, score, value, xp) SELECT id, x, y, z, race, size, score, value, xp FROM planet WHERE planet.id IS NULL;")).rowcount < 1:
                    return None
                if session.execute(text("INSERT INTO planet_old_id_search (id, x, y, z, race, size, score, value, xp, vdiff) SELECT id, x, y, z, race, size, score, value, xp, vdiff FROM planet_history WHERE tick = :tick AND planet_history.id NOT IN (SELECT id FROM planet WHERE id IS NOT NULL);", bindparams=[bindparam("tick",last_tick)])).rowcount < 1:
                    return None
                session.execute(text("UPDATE planet SET id = (SELECT id FROM planet_new_id_search WHERE planet.x = planet_new_id_search.x AND planet.y = planet_new_id_search.y AND planet.z = planet_new_id_search.z) WHERE id IS NULL;"))
                return 1
            if load_planet_id_search() is None: break
            session.execute(text("""UPDATE planet_new_id_search SET id = (
                                      SELECT id FROM planet_old_id_search WHERE
                                        planet_old_id_search.x = planet_new_id_search.x AND
                                        planet_old_id_search.y = planet_new_id_search.y AND
                                        planet_old_id_search.z = planet_new_id_search.z AND
                                        planet_old_id_search.race = planet_new_id_search.race AND
                                        planet_old_id_search.size > 500 AND
                                        planet_old_id_search.size = planet_new_id_search.size
                                      );"""))
            if load_planet_id_search() is None: break
            session.execute(text("""UPDATE planet_new_id_search SET id = (
                                      SELECT id FROM planet_old_id_search WHERE
                                        planet_old_id_search.x = planet_new_id_search.x AND
                                        planet_old_id_search.y = planet_new_id_search.y AND
                                        planet_old_id_search.z = planet_new_id_search.z AND
                                        planet_old_id_search.race = planet_new_id_search.race AND
                                        planet_old_id_search.value > 500000 AND
                                        planet_new_id_search.value BETWEEN planet_old_id_search.value - (2* planet_old_id_search.vdiff) AND planet_old_id_search.value + (2* planet_old_id_search.vdiff)
                                      );"""))
            if load_planet_id_search() is None: break
            session.execute(text("""UPDATE planet_new_id_search SET id = (
                                      SELECT id FROM planet_old_id_search WHERE
                                        planet_old_id_search.race = planet_new_id_search.race AND
                                        planet_old_id_search.size > 500 AND
                                        planet_old_id_search.size = planet_new_id_search.size AND
                                        planet_old_id_search.value > 500000 AND
                                        planet_new_id_search.value BETWEEN planet_old_id_search.value - (2* planet_old_id_search.vdiff) AND planet_old_id_search.value + (2* planet_old_id_search.vdiff)
                                      );"""))
            break

        t2=time.time()-t1
        print "Lost planet ids match up in %.3f seconds" % (t2,)
        t1=time.time()

        session.execute(text("INSERT INTO planet_ref (rulername, planetname) SELECT rulername, planetname FROM planet WHERE id IS NULL;"))
        session.execute(text("UPDATE planet SET id = (SELECT id FROM planet_ref WHERE planet.rulername = planet_ref.rulername AND planet.planetname = planet_ref.planetname ORDER BY planet_ref.id DESC) WHERE id IS NULL;"))

        t2=time.time()-t1
        print "Generate new planet ids in %.3f seconds" % (t2,)
        t1=time.time()

        session.execute(text("INSERT INTO planet_size_rank (id, size) SELECT id, size FROM planet ORDER BY size DESC;"))
        session.execute(text("INSERT INTO planet_score_rank (id, score) SELECT id, score FROM planet ORDER BY score DESC;"))
        session.execute(text("INSERT INTO planet_value_rank (id, value) SELECT id, value FROM planet ORDER BY value DESC;"))
        session.execute(text("INSERT INTO planet_xp_rank (id, xp) SELECT id, xp FROM planet ORDER BY xp DESC;"))
        session.execute(text("""UPDATE planet SET
                                    size_rank = (SELECT size_rank FROM planet_size_rank WHERE planet.id = planet_size_rank.id),
                                    score_rank = (SELECT score_rank FROM planet_score_rank WHERE planet.id = planet_score_rank.id),
                                    value_rank = (SELECT value_rank FROM planet_value_rank WHERE planet.id = planet_value_rank.id),
                                    xp_rank = (SELECT xp_rank FROM planet_xp_rank WHERE planet.id = planet_xp_rank.id)
                            """))
        session.execute(text("UPDATE planet SET vdiff = planet.value - (SELECT value FROM planet_history WHERE planet.id = planet_history.id AND planet_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))
        session.execute(text("UPDATE planet SET idle = COALESCE(1 + (SELECT idle FROM planet_history WHERE planet.id = planet_history.id AND planet_history.tick = :tick AND planet.vdiff BETWEEN planet_history.vdiff -1 AND planet_history.vdiff +1 AND planet.xp - planet_history.xp = 0), 1);", bindparams=[bindparam("tick",last_tick)]))

        t2=time.time()-t1
        print "Planet ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##############################    GALAXIES    ############################# #
# ########################################################################### #

        session.execute(text("UPDATE galaxy SET id = (SELECT id FROM galaxy_history WHERE galaxy.x = galaxy_history.x AND galaxy.y = galaxy_history.y AND galaxy_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))

        t2=time.time()-t1
        print "Copy galaxy ids from history in %.3f seconds" % (t2,)
        t1=time.time()

        session.execute(text("INSERT INTO galaxy_ref (x, y) SELECT x, y FROM galaxy WHERE id IS NULL;"))
        session.execute(text("UPDATE galaxy SET id = (SELECT id FROM galaxy_ref WHERE galaxy.x = galaxy_ref.x AND galaxy.y = galaxy_ref.y ORDER BY galaxy_ref.id DESC) WHERE id IS NULL;"))

        t2=time.time()-t1
        print "Generate new galaxy ids in %.3f seconds" % (t2,)
        t1=time.time()

        session.execute(text("INSERT INTO galaxy_size_rank (id, size) SELECT id, size FROM galaxy ORDER BY size DESC;"))
        session.execute(text("INSERT INTO galaxy_score_rank (id, score) SELECT id, score FROM galaxy ORDER BY score DESC;"))
        session.execute(text("INSERT INTO galaxy_value_rank (id, value) SELECT id, value FROM galaxy ORDER BY value DESC;"))
        session.execute(text("INSERT INTO galaxy_xp_rank (id, xp) SELECT id, xp FROM galaxy ORDER BY xp DESC;"))
        session.execute(text("""UPDATE galaxy SET
                                    size_rank = (SELECT size_rank FROM galaxy_size_rank WHERE galaxy.id = galaxy_size_rank.id),
                                    score_rank = (SELECT score_rank FROM galaxy_score_rank WHERE galaxy.id = galaxy_score_rank.id),
                                    value_rank = (SELECT value_rank FROM galaxy_value_rank WHERE galaxy.id = galaxy_value_rank.id),
                                    xp_rank = (SELECT xp_rank FROM galaxy_xp_rank WHERE galaxy.id = galaxy_xp_rank.id)
                            """))

        t2=time.time()-t1
        print "Galaxy ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# #############################    ALLIANCES    ############################# #
# ########################################################################### #

        session.execute(text("UPDATE alliance SET id = (SELECT id FROM alliance_history WHERE alliance.name = alliance_history.name AND alliance_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))

        t2=time.time()-t1
        print "Copy alliance ids from history in %.3f seconds" % (t2,)
        t1=time.time()

        session.execute(text("INSERT INTO alliance_ref (name) SELECT name FROM alliance WHERE id IS NULL;"))
        session.execute(text("UPDATE alliance SET id = (SELECT id FROM alliance_ref WHERE alliance.name = alliance_ref.name ORDER BY alliance_ref.id DESC) WHERE id IS NULL;"))

        t2=time.time()-t1
        print "Generate new alliance ids in %.3f seconds" % (t2,)
        t1=time.time()

        session.execute(text("INSERT INTO alliance_size_rank (id, size) SELECT id, size FROM alliance ORDER BY size DESC;"))
        session.execute(text("INSERT INTO alliance_members_rank (id, members) SELECT id, members FROM alliance ORDER BY members DESC;"))
        session.execute(text("INSERT INTO alliance_size_avg_rank (id, size_avg) SELECT id, size_avg FROM alliance ORDER BY size_avg DESC;"))
        session.execute(text("INSERT INTO alliance_score_avg_rank (id, score_avg) SELECT id, score_avg FROM alliance ORDER BY score_avg DESC;"))
        session.execute(text("""UPDATE alliance SET
                                    size_rank = (SELECT size_rank FROM alliance_size_rank WHERE alliance.id = alliance_size_rank.id),
                                    members_rank = (SELECT members_rank FROM alliance_members_rank WHERE alliance.id = alliance_members_rank.id),
                                    size_avg_rank = (SELECT size_avg_rank FROM alliance_size_avg_rank WHERE alliance.id = alliance_size_avg_rank.id),
                                    score_avg_rank = (SELECT score_avg_rank FROM alliance_score_avg_rank WHERE alliance.id = alliance_score_avg_rank.id)
                            """))

        t2=time.time()-t1
        print "Alliance ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##################   HISTORY: EVERYTHING BECOMES FINAL   ################## #
# ########################################################################### #

        # planet_tick = last_tick + 1
        session.execute(text("INSERT INTO planet_exiles (tick, id, oldx, oldy, oldz, newx, newy, newz) SELECT :tick, planet.id, planet_history.x, planet_history.y, planet_history.z, planet.x, planet.y, planet.z FROM planet, planet_history WHERE planet.id = planet_history.id AND planet_history.tick = :oldtick AND (planet.x != planet_history.x OR planet.y != planet_history.y OR planet.z != planet_history.z);", bindparams=[bindparam("tick",planet_tick), bindparam("oldtick",last_tick)]))
        session.execute(text("INSERT INTO planet_history (tick, id, x, y, z, planetname, rulername, race, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank, idle, vdiff) SELECT :tick, id, x, y, z, planetname, rulername, race, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank, idle, vdiff FROM planet ORDER BY id ASC;", bindparams=[bindparam("tick",planet_tick)]))
        session.execute(text("INSERT INTO galaxy_history (tick, id, x, y, name, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank) SELECT :tick, id, x, y, name, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank FROM galaxy ORDER BY id ASC;", bindparams=[bindparam("tick",planet_tick)]))
        session.execute(text("INSERT INTO alliance_history (tick, id, name, size, members, score, size_avg, score_avg, size_rank, members_rank, score_rank, size_avg_rank, score_avg_rank) SELECT :tick, id, name, size, members, score, size_avg, score_avg, size_rank, members_rank, score_rank, size_avg_rank, score_avg_rank FROM alliance ORDER BY id ASC;", bindparams=[bindparam("tick",planet_tick)]))
        session.execute(DB.Maps.Updates.__table__.insert().values(tick=planet_tick, planets=DB.Maps.Planet.__table__.count(), galaxies=DB.Maps.Galaxy.__table__.count(), alliances=DB.Maps.Alliance.__table__.count()))
        session.commit()
        session.close()

        t2=time.time()-t1
        print "History and final update in %.3f seconds" % (t2,)
        t1=time.time()

        break
    except Exception, e:
        print "Something random went wrong, sleeping for 15 seconds to hope it improves"
        print e.__str__()
        traceback.print_exc()
        session.rollback()
        time.sleep(15)
        continue

t1=time.time()-t_start
print "Total time taken: %.3f seconds" % (t1,)
planet_new_id_search.drop()
planet_old_id_search.drop()
planet_size_rank.drop()
planet_score_rank.drop()
planet_value_rank.drop()
planet_xp_rank.drop()
galaxy_size_rank.drop()
galaxy_score_rank.drop()
galaxy_value_rank.drop()
galaxy_xp_rank.drop()
alliance_size_rank.drop()
alliance_members_rank.drop()
alliance_size_avg_rank.drop()
alliance_score_avg_rank.drop()

last_tick = DB.Maps.Updates.current_tick()
history_tick = max(last_tick-72, 1)
session = DB.Session()
t_start=time.time()
t1=t_start
session.execute(DB.Maps.epenis.__table__.delete())
session.execute(text("INSERT INTO epenis (user_id, penis) SELECT users.id, planet.score - planet_history.score FROM users, planet, planet_history WHERE users.planet_id = planet.id AND planet.id = planet_history.id AND planet_history.tick = :tick ORDER BY planet.score - planet_history.score DESC;", bindparams=[bindparam("tick",history_tick)]))
t2=time.time()-t1
print "epenis in %.3f seconds" % (t2,)
t1=time.time()
session.execute(DB.Maps.galpenis.__table__.delete())
session.execute(text("INSERT INTO galpenis (galaxy_id, penis) SELECT galaxy.id, galaxy.score - galaxy_history.score FROM galaxy, galaxy_history WHERE galaxy.id = galaxy_history.id AND galaxy_history.tick = :tick ORDER BY galaxy.score - galaxy_history.score DESC;", bindparams=[bindparam("tick",history_tick)]))
t2=time.time()-t1
print "galpenis in %.3f seconds" % (t2,)
t1=time.time()
session.execute(DB.Maps.apenis.__table__.delete())
session.execute(text("INSERT INTO apenis (alliance_id, penis) SELECT alliance.id, alliance.score - alliance_history.score FROM alliance, alliance_history WHERE alliance.id = alliance_history.id AND alliance_history.tick = :tick ORDER BY alliance.score - alliance_history.score DESC;", bindparams=[bindparam("tick",history_tick)]))
t2=time.time()-t1
print "galpenis in %.3f seconds" % (t2,)
session.commit()
session.close()
t1=time.time()-t_start
print "Total penis time: %.3f seconds" % (t1,)
