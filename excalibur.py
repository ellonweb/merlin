#!/usr/local/bin/python

import re, urllib2, time, traceback
from variables import urlPlanet, urlGalaxy, urlAlliance
import Core.db as DB
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.sql import text, bindparam
from sqlalchemy.sql.functions import max

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

t_start=time.time()
t1=t_start

while True:
    try:
        last_tick = DB.Maps.Updates.current_tick()

        try:
            planets = urllib2.urlopen(urlPlanet)
        except Exception, e:
            print "Failed gathering planet listing."
            print e.__str__()
            time.sleep(300)
            continue
        try:
            galaxies = urllib2.urlopen(urlGalaxy)
        except Exception, e:
            print "Failed gathering galaxy listing."
            print e.__str__()
            time.sleep(300)
            continue    
        try:
            alliances = urllib2.urlopen(urlAlliance)
        except Exception, e:
            print "Failed gathering alliance listing."
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

        session = DB.Session()

        session.execute(DB.Maps.Planet.__table__.delete())
        for line in planets:
            p=line.strip().split("\t")
            session.execute(DB.Maps.Planet.__table__.insert().values(x=p[0],y=p[1],z=p[2],planetname=unicode(p[3].strip("\""),encoding='latin-1'),rulername=unicode(p[4].strip("\""),encoding='latin-1'),race=p[5],size=p[6],score=p[7],value=p[8],xp=p[9]))

        session.execute(DB.Maps.Galaxy.__table__.delete())
        for line in galaxies:
            g=line.strip().split("\t")
            session.execute(DB.Maps.Galaxy.__table__.insert().values(x=g[0],y=g[1],name=unicode(g[2].strip("\""),encoding='latin-1'),size=g[3],score=g[4],value=g[5],xp=g[6]))

        session.execute(DB.Maps.Alliance.__table__.delete())
        for line in alliances:
            a=line.strip().split("\t")
            session.execute(DB.Maps.Alliance.__table__.insert().values(score_rank=a[0],name=unicode(a[1].strip("\""),encoding='latin-1'),size=a[2],members=a[3],score=a[4],size_avg=int(a[2])/int(a[3]),score_avg=int(a[4])/int(a[3])))

        t2=time.time()-t1
        print "Inserted dumps in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##############################    PLANETS    ############################## #
