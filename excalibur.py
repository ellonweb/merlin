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
 
import re, time, traceback, urllib2
from sqlalchemy.sql import text, bindparam
from Core.config import Config
from Core.paconf import PA
from Core.string import decode
from Core.db import true, false, session
from Core.maps import Updates, Galaxy, Planet, Alliance, epenis, galpenis, apenis
from Core.maps import galaxy_temp, planet_temp, alliance_temp, planet_new_id_search, planet_old_id_search

# Get the previous tick number!
last_tick = Updates.current_tick()
midnight = Updates.midnight_tick() == last_tick

t_start=time.time()
t1=t_start

while True:
    try:

        # How long has passed since starting?
        # If 55 mins, we're not likely getting dumps this tick, so quit
        if (time.time() - t_start) >= (55 * 60):
            print "55 minutes without a successful dump, giving up!"
            session.close()
            exit()

        # Open the dump files
        try:
            planets = urllib2.urlopen(Config.get("URL", "planets"))
            galaxies = urllib2.urlopen(Config.get("URL", "galaxies"))
            alliances = urllib2.urlopen(Config.get("URL", "alliances"))
        except Exception, e:
            print "Failed gathering dump files."
            print e.__str__()
            time.sleep(300)
            continue

        # Skip first three lines of the dump, tick info is on fourth line
        planets.readline();planets.readline();planets.readline();
        # Parse the fourth line and check we have a number
        tick=planets.readline()
        m=re.search(r"tick:\s+(\d+)",tick,re.I)
        if not m:
            print "Invalid tick: '%s'" % (tick,)
            time.sleep(120)
            continue
        planet_tick=int(m.group(1))
        print "Planet dump for tick %s" % (planet_tick,)
        # Skip next three lines; two are junk, next is blank, data starts next
        planets.readline();planets.readline();planets.readline();

        # As above
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

        # As above
        alliances.readline();alliances.readline();alliances.readline();
        tick=alliances.readline()
        m=re.search(r"tick:\s+(\d+)",tick,re.I)
        if not m:
            print "Invalid tick: '%s'" % (tick,)
            time.sleep(120)
            continue
        alliance_tick=int(m.group(1))
        print "Alliance dump for tick %s" % (alliance_tick,)
        alliances.readline();alliances.readline();alliances.readline();

        # Check the ticks of the dumps are all the same and that it's
        #  greater than the previous tick, i.e. a new tick
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

        # Empty out the temp tables
        session.execute(galaxy_temp.delete())
        session.execute(planet_temp.delete())
        session.execute(alliance_temp.delete())

        # If the new tick is below the shuffle tick, empty out all the data
        #  and don't store anything from the dumps other than the tick itself
        if planet_tick <= PA.getint("numbers", "shuffle"):
            print "Pre-shuffle dumps detected, emptying out the data"
            planets.readlines()
            galaxies.readlines()
            alliances.readlines()

        # Insert the data to the temporary tables, some DBMS do not support
        #  multiple row insert in the same statement so we have to do it one at
        #  a time which is a bit slow unfortunatly
        # Previously got around this with:
        #  INSERT INTO .. row UNION row UNION row...
        #  Some DBMS complained the resultant query was too long for the planet
        #  dumps, so back at one row per statement
        planet_insert = "INSERT INTO planet_temp (x, y, z, planetname, rulername, race, size, score, value, xp) "
        planet_insert+= "VALUES (%s, %s, %s, '%s', '%s', '%s', %s, %s, %s, %s);"
        for line in planets:
            p=decode(line).strip().split("\t")
            session.execute(text(planet_insert % (p[0], p[1], p[2], p[3].strip("\""), p[4].strip("\""), p[5], p[6], p[7], p[8], p[9],)))

        # As above
        galaxy_insert = "INSERT INTO galaxy_temp (x, y, name, size, score, value, xp) "
        galaxy_insert+= "VALUES (%s, %s, '%s', %s, %s, %s, %s);"
        for line in galaxies:
            g=decode(line).strip().split("\t")
            session.execute(text(galaxy_insert % (g[0], g[1], g[2].strip("\""), g[3], g[4], g[5], g[6],)))

        # As above
        alliance_insert = "INSERT INTO alliance_temp (score_rank, name, size, members, score, points, size_avg, score_avg, points_avg) "
        alliance_insert+= "VALUES (%s, '%s', %s, %s, %s, %s, %s, %s, %s);"
        for line in alliances:
            a=decode(line).strip().split("\t")
            session.execute(text(alliance_insert % (a[0], a[1].strip("\""), a[2], a[3], a[4], a[5], int(a[2])/int(a[3]), int(a[4])/min(PA.getint("numbers", "tag_count"),int(a[3])), int(a[5])/int(a[3]),)))

        t2=time.time()-t1
        print "Inserted dumps in %.3f seconds" % (t2,)
        t1=time.time()

