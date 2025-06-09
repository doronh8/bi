/*
list of top 100 users
in ppltx app-game
*/

--create or replace table `bi-course-461012.fp_scheduled_query.daily_segment` as
--truncate table `bi-course-461012.fp_scheduled_query.daily_segment`
insert into `bi-course-461012.fp_scheduled_query.daily_segment`
select
session_user() as source,
current_timestamp() as run_time,
rn as row_num,
left(generate_uuid(),8) as uuid,
cast ( ceil( 20 * rand()) as int64) as level
from
unnest(Generate_array(1,100)) as rn
order by level desc