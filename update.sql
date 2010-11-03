/*
    Columns
*/
alter table planet add column age integer;
alter table planet add column totalroundroids integer;
alter table planet add column totallostroids integer;
alter table planet add column ticksroiding integer;
alter table planet add column ticksroided integer;
alter table planet add column tickroids integer;
alter table planet add column avroids float;

/*
    Age
*/
update planet as p set age = history.c
from
(
    select id, count(*) as c from planet_history group by id
) as history
where history.id = p.id;

/*
    Total Round Roids
*/
update planet as p set totalroundroids = history.s
from
(
	select c.id as id, sum(c.size- o.size) as s
	from
		(select id, rank() over (partition by id order by tick asc) as time, size from planet_history) as c,
		(select id, rank() over (partition by id order by tick asc) as time, size from planet_history) as o
		where o.id=c.id and c.time = o.time+1 and c.size > o.size
		group by c.id
) as history
where history.id = p.id;
update planet as p set totalroundroids = coalesce(p.totalroundroids, 0) + history.size
from
(
	select id, rank() over (partition by id order by tick asc) as time, size from planet_history
) as history
where history.id = p.id and history.time=1;

/*
    Total Lost Roids
*/
update planet as p set totallostroids = history.s
from
(
    select c.id as id, sum(o.size - c.size) as s
	from
		(select id, rank() over (partition by id order by tick asc) as time, size from planet_history) as c,
		(select id, rank() over (partition by id order by tick asc) as time, size from planet_history) as o
		where o.id=c.id and c.time = o.time+1 and c.size < o.size
		group by c.id
) as history
where history.id = p.id;
update planet as p set totallostroids = coalesce(p.totallostroids, 0);

/*
    Ticks Roiding
*/
update planet as p set ticksroiding = history.c
from
(
    select c.id as id, count(nullif((c.size - o.size), (c.xp - o.xp))) as c
	from
		(select id, rank() over (partition by id order by tick asc) as time, size, xp from planet_history) as c,
		(select id, rank() over (partition by id order by tick asc) as time, size, xp from planet_history) as o
		where o.id=c.id and c.time = o.time+1 and c.size > o.size
		group by c.id
) as history
where history.id = p.id;
update planet as p set ticksroiding = coalesce(p.ticksroiding, 0);

/*
    Ticks Roided
*/
update planet as p set ticksroided = history.c
from
(
    select c.id as id, count(*) as c
	from
		(select id, rank() over (partition by id order by tick asc) as time, size, xp from planet_history) as c,
		(select id, rank() over (partition by id order by tick asc) as time, size, xp from planet_history) as o
		where o.id=c.id and c.time = o.time+1 and c.size < o.size
		group by c.id
) as history
where history.id = p.id;
update planet as p set ticksroiding = coalesce(p.ticksroiding, 0);

/*
    Tick-Roids
*/
update planet as p set tickroids = history.s
from
(
    select id, sum(size) as s from planet_history group by id
) as history
where history.id = p.id;
update planet as p set tickroids = coalesce(p.tickroids, 0);

/*
    Av Roids
*/
update planet as p set avroids = 1.0*p.tickroids/p.age;