# We do galaxies before planets now in order to satisfy the planet(x,y) FK

# ########################################################################### #
# ##############################    GALAXIES    ############################# #
# ########################################################################### #

        # Update the newly dumped data with IDs from the current data
        #  based on an x,y match in the two tables (and active=True)
        session.execute(text("""UPDATE galaxy_temp AS t SET
                                  id = g.id
                                FROM (SELECT id, x, y FROM galaxy) AS g
                                  WHERE t.x = g.x AND t.y = g.y
                            ;"""))

        # Make sure all the galaxies are active,
        #  some might have been deactivated previously
        session.execute(text("""UPDATE galaxy SET
                                  active = :true
                            ;""", bindparams=[true]))

        t2=time.time()-t1
        print "Copy galaxy ids to temp and activate in %.3f seconds" % (t2,)
        t1=time.time()

        # For galaxies that are no longer present in the new dump, we will
        #  NULL all the data, leaving only the coords and id for FKs
        session.execute(text("""UPDATE galaxy SET
                                  active = :false,
                                  name = NULL, size = NULL, score = NULL, value = NULL, xp = NULL,
                                  members = NULL, member_growth = NULL,
                                  size_growth = NULL, score_growth = NULL, value_growth = NULL, xp_growth = NULL,
                                  size_growth_pc = NULL, score_growth_pc = NULL, value_growth_pc = NULL, xp_growth_pc = NULL,
                                  size_rank_change = NULL, score_rank_change = NULL, value_rank_change = NULL, xp_rank_change = NULL,
                                  size_rank = NULL, score_rank = NULL, value_rank = NULL, xp_rank = NULL
                                WHERE id NOT IN (SELECT id FROM galaxy_temp WHERE id IS NOT NULL)
                            ;""", bindparams=[false]))

        # Any galaxies in the temp table without an id are new
        # Insert them to the current table and the id(serial/auto_increment)
        #  will be generated, and we can then copy it back to the temp table
        # Galaxies under a certain amount of planets are private
        session.execute(text("""INSERT INTO galaxy (x, y, active, private)
                                SELECT g.x, g.y, :true, count(p) <= :priv_gal OR (g.x = 1 AND g.y = 1)
                                FROM
                                  galaxy_temp as g,
                                  (SELECT x, y FROM planet_temp) as p
                                WHERE
                                  g.x = p.x AND g.y = p.y AND
                                  g.id IS NULL
                                GROUP BY
                                  g.x, g.y
                            ;""", bindparams=[true, bindparam("priv_gal",PA.getint("numbers", "priv_gal"))]))
        session.execute(text("UPDATE galaxy_temp SET id = (SELECT id FROM galaxy WHERE galaxy.x = galaxy_temp.x AND galaxy.y = galaxy_temp.y AND galaxy.active = :true ORDER BY galaxy.id DESC) WHERE id IS NULL;", bindparams=[true]))

        t2=time.time()-t1
        print "Deactivate old galaxies and generate new galaxy ids in %.3f seconds" % (t2,)
        t1=time.time()

        # Update everything from the temp table and generate ranks
        # Deactivated items are untouched but NULLed earlier
        session.execute(text("""UPDATE galaxy AS g SET
                                  x = t.x, y = t.y,
                                  name = t.name, size = t.size, score = t.score, value = t.value, xp = t.xp,
                                  members = p.count,
                             """ + (
                             """
                                  size_growth = t.size - COALESCE(g.size - g.size_growth, 0),
                                  score_growth = t.score - COALESCE(g.score - g.score_growth, 0),
                                  value_growth = t.value - COALESCE(g.value - g.value_growth, 0),
                                  xp_growth = t.xp - COALESCE(g.xp - g.xp_growth, 0),
                                  member_growth = p.count - COALESCE(g.members - g.member_growth, 0),
                                  size_growth_pc = CASE WHEN (g.size - g.size_growth != 0) THEN COALESCE((t.size - (g.size - g.size_growth)) * 100.0 / (g.size - g.size_growth), 0) ELSE 0 END,
                                  score_growth_pc = CASE WHEN (g.score - g.score_growth != 0) THEN COALESCE((t.score - (g.score - g.score_growth)) * 100.0 / (g.score - g.score_growth), 0) ELSE 0 END,
                                  value_growth_pc = CASE WHEN (g.value - g.value_growth != 0) THEN COALESCE((t.value - (g.value - g.value_growth)) * 100.0 / (g.value - g.value_growth), 0) ELSE 0 END,
                                  xp_growth_pc = CASE WHEN (g.xp - g.xp_growth != 0) THEN COALESCE((t.xp - (g.xp - g.xp_growth)) * 100.0 / (g.xp - g.xp_growth), 0) ELSE 0 END,
                                  size_rank_change = t.size_rank - COALESCE(g.size_rank - g.size_rank_change, 0),
                                  score_rank_change = t.score_rank - COALESCE(g.score_rank - g.score_rank_change, 0),
                                  value_rank_change = t.value_rank - COALESCE(g.value_rank - g.value_rank_change, 0),
                                  xp_rank_change = t.xp_rank - COALESCE(g.xp_rank - g.xp_rank_change, 0),
                             """ if not midnight
                                 else
                             """
                                  size_growth = t.size - COALESCE(g.size, 0),
                                  score_growth = t.score - COALESCE(g.score, 0),
                                  value_growth = t.value - COALESCE(g.value, 0),
                                  xp_growth = t.xp - COALESCE(g.xp, 0),
                                  member_growth = p.count - COALESCE(g.members, 0),
                                  size_growth_pc = CASE WHEN (g.size != 0) THEN COALESCE((t.size - g.size) * 100.0 / g.size, 0) ELSE 0 END,
                                  score_growth_pc = CASE WHEN (g.score != 0) THEN COALESCE((t.score - g.score) * 100.0 / g.score * 100, 0) ELSE 0 END,
                                  value_growth_pc = CASE WHEN (g.value != 0) THEN COALESCE((t.value - g.value) * 100.0 / g.value, 0) ELSE 0 END,
                                  xp_growth_pc = CASE WHEN (g.xp != 0) THEN COALESCE((t.xp - g.xp) * 100.0 / g.xp, 0) ELSE 0 END,
                                  size_rank_change = t.size_rank - COALESCE(g.size_rank, 0),
                                  score_rank_change = t.score_rank - COALESCE(g.score_rank, 0),
                                  value_rank_change = t.value_rank - COALESCE(g.value_rank, 0),
                                  xp_rank_change = t.xp_rank - COALESCE(g.xp_rank, 0),
                             """ ) +
                             """
                                  size_rank = t.size_rank, score_rank = t.score_rank, value_rank = t.value_rank, xp_rank = t.xp_rank
                                FROM (SELECT *,
                                  rank() OVER (ORDER BY size DESC) AS size_rank,
                                  rank() OVER (ORDER BY score DESC) AS score_rank,
                                  rank() OVER (ORDER BY value DESC) AS value_rank,
                                  rank() OVER (ORDER BY xp DESC) AS xp_rank
                                FROM galaxy_temp) AS t,
                                  (SELECT count(*) AS count, x, y FROM planet_temp GROUP BY x, y) AS p
                                  WHERE g.id = t.id
                                   AND g.x = p.x AND g.y = p.y
                                AND g.active = :true
                            ;""", bindparams=[true]))

        t2=time.time()-t1
        print "Update galaxies from temp and generate ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##############################    PLANETS    ############################## #