# ########################################################################### #

        session.execute(text("UPDATE planet SET id = (SELECT id FROM planet_history WHERE planet.rulername = planet_history.rulername AND planet.planetname = planet_history.planetname AND planet_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))
        session.commit()

        t2=time.time()-t1
        print "Copy planet ids from history in %.3f seconds" % (t2,)
        t1=time.time()

        planet_new_id_search.drop(checkfirst=True)
        planet_old_id_search.drop(checkfirst=True)
        planet_new_id_search.create()
        planet_old_id_search.create()
        while True:
            if session.execute(DB.Maps.Updates.__table__.count()).scalar() < 1:
                break
            def load_planet_id_search():
                session.execute(planet_new_id_search.delete())
                session.execute(planet_old_id_search.delete())
                if session.execute(text("INSERT INTO planet_new_id_search (id, x, y, z, race, size, score, value, xp) SELECT id, x, y, z, race, size, score, value, xp FROM planet WHERE planet.id IS NULL;")).rowcount < 1:
                    return None
                if session.execute(text("INSERT INTO planet_old_id_search (id, x, y, z, race, size, score, value, xp, vdiff) SELECT id, x, y, z, race, size, score, value, xp, vdiff FROM planet_history WHERE tick = :tick AND planet_history.id NOT IN (SELECT id FROM planet WHERE id NOT NULL);", bindparams=[bindparam("tick",last_tick)])).rowcount < 1:
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
        session.commit()
        planet_new_id_search.drop()
        planet_old_id_search.drop()
        session.commit()

        t2=time.time()-t1
        print "Lost planet ids match up in %.3f seconds" % (t2,)
        t1=time.time()

        p_id = session.query(max(DB.Maps.PlanetHistory.id)).scalar() or 0
        for planet in session.query(DB.Maps.Planet).filter_by(id=None):
            p_id += 1
            planet.id = p_id
        session.commit()

        t2=time.time()-t1
        print "Generate new planet ids in %.3f seconds" % (t2,)
        t1=time.time()

        planet_size_rank.drop(checkfirst=True)
        planet_score_rank.drop(checkfirst=True)
        planet_value_rank.drop(checkfirst=True)
        planet_xp_rank.drop(checkfirst=True)
        planet_size_rank.create()
        planet_score_rank.create()
        planet_value_rank.create()
        planet_xp_rank.create()
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
        session.commit()
        planet_size_rank.drop()
        planet_score_rank.drop()
        planet_value_rank.drop()
        planet_xp_rank.drop()
        session.execute(text("UPDATE planet SET vdiff = planet.value - (SELECT value FROM planet_history WHERE planet.id = planet_history.id AND planet_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))
        session.execute(text("UPDATE planet SET idle = COALESCE(1 + (SELECT idle FROM planet_history WHERE planet.id = planet_history.id AND planet_history.tick = :tick AND planet.vdiff BETWEEN planet_history.vdiff -1 AND planet_history.vdiff +1 AND planet.xp - planet_history.xp = 0), 1);", bindparams=[bindparam("tick",last_tick)]))
        session.commit()

        t2=time.time()-t1
        print "Planet ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##############################    GALAXIES    ############################# #
# ########################################################################### #

        session.execute(text("UPDATE galaxy SET id = (SELECT id FROM galaxy_history WHERE galaxy.x = galaxy_history.x AND galaxy.y = galaxy_history.y AND galaxy_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))
        session.commit()

        t2=time.time()-t1
        print "Copy galaxy ids from history in %.3f seconds" % (t2,)
        t1=time.time()

        g_id = session.query(max(DB.Maps.GalaxyHistory.id)).scalar() or 0
        for galaxy in session.query(DB.Maps.Galaxy).filter_by(id=None):
            g_id += 1
            galaxy.id = g_id
        session.commit()

        t2=time.time()-t1
        print "Generate new galaxy ids in %.3f seconds" % (t2,)
        t1=time.time()

        galaxy_size_rank.drop(checkfirst=True)
        galaxy_score_rank.drop(checkfirst=True)
        galaxy_value_rank.drop(checkfirst=True)
        galaxy_xp_rank.drop(checkfirst=True)
        galaxy_size_rank.create()
        galaxy_score_rank.create()
        galaxy_value_rank.create()
        galaxy_xp_rank.create()
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
        session.commit()
        galaxy_size_rank.drop()
        galaxy_score_rank.drop()
        galaxy_value_rank.drop()
        galaxy_xp_rank.drop()
        session.commit()

        t2=time.time()-t1
        print "Galaxy ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# #############################    ALLIANCES    ############################# #
# ########################################################################### #

        session.execute(text("UPDATE alliance SET id = (SELECT id FROM alliance_history WHERE alliance.name = alliance_history.name AND alliance_history.tick = :tick);", bindparams=[bindparam("tick",last_tick)]))
        session.commit()

        t2=time.time()-t1
        print "Copy alliance ids from history in %.3f seconds" % (t2,)
        t1=time.time()

        a_id = session.query(max(DB.Maps.AllianceHistory.id)).scalar() or 0
        for alliance in session.query(DB.Maps.Alliance).filter_by(id=None):
            a_id += 1
            alliance.id = a_id
        session.commit()

        t2=time.time()-t1
        print "Generate new alliance ids in %.3f seconds" % (t2,)
        t1=time.time()

        alliance_size_rank.drop(checkfirst=True)
        alliance_members_rank.drop(checkfirst=True)
        alliance_size_avg_rank.drop(checkfirst=True)
        alliance_score_avg_rank.drop(checkfirst=True)
        alliance_size_rank.create()
        alliance_members_rank.create()
        alliance_size_avg_rank.create()
        alliance_score_avg_rank.create()
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
        session.commit()
        alliance_size_rank.drop()
        alliance_members_rank.drop()
        alliance_size_avg_rank.drop()
        alliance_score_avg_rank.drop()
        session.commit()

        t2=time.time()-t1
        print "Alliance ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##################   HISTORY: EVERYTHING BECOMES FINAL   ################## #
# ########################################################################### #

        # planet_tick = last_tick + 1
        session.execute(text("INSERT INTO planet_exiles (tick, id, oldx, oldy, oldz, newx, newy, newz) SELECT :tick, planet.id, planet_history.x, planet_history.y, planet_history.z, planet.x, planet.y, planet.z FROM planet, planet_history WHERE planet.id = planet_history.id AND (planet.x != planet_history.x OR planet.y != planet_history.y OR planet.z != planet_history.z);", bindparams=[bindparam("tick",planet_tick)]))
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
        time.sleep(15)
        continue

t1=time.time()-t_start
print "Total time taken: %.3f seconds" % (t1,)
