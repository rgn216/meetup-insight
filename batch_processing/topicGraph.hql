DROP TABLE topicGraph1;
DROP TABLE topicGraph2;

CREATE EXTERNAL TABLE IF NOT EXISTS topicGraph1 ( memberid string, membername string, topicid string, topicname string )
ROW FORMAT DELIMITED FIELDS TERMINATED BY "," LINES TERMINATED BY "\n"
STORED AS TEXTFILE LOCATION '/user/meetup/topics';

CREATE EXTERNAL TABLE IF NOT EXISTS topicGraph2 ( memberid string, membername string, topicid string, topicname string )
ROW FORMAT DELIMITED FIELDS TERMINATED BY "," LINES TERMINATED BY "\n"
STORED AS TEXTFILE LOCATION '/user/meetup/topics';

DROP VIEW JOINTOPICS;
DROP VIEW RES;

CREATE VIEW JOINTOPICS
AS
SELECT  topicGraph1.membername as name1, topicGraph1.memberid AS id1, topicGraph2.membername as name2, topicGraph2.memberid AS id2
FROM topicGraph1, topicGraph2
WHERE topicGraph1.topicid = topicGraph2.topicid AND topicGraph1.memberid != topicGraph2.memberid;

CREATE VIEW RES(name1 , id1 , name2 , id2 , cooccurrence)
AS
SELECT name1, id1 ,name2, id2 ,count(*)
FROM JOINTOPICS
GROUP BY id1,id2;

INSERT OVERWRITE DIRECTORY '/user/topic_output_hive'
ROW FORMAT DELIMITED FIELDS TERMINATED BY "\t" LINES TERMINATED BY "\n"

SELECT name1, name2, cooccurrence
FROM RES
WHERE id1 != id2 AND cooccurrence !=1
ORDER BY name1, cooccurrence DESC;