# ########################################################################### #

        # Update the newly dumped data with IDs from the current data
        #  based on an ruler-,planet-name match in the two tables (and active=True)
        session.execute(text("""UPDATE planet_temp AS t SET
                                  id = p.id
                                FROM (SELECT id, rulername, planetname FROM planet WHERE active = :true) AS p
                                  WHERE t.rulername = p.rulername AND t.planetname = p.planetname
                            ;""", bindparams=[true]))

        t2=time.time()-t1
        print "Copy planet ids to temp in %.3f seconds" % (t2,)
        t1=time.time()

        while last_tick > PA.getint("numbers", "shuffle"): #looks are deceiving, this only runs once
            # This code is designed to match planets whose ruler/planet names
            #  change, by matching them with new planets using certain criteria

            def load_planet_id_search():
                # If we have any ids in the planet_new_id_search table,
                #  match them up with planet_temp using x,y,z
                session.execute(text("UPDATE planet_temp SET id = (SELECT id FROM planet_new_id_search WHERE planet_temp.x = planet_new_id_search.x AND planet_temp.y = planet_new_id_search.y AND planet_temp.z = planet_new_id_search.z) WHERE id IS NULL;"))
                # Empty out the two search tables
                session.execute(planet_new_id_search.delete())
                session.execute(planet_old_id_search.delete())
                # Insert from the new tick any planets without id
                if session.execute(text("INSERT INTO planet_new_id_search (id, x, y, z, race, size, score, value, xp) SELECT id, x, y, z, race, size, score, value, xp FROM planet_temp WHERE planet_temp.id IS NULL;")).rowcount < 1:
                    return None
                # Insert from the previous tick any planets without
                #  an equivalent planet from the new tick
                if session.execute(text("INSERT INTO planet_old_id_search (id, x, y, z, race, size, score, value, xp, vdiff) SELECT id, x, y, z, race, size, score, value, xp, vdiff FROM planet WHERE planet.id NOT IN (SELECT id FROM planet_temp WHERE id IS NOT NULL) AND planet.active = :true;", bindparams=[true])).rowcount < 1:
                    return None
                # If either of the two search tables do not have any planets
                #  to match moved in (.rowcount() < 1) then return None, else:
                return 1

            # Load in the planets to match against and use the first set of match criterion
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
            # As above, second set of criterion
            if load_planet_id_search() is None: break
            session.execute(text("""UPDATE planet_new_id_search SET id = (
                                      SELECT id FROM planet_old_id_search WHERE
                                        planet_old_id_search.x = planet_new_id_search.x AND
                                        planet_old_id_search.y = planet_new_id_search.y AND
                                        planet_old_id_search.z = planet_new_id_search.z AND
                                        planet_old_id_search.race = planet_new_id_search.race AND
                                        planet_old_id_search.value > 500000 AND
                                        planet_new_id_search.value BETWEEN
                                                planet_old_id_search.value - (2* planet_old_id_search.vdiff) AND 
                                                planet_old_id_search.value + (2* planet_old_id_search.vdiff)
                                      );"""))
            # Third set of criterion
            if load_planet_id_search() is None: break
            session.execute(text("""UPDATE planet_new_id_search SET id = (
                                      SELECT id FROM planet_old_id_search WHERE
                                        planet_old_id_search.race = planet_new_id_search.race AND
                                        planet_old_id_search.size > 500 AND
                                        planet_old_id_search.size = planet_new_id_search.size AND
                                        planet_old_id_search.value > 500000 AND
                                        planet_new_id_search.value BETWEEN
                                                planet_old_id_search.value - (2* planet_old_id_search.vdiff) AND
                                                planet_old_id_search.value + (2* planet_old_id_search.vdiff)
                                      );"""))
            # Fourth set of criterion for smaller planets
            if load_planet_id_search() is None: break
            session.execute(text("""UPDATE planet_new_id_search SET id = (
                                      SELECT id FROM planet_old_id_search WHERE
                                        planet_old_id_search.x = planet_new_id_search.x AND
                                        planet_old_id_search.y = planet_new_id_search.y AND
                                        planet_old_id_search.z = planet_new_id_search.z AND
                                        planet_old_id_search.race = planet_new_id_search.race AND
                                        planet_old_id_search.size = planet_new_id_search.size AND
                                        planet_new_id_search.value BETWEEN
                                                planet_old_id_search.value - (2* planet_old_id_search.vdiff) AND
                                                planet_old_id_search.value + (2* planet_old_id_search.vdiff)
                                      );"""))
            break

        t2=time.time()-t1
        print "Lost planet ids match up in %.3f seconds" % (t2,)
        t1=time.time()

        # For planets that are no longer present in the new dump, we will
        #  NULL all the data, leaving only the coords and id for FKs
        session.execute(text("""UPDATE planet SET
                                  active = :false,
                                  size = NULL, score = NULL, value = NULL, xp = NULL,
                                  size_growth = NULL, score_growth = NULL, value_growth = NULL, xp_growth = NULL,
                                  size_growth_pc = NULL, score_growth_pc = NULL, value_growth_pc = NULL, xp_growth_pc = NULL,
                                  size_rank_change = NULL, score_rank_change = NULL, value_rank_change = NULL, xp_rank_change = NULL,
                                  size_rank = NULL, score_rank = NULL, value_rank = NULL, xp_rank = NULL,
                                  vdiff = NULL, idle = NULL
                                WHERE id NOT IN (SELECT id FROM planet_temp WHERE id IS NOT NULL)
                            ;""", bindparams=[false]))

        # Any planets in the temp table without an id are new
        # Insert them to the current table and the id(serial/auto_increment)
        #  will be generated, and we can then copy it back to the temp table
        session.execute(text("INSERT INTO planet (rulername, planetname, active) SELECT rulername, planetname, :true FROM planet_temp WHERE id IS NULL;", bindparams=[true]))
        session.execute(text("UPDATE planet_temp SET id = (SELECT id FROM planet WHERE planet.rulername = planet_temp.rulername AND planet.planetname = planet_temp.planetname AND planet.active = :true ORDER BY planet.id DESC) WHERE id IS NULL;", bindparams=[true]))

        t2=time.time()-t1
        print "Deactivate old planets and generate new planet ids in %.3f seconds" % (t2,)
        t1=time.time()

        # Update everything from the temp table and generate ranks
        # Deactivated items are untouched but NULLed earlier
        session.execute(text("""UPDATE planet AS p SET
                                  x = t.x, y = t.y, z = t.z,
                                  planetname = t.planetname, rulername = t.rulername, race = t.race,
                                  size = t.size, score = t.score, value = t.value, xp = t.xp,
                             """ + (
                             """
                                  size_growth = t.size - COALESCE(p.size - p.size_growth, 0),
                                  score_growth = t.score - COALESCE(p.score - p.score_growth, 0),
                                  value_growth = t.value - COALESCE(p.value - p.value_growth, 0),
                                  xp_growth = t.xp - COALESCE(p.xp - p.xp_growth, 0),
                                  size_growth_pc = CASE WHEN (p.size - p.size_growth != 0) THEN COALESCE((t.size - (p.size - p.size_growth)) * 100.0 / (p.size - p.size_growth), 0) ELSE 0 END,
                                  score_growth_pc = CASE WHEN (p.score - p.score_growth != 0) THEN COALESCE((t.score - (p.score - p.score_growth)) * 100.0 / (p.score - p.score_growth), 0) ELSE 0 END,
                                  value_growth_pc = CASE WHEN (p.value - p.value_growth != 0) THEN COALESCE((t.value - (p.value - p.value_growth)) * 100.0 / (p.value - p.value_growth), 0) ELSE 0 END,
                                  xp_growth_pc = CASE WHEN (p.xp - p.xp_growth != 0) THEN COALESCE((t.xp - (p.xp - p.xp_growth)) * 100.0 / (p.xp - p.xp_growth), 0) ELSE 0 END,
                                  size_rank_change = t.size_rank - COALESCE(p.size_rank - p.size_rank_change, 0),
                                  score_rank_change = t.score_rank - COALESCE(p.score_rank - p.score_rank_change, 0),
                                  value_rank_change = t.value_rank - COALESCE(p.value_rank - p.value_rank_change, 0),
                                  xp_rank_change = t.xp_rank - COALESCE(p.xp_rank - p.xp_rank_change, 0),
                             """ if not midnight
                                 else
                             """
                                  size_growth = t.size - COALESCE(p.size, 0),
                                  score_growth = t.score - COALESCE(p.score, 0),
                                  value_growth = t.value - COALESCE(p.value, 0),
                                  xp_growth = t.xp - COALESCE(p.xp, 0),
                                  size_growth_pc = CASE WHEN (p.size != 0) THEN COALESCE((t.size - p.size) * 100.0 / p.size, 0) ELSE 0 END,
                                  score_growth_pc = CASE WHEN (p.score != 0) THEN COALESCE((t.score - p.score) * 100.0 / p.score, 0) ELSE 0 END,
                                  value_growth_pc = CASE WHEN (p.value != 0) THEN COALESCE((t.value - p.value) * 100.0 / p.value, 0) ELSE 0 END,
                                  xp_growth_pc = CASE WHEN (p.xp != 0) THEN COALESCE((t.xp - p.xp) * 100.0 / p.xp, 0) ELSE 0 END,
                                  size_rank_change = t.size_rank - COALESCE(p.size_rank, 0),
                                  score_rank_change = t.score_rank - COALESCE(p.score_rank, 0),
                                  value_rank_change = t.value_rank - COALESCE(p.value_rank, 0),
                                  xp_rank_change = t.xp_rank - COALESCE(p.xp_rank, 0),
                             """ ) +
                             """
                                  size_rank = t.size_rank, score_rank = t.score_rank, value_rank = t.value_rank, xp_rank = t.xp_rank,
                                  vdiff = t.value - p.value,
                                  idle = COALESCE(1 + (SELECT p.idle WHERE (t.value-p.value) BETWEEN (p.vdiff-1) AND (p.vdiff+1) AND (p.xp-t.xp=0) ), 0)
                                FROM (SELECT *,
                                  rank() OVER (ORDER BY size DESC) AS size_rank,
                                  rank() OVER (ORDER BY score DESC) AS score_rank,
                                  rank() OVER (ORDER BY value DESC) AS value_rank,
                                  rank() OVER (ORDER BY xp DESC) AS xp_rank
                                FROM planet_temp) AS t
                                  WHERE p.id = t.id
                                AND p.active = :true
                            ;""", bindparams=[true]))

        t2=time.time()-t1
        print "Update planets from temp and generate ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# #############################    ALLIANCES    ############################# #
