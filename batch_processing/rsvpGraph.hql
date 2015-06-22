DROP TABLE rsvpGraph;

CREATE EXTERNAL TABLE IF NOT EXISTS rsvpGraph1 (rsvpid bigint , eventid string , groupid int , created bigint , response string,
guests int, membername string , memberid string, mtime bigint)
ROW FORMAT DELIMITED FIELDS TERMINATED BY "," LINES TERMINATED BY "\n"
STORED AS TEXTFILE LOCATION '/user/meetup/rsvp';

CREATE EXTERNAL TABLE IF NOT EXISTS rsvpGraph2 (rsvpid bigint , eventid string , groupid int , created bigint, response string,
guests int, membername string , memberid string, mtime bigint)
ROW FORMAT DELIMITED FIELDS TERMINATED BY "," LINES TERMINATED BY "\n"
STORED AS TEXTFILE LOCATION '/user/meetup/rsvp';

DROP VIEW JOINTEVENTS;
DROP VIEW RES;

CREATE VIEW JOINTEVENTS;
AS
SELECT  rsvpGraph1.membername as name1, rsvpGraph1.memberid AS id1, rsvpGraph2.membername as name2, rsvpGraph2.memberid AS id2
FROM rsvpGraph1, rsvpGraph2
WHERE rsvpGraph1.eventid = rsvpGraph2.eventid;

CREATE VIEW RES(name1 , id1 , name2 , id2 , cooccurrence)
AS
SELECT name1, id1 ,name2, id2 ,count(*)
FROM JOINTEVENTS
GROUP BY id1,name1,id2,name2;

SELECT name1, name2, cooccurrence
FROM RES
WHERE id1 != id2 AND cooccurrence !=1
ORDER BY name1, cooccurrence DESC;