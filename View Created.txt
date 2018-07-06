Created  views:
CREATE VIEW status_tot AS
SELECT time ::date,status
FROM log;

CREATE VIEW failed_status AS
SELECT time,count(*) AS number
FROM status_tot WHERE status = '404 NOT FOUND'
GROUP BY time;


CREATE VIEW all_status as
SELECT time, count(*) AS num
FROM status_tot WHERE status = '404 NOT FOUND' OR status = '200 OK'
GROUP BY time;

CREATE VIEW percent_ount AS
SELECT all_status.time, all_status.num AS numall,
       failed_status.number AS numfailed,
       failed_status.number::double precision/all_status.num::double precision * 100 AS percentagefailed
FROM all_status,failed_status WHERE all_status.time = failed_status.time;