# ########################################################################### #

        # Update the newly dumped data with IDs from the current data
        #  based on a name match in the two tables (and active=True)
        session.execute(text("""UPDATE alliance_temp AS t SET
                                  id = a.id
                                FROM (SELECT id, name FROM alliance) AS a
                                  WHERE t.name = a.name
                            ;"""))

        # Make sure all the alliances are active,
        #  some might have been deactivated previously
        session.execute(text("""UPDATE alliance SET
                                  active = :true
                            ;""", bindparams=[true]))

        t2=time.time()-t1
        print "Copy alliance ids to temp and activate in %.3f seconds" % (t2,)
        t1=time.time()

        # For alliances that are no longer present in the new dump, we will
        #  NULL all the data, leaving only the name and id for FKs
        session.execute(text("""UPDATE alliance SET
                                  active = :false,
                                  size = NULL, members = NULL, score = NULL, points = NULL, size_avg = NULL, score_avg = NULL, points_avg = NULL,
                                  size_growth = NULL, score_growth = NULL, points_growth = NULL, member_growth = NULL,
                                  size_growth_pc = NULL, score_growth_pc = NULL, points_growth_pc = NULL,
                                  size_avg_growth = NULL, score_avg_growth = NULL, points_avg_growth = NULL,
                                  size_avg_growth_pc = NULL, score_avg_growth_pc = NULL, points_avg_growth_pc = NULL,
                                  size_rank_change = NULL, members_rank_change = NULL, score_rank_change = NULL, points_rank_change = NULL, size_avg_rank_change = NULL, score_avg_rank_change = NULL, points_avg_rank_change = NULL,
                                  size_rank = NULL, members_rank = NULL, score_rank = NULL, points_rank = NULL, size_avg_rank = NULL, score_avg_rank = NULL, points_avg_rank = NULL
                                WHERE id NOT IN (SELECT id FROM alliance_temp WHERE id IS NOT NULL)
                            ;""", bindparams=[false]))

        # Any alliances in the temp table without an id are new
        # Insert them to the current table and the id(serial/auto_increment)
        #  will be generated, and we can then copy it back to the temp table
        session.execute(text("INSERT INTO alliance (name, active) SELECT name, :true FROM alliance_temp WHERE id IS NULL;", bindparams=[true]))
        session.execute(text("UPDATE alliance_temp SET id = (SELECT id FROM alliance WHERE alliance.name = alliance_temp.name AND alliance.active = :true ORDER BY alliance.id DESC) WHERE id IS NULL;", bindparams=[true]))

        t2=time.time()-t1
        print "Deactivate old alliances and generate new alliance ids in %.3f seconds" % (t2,)
        t1=time.time()

        # Update everything from the temp table and generate ranks
        # Deactivated items are untouched but NULLed earlier
        session.execute(text("""UPDATE alliance AS a SET
                                  size = t.size, members = t.members, score = t.score, points = t.points,
                                  size_avg = t.size_avg, score_avg = t.score_avg, points_avg = t.points_avg,
                             """ + (
                             """
                                  size_growth = t.size - COALESCE(a.size - a.size_growth, 0),
                                  score_growth = t.score - COALESCE(a.score - a.score_growth, 0),
                                  points_growth = t.points - COALESCE(a.points - a.points_growth, 0),
                                  member_growth = t.members - COALESCE(a.members - a.member_growth, 0),
                                  size_growth_pc = CASE WHEN (a.size - a.size_growth != 0) THEN COALESCE((t.size - (a.size - a.size_growth)) * 100.0 / (a.size - a.size_growth), 0) ELSE 0 END,
                                  score_growth_pc = CASE WHEN (a.score - a.score_growth != 0) THEN COALESCE((t.score - (a.score - a.score_growth)) * 100.0 / (a.score - a.score_growth), 0) ELSE 0 END,
                                  points_growth_pc = CASE WHEN (a.points - a.points_growth != 0) THEN COALESCE((t.points - (a.points - a.points_growth)) * 100.0 / (a.points - a.points_growth), 0) ELSE 0 END,
                                  size_avg_growth = t.size_avg - COALESCE(a.size_avg - a.size_avg_growth, 0),
                                  score_avg_growth = t.score_avg - COALESCE(a.score_avg - a.score_avg_growth, 0),
                                  points_avg_growth = t.points_avg - COALESCE(a.points_avg - a.points_avg_growth, 0),
                                  size_avg_growth_pc = CASE WHEN (a.size_avg - a.size_avg_growth != 0) THEN COALESCE((t.size_avg - (a.size_avg - a.size_avg_growth)) * 100.0 / (a.size_avg - a.size_avg_growth), 0) ELSE 0 END,
                                  score_avg_growth_pc = CASE WHEN (a.score_avg - a.score_avg_growth != 0) THEN COALESCE((t.score_avg - (a.score_avg - a.score_avg_growth)) * 100.0 / (a.score_avg - a.score_avg_growth), 0) ELSE 0 END,
                                  points_avg_growth_pc = CASE WHEN (a.points_avg - a.points_avg_growth != 0) THEN COALESCE((t.points_avg - (a.points_avg - a.points_avg_growth)) * 100.0 / (a.points_avg - a.points_avg_growth), 0) ELSE 0 END,
                                  size_rank_change = t.size_rank - COALESCE(a.size_rank - a.size_rank_change, 0),
                                  members_rank_change = t.members_rank - COALESCE(a.members_rank - a.members_rank_change, 0),
                                  score_rank_change = t.score_rank - COALESCE(a.score_rank - a.score_rank_change, 0),
                                  points_rank_change = t.points_rank - COALESCE(a.points_rank - a.points_rank_change, 0),
                                  size_avg_rank_change = t.size_avg_rank - COALESCE(a.size_avg_rank - a.size_avg_rank_change, 0),
                                  score_avg_rank_change = t.score_avg_rank - COALESCE(a.score_avg_rank - a.score_avg_rank_change, 0),
                                  points_avg_rank_change = t.points_avg_rank - COALESCE(a.points_avg_rank - a.points_avg_rank_change, 0),
                             """ if not midnight
                                 else
                             """
                                  size_growth = t.size - COALESCE(a.size, 0),
                                  score_growth = t.score - COALESCE(a.score, 0),
                                  points_growth = t.points - COALESCE(a.points, 0),
                                  member_growth = t.members - COALESCE(a.members, 0),
                                  size_growth_pc = CASE WHEN (a.size != 0) THEN COALESCE((t.size - a.size) * 100.0 / a.size, 0) ELSE 0 END,
                                  score_growth_pc = CASE WHEN (a.score != 0) THEN COALESCE((t.score - a.score) * 100.0 / a.score, 0) ELSE 0 END,
                                  points_growth_pc = CASE WHEN (a.points != 0) THEN COALESCE((t.points - a.points) * 100.0 / a.points, 0) ELSE 0 END,
                                  size_avg_growth = t.size_avg - COALESCE(a.size_avg, 0),
                                  score_avg_growth = t.score_avg - COALESCE(a.score_avg, 0),
                                  points_avg_growth = t.points_avg - COALESCE(a.points_avg, 0),
                                  size_avg_growth_pc = CASE WHEN (a.size_avg != 0) THEN COALESCE((t.size_avg - a.size_avg) * 100.0 / a.size_avg, 0) ELSE 0 END,
                                  score_avg_growth_pc = CASE WHEN (a.score_avg != 0) THEN COALESCE((t.score_avg - a.score_avg) * 100.0 / a.score_avg, 0) ELSE 0 END,
                                  points_avg_growth_pc = CASE WHEN (a.points_avg != 0) THEN COALESCE((t.points_avg - a.points_avg) * 100.0 / a.points_avg, 0) ELSE 0 END,
                                  size_rank_change = t.size_rank - COALESCE(a.size_rank, 0),
                                  members_rank_change = t.members_rank - COALESCE(a.members_rank, 0),
                                  score_rank_change = t.score_rank - COALESCE(a.score_rank, 0),
                                  points_rank_change = t.points_rank - COALESCE(a.points_rank, 0),
                                  size_avg_rank_change = t.size_avg_rank - COALESCE(a.size_avg_rank, 0),
                                  score_avg_rank_change = t.score_avg_rank - COALESCE(a.score_avg_rank, 0),
                                  points_avg_rank_change = t.points_avg_rank - COALESCE(a.points_avg_rank, 0),
                             """ ) +
                             """
                                  size_rank = t.size_rank, members_rank = t.members_rank, score_rank = t.score_rank, points_rank = t.points_rank,
                                  size_avg_rank = t.size_avg_rank, score_avg_rank = t.score_avg_rank, points_avg_rank = t.points_avg_rank
                                FROM (SELECT *,
                                  rank() OVER (ORDER BY size DESC) AS size_rank,
                                  rank() OVER (ORDER BY points DESC) AS points_rank,
                                  rank() OVER (ORDER BY members DESC) AS members_rank,
                                  rank() OVER (ORDER BY size_avg DESC) AS size_avg_rank,
                                  rank() OVER (ORDER BY score_avg DESC) AS score_avg_rank,
                                  rank() OVER (ORDER BY points_avg DESC) AS points_avg_rank
                                FROM alliance_temp) AS t
                                  WHERE a.id = t.id
                                AND a.active = :true
                            ;""", bindparams=[true]))

        t2=time.time()-t1
        print "Update alliances from temp and generate ranks in %.3f seconds" % (t2,)
        t1=time.time()

# ########################################################################### #
# ##################   HISTORY: EVERYTHING BECOMES FINAL   ################## #
# ########################################################################### #

        # Uncomment this line to allow ticking on the same data for debug
        # planet_tick = last_tick + 1

        # Insert a record of the tick, with counts of the dumps
        #  and a timestamp generated by SQLA
        session.execute(Updates.__table__.insert().values(
                          id=planet_tick,
                          galaxies=Galaxy.__table__.count(Galaxy.active==True),
                          planets=Planet.__table__.count(Planet.active==True),
                          alliances=Alliance.__table__.count(Alliance.active==True)
                        ))

        # Create records of planet movements or deletions
        session.execute(text("INSERT INTO planet_exiles (tick, id, oldx, oldy, oldz, newx, newy, newz) SELECT :tick, planet.id, planet_history.x, planet_history.y, planet_history.z, planet.x, planet.y, planet.z FROM planet, planet_history WHERE planet.id = planet_history.id AND planet_history.tick = :oldtick AND (planet.active = :true AND (planet.x != planet_history.x OR planet.y != planet_history.y OR planet.z != planet_history.z) OR planet.active = :false);", bindparams=[bindparam("tick",planet_tick), bindparam("oldtick",last_tick), true, false]))

        # Copy the dumps to their respective history tables
        session.execute(text("INSERT INTO galaxy_history (tick, id, x, y, name, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank) SELECT :tick, id, x, y, name, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank FROM galaxy WHERE galaxy.active = :true ORDER BY id ASC;", bindparams=[bindparam("tick",planet_tick), true]))
        session.execute(text("INSERT INTO planet_history (tick, id, x, y, z, planetname, rulername, race, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank, idle, vdiff) SELECT :tick, id, x, y, z, planetname, rulername, race, size, score, value, xp, size_rank, score_rank, value_rank, xp_rank, idle, vdiff FROM planet WHERE planet.active = :true ORDER BY id ASC;", bindparams=[bindparam("tick",planet_tick), true]))
        session.execute(text("INSERT INTO alliance_history (tick, id, name, size, members, score, points, size_avg, score_avg, points_avg, size_rank, members_rank, score_rank, points_rank, size_avg_rank, score_avg_rank, points_avg_rank) SELECT :tick, id, name, size, members, score, points, size_avg, score_avg, points_avg, size_rank, members_rank, score_rank, points_rank, size_avg_rank, score_avg_rank, points_avg_rank FROM alliance WHERE alliance.active = :true ORDER BY id ASC;", bindparams=[bindparam("tick",planet_tick), true]))

        # Finally we can commit!
        session.commit()

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

session.close()

t1=time.time()-t_start
print "Total time taken: %.3f seconds" % (t1,)

# Measure some dicks
last_tick = Updates.current_tick()
history_tick = max(last_tick-72, 1)
t_start=time.time()
t1=t_start
session.execute(epenis.__table__.delete())
session.execute(text("SELECT setval('epenis_rank_seq', 1, :false);", bindparams=[false]))
session.execute(text("INSERT INTO epenis (user_id, penis) SELECT users.id, planet.score - planet_history.score FROM users, planet, planet_history WHERE users.active = :true AND users.access >= :member AND planet.active = :true AND users.planet_id = planet.id AND planet.id = planet_history.id AND planet_history.tick = :tick ORDER BY planet.score - planet_history.score DESC;", bindparams=[true,bindparam("member",Config.getint("Access","member")),bindparam("tick",history_tick)]))
t2=time.time()-t1
print "epenis in %.3f seconds" % (t2,)
t1=time.time()
session.execute(galpenis.__table__.delete())
session.execute(text("SELECT setval('galpenis_rank_seq', 1, :false);", bindparams=[false]))
session.execute(text("INSERT INTO galpenis (galaxy_id, penis) SELECT galaxy.id, galaxy.score - galaxy_history.score FROM galaxy, galaxy_history WHERE galaxy.active = :true AND galaxy.id = galaxy_history.id AND galaxy_history.tick = :tick ORDER BY galaxy.score - galaxy_history.score DESC;", bindparams=[true,bindparam("tick",history_tick)]))
t2=time.time()-t1
print "galpenis in %.3f seconds" % (t2,)
t1=time.time()
session.execute(apenis.__table__.delete())
session.execute(text("SELECT setval('apenis_rank_seq', 1, :false);", bindparams=[false]))
session.execute(text("INSERT INTO apenis (alliance_id, penis) SELECT alliance.id, alliance.score - alliance_history.score FROM alliance, alliance_history WHERE alliance.active = :true AND alliance.id = alliance_history.id AND alliance_history.tick = :tick ORDER BY alliance.score - alliance_history.score DESC;", bindparams=[true,bindparam("tick",history_tick)]))
t2=time.time()-t1
print "apenis in %.3f seconds" % (t2,)
session.commit()
t1=time.time()-t_start
print "Total penis time: %.3f seconds" % (t1,)
session.close()
