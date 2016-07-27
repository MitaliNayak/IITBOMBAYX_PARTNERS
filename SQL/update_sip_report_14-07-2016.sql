UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS id,"Course" as''A'',"RCID" as''B'' ,"Institute" as ''C''
,"Email" as''D'',"Name" as ''E'' ,"#Students" as ''F'' union all
select (@cnt := @cnt + 1) AS
id,query.course,query.rcid,query.institutename,query.email,query.name,query.student
from  (SELECT  e.course, ai.remotecenterid_id rcid
,i.institutename,p.email,concat(p.firstname," ", p.lastname) name
,count(*) student FROM `SIP_studentdetails` s, SIP_courselevelusers
c,SIP_edxcourses e,SIP_t10kt_institute i, SIP_personinformation
p,SIP_t10kt_approvedinstitute  ai where s.edxis_active =1 and s.teacherid_id=c.id and
c.personid_id=p.id and p.instituteid_id =i.instituteid and
p.instituteid_id !=0 and  e.id=c.courseid_id and  p.instituteid_id=
ai.instituteid_id and e.courseend >= DATE_ADD(NOW(), INTERVAL -7 DAY) and e.courseid != "IITBombayX/DC101/2015_25"
group by c.courseid_id, e.course,
p.email,p.firstname, p.lastname,p.instituteid_id
,i.institutename,ai.remotecenterid_id order by
e.id desc,ai.remotecenterid_id, student DESC ) query  CROSS JOIN
(SELECT @cnt := 0) AS dummy' WHERE `SIP_reports`.`reportid` = '6';



UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS
id,"Institute Name" as''A'',"RCID" as''B'' ,"HS791xA16" as ''C''
,"EE210xA16" as''D'',"SKANI101xA" as ''E''
union all  select (@cnt
:= @cnt + 1) AS
id,query.institutename,query.remotecenterid_id,query.hs,query.ee,query.sk
from (select
b.institutename,remotecenterid_id,sum(if(courseid_id=43,teachers,0)) as
hs ,sum(if(courseid_id=45,teachers,0)) as ee,
sum(if(courseid_id=41,teachers,0)) as sk
from (SELECT
a.instituteid_id,a.remotecenterid_id,b.courseid_id,count(personid_id)
teachers FROM `SIP_t10kt_approvedinstitute` a,SIP_courselevelusers b
where  a.instituteid_id=b.instituteid_id and roleid = 5 and
a.remotecenterid_id >1000 group by
a.instituteid_id,a.remotecenterid_id,b.courseid_id ) query,
SIP_t10kt_institute b WHERE instituteid_id=b.instituteid GROUP BY
b.institutename,remotecenterid_id ORDER BY remotecenterid_id,ee
DESC,hs DESC,sk DESC) query  CROSS JOIN (SELECT @cnt := 0) AS dummy
union all
select "Total",
"",count(distinct remotecenterid_id),sum(if(courseid_id=43,teachers,0)) as hs ,
sum(if(courseid_id=45,teachers,0)) as ee,
sum(if(courseid_id=41,teachers,0)) as sk
from (SELECT
a.instituteid_id,a.remotecenterid_id,b.courseid_id,count(personid_id)
teachers FROM `SIP_t10kt_approvedinstitute` a,SIP_courselevelusers b
where  a.instituteid_id=b.instituteid_id and roleid = 5 and
a.remotecenterid_id >1000 group by
a.instituteid_id,a.remotecenterid_id,b.courseid_id ) query,
SIP_t10kt_institute b WHERE instituteid_id=b.instituteid', `num_cols` = '5' WHERE `SIP_reports`.`reportid` = '7';


UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = '
select 0 AS id," " as A,"HS791xA16" as''B'',"EE210xA16" as ''C'' ,"SKANI101xA" as ''D''
 union all select (@cnt := @cnt + 1) AS id,
"No. of Institutes" a, query.hs,query.ee,query.sk 
from
 (SELECT sum( if( courseid_id =43, 1, 0 ) ) as hs,
         sum( if( courseid_id =45, 1, 0 ) ) as ee,
         sum( if( courseid_id =41, 1, 0 ) ) as sk
FROM (SELECT a.instituteid_id, a.remotecenterid_id, b.courseid_id, count( personid_id ) teachers
FROM `SIP_t10kt_approvedinstitute` a, SIP_courselevelusers b
WHERE a.instituteid_id = b.instituteid_id AND roleid =5
AND a.remotecenterid_id >1000
GROUP BY a.instituteid_id, a.remotecenterid_id, b.courseid_id )q)
query CROSS JOIN (SELECT @cnt := 0) AS dummy;
' WHERE `SIP_reports`.`reportid` = '8';


UPDATE `iitbxblended`.`SIP_reports` SET `num_cols` = '4' WHERE `SIP_reports`.`reportid` = '8';

UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = '
select 0 AS id,"Institute Name" as''A'',"RCID" as B,"HS791xA16" as''C'',"EE210xA16" as ''D'' ,"SKANI101xA" as ''E''
 union all select (@cnt := @cnt + 1) AS
id,query.remotecentername,query.remotecenterid,query.hs,query.ee,query.sk
FROM (SELECT t.remotecentername,t.remotecenterid,
sum(if(s.courseid="IITBombayX/HS791xA16/2016-17",1,0)) hs,
sum(if(s.courseid="IITBombayX/EE210xA16/2016-17",1,0)) ee,
sum(if(s.courseid="IITBombayX/SKANI101xA/2016_T2",1,0)) sk
FROM SIP_studentdetails s, SIP_courselevelusers c,
SIP_t10kt_remotecenter t
WHERE s.edxis_active =1 AND s.teacherid_id = c.id
 AND t.instituteid_id = c.instituteid_id AND c.instituteid_id !=0 AND t.remotecenterid >1000
group by t.remotecentername ORDER BY `t`.`remotecentername` ASC
      ) query
CROSS JOIN (SELECT @cnt := 0) AS dummy
union all
 SELECT "Total","",count(distinct t.remotecenterid),
 sum(if(s.courseid="IITBombayX/HS791xA16/2016-17",1,0)) hs,
sum(if(s.courseid="IITBombayX/EE210xA16/2016-17",1,0)) ee,
sum(if(s.courseid="IITBombayX/SKANI101xA/2016_T2",1,0)) sk
FROM SIP_studentdetails s, SIP_courselevelusers c,
SIP_t10kt_remotecenter t
WHERE s.edxis_active =1 AND s.teacherid_id = c.id
 AND t.instituteid_id = c.instituteid_id AND c.instituteid_id !=0 AND t.remotecenterid >1000 ', `num_cols` = '5' WHERE `SIP_reports`.`reportid` = '14';


INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`, `category`, `rel_rep_id`) VALUES ('45', '0', 'select 0 AS id,"Course" as''A'',"RCID" as''B'' ,"Institute" as ''C''
,"Email" as''D'',"Name" as ''E'' ,"#Students" as ''F'' union all
select (@cnt := @cnt + 1) AS
id,query.course,query.rcid,query.institutename,query.email,query.name,query.student
from  (SELECT  e.course, ai.remotecenterid_id rcid
,i.institutename,p.email,concat(p.firstname," ", p.lastname) name
,count(*) student FROM `SIP_studentdetails` s, SIP_courselevelusers
c,SIP_edxcourses e,SIP_t10kt_institute i, SIP_personinformation
p,SIP_t10kt_approvedinstitute  ai where s.edxis_active =1 and s.teacherid_id=c.id and
c.personid_id=p.id and p.instituteid_id =i.instituteid and
p.instituteid_id !=0 and  e.id=c.courseid_id and  p.instituteid_id=
ai.instituteid_id and e.courseend < DATE_ADD(NOW(), INTERVAL -7 DAY) and e.courseid != "IITBombayX/DC101/2015_25"
group by c.courseid_id, e.course,
p.email,p.firstname, p.lastname,p.instituteid_id
,i.institutename,ai.remotecenterid_id order by
e.id desc,ai.remotecenterid_id, student DESC ) query  CROSS JOIN
(SELECT @cnt := 0) AS dummy', 'Teacher wise- Students Summary of Archived Courses', 'Displays the summary of students who have been tagged by the teachers of Archived Courses', '6', 'Teacher-Students Association', NULL);




INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`, `category`, `rel_rep_id`) VALUES ('46', '0', 'select 0 AS
id,"Institute Name" as''A'',"RCID" as''B'' ,"CS101.1xS16" as ''C''
,"ME209xS16" as''D'',"EE210xS16" as ''E'', "HS791xS16" as F , "CS101.1xA15" as G
,"ME209.1xA15" as H,"EE210.1xA15" as I
union all  select (@cnt
:= @cnt + 1) AS
id,query.institutename,query.remotecenterid_id,query.cs,query.me,query.ee,query.hs,query.cso,query.meo,query.eeo
from (select
b.institutename,remotecenterid_id,sum(if(courseid_id=30,teachers,0)) as
cs ,sum(if(courseid_id=32,teachers,0)) as
me,sum(if(courseid_id=31,teachers,0)) as ee,sum(if(courseid_id=33,teachers,0)) as hs,
sum(if(courseid_id=6,teachers,0)) as
cso ,sum(if(courseid_id=7,teachers,0)) as
meo,sum(if(courseid_id=8,teachers,0)) as eeo
 from (SELECT
a.instituteid_id,a.remotecenterid_id,b.courseid_id,count(personid_id)
teachers FROM `SIP_t10kt_approvedinstitute` a,SIP_courselevelusers b
where  a.instituteid_id=b.instituteid_id and roleid = 5 and
a.remotecenterid_id >1000 group by
a.instituteid_id,a.remotecenterid_id,b.courseid_id ) query,
SIP_t10kt_institute b WHERE instituteid_id=b.instituteid GROUP BY
b.institutename,remotecenterid_id ORDER BY remotecenterid_id,cs
DESC,me DESC,ee DESC,hs DESC) query  CROSS JOIN (SELECT @cnt := 0) AS dummy
union all
select "Total",
"",count(distinct remotecenterid_id),sum(if(courseid_id=30,teachers,0)) as
cs ,sum(if(courseid_id=32,teachers,0)) as
me,sum(if(courseid_id=31,teachers,0)) as ee,sum(if(courseid_id=33,teachers,0)) as hs,
sum(if(courseid_id=6,teachers,0)) as
cso ,sum(if(courseid_id=7,teachers,0)) as
meo,sum(if(courseid_id=8,teachers,0)) as eeo
 from (SELECT
a.instituteid_id,a.remotecenterid_id,b.courseid_id,count(personid_id)
teachers FROM `SIP_t10kt_approvedinstitute` a,SIP_courselevelusers b
where  a.instituteid_id=b.instituteid_id and roleid = 5 and
a.remotecenterid_id >1000 group by
a.instituteid_id,a.remotecenterid_id,b.courseid_id ) query,
SIP_t10kt_institute b WHERE instituteid_id=b.instituteid', 'Teachers'' Participation for Academic year 2015-16', 'Number of teachers participating in respective courses institute-wise', '9', 'Institute-wise', NULL);



INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`, `category`, `rel_rep_id`) VALUES ('47', '0', 'select 0 AS id," " as A,"CS101.1xS16" as''B'',"ME209xS16" as ''C'' ,"EE210xS16" as ''D'',
"HS791xS16" E,"CS101.1xA15" as''F'',"ME209xA15" as ''G'' ,"EE210.1xA15" as ''H''
 union all select (@cnt := @cnt + 1) AS id,
"No. of Institutes" a, query.cs,query.me,query.ee,query.hs,query.cs1,query.me1,query.ee1 from
 (SELECT sum( if( courseid_id =30, 1, 0 ) ) as cs,
         sum( if( courseid_id =32, 1, 0 ) ) as me,
 sum( if( courseid_id =31, 1, 0 ) ) as ee,
 sum( if( courseid_id =33, 1, 0 ) ) as hs,
sum( if( courseid_id =6, 1, 0 ) ) as cs1,
         sum( if( courseid_id =7, 1, 0 ) ) as me1,
 sum( if( courseid_id =8, 1, 0 ) ) as ee1
 FROM (SELECT a.instituteid_id, a.remotecenterid_id, b.courseid_id, count( personid_id ) teachers
FROM `SIP_t10kt_approvedinstitute` a, SIP_courselevelusers b
WHERE a.instituteid_id = b.instituteid_id AND roleid =5
AND a.remotecenterid_id >1000
GROUP BY a.instituteid_id, a.remotecenterid_id, b.courseid_id )q)
query CROSS JOIN (SELECT @cnt := 0) AS dummy;', 'Institute wise Course Participation for Academic Year 2015-16', 'Displays Institutes'' Participation count in each Course of Academic Year 2015-16', '8', 'Institute-wise', NULL);


INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`, `category`, `rel_rep_id`) VALUES ('48', '0', 'select 0 AS id,"Institute Name" as''A'',"RCID" as B,"CS101.1xS16" as''C'' ,"ME209xS16" as''D'', "EE210.1xS16" as''E'',
"HS791xS16" as''F'' ,"CS101.1xA15" as''G'' ,"ME209xA15" as''H'', "EE210.1xA15" as''I''
 union all select (@cnt := @cnt + 1) AS
id,query.remotecentername,query.remotecenterid,query.CS101xS16,query.ME209xS16,query.EE210xS16 ,query.HS791xS16 ,
query.CS101xA15,query.ME209xA15,query.EE210xA15
FROM (SELECT t.remotecentername,t.remotecenterid,
sum(if(s.courseid="IITBombayX/EE210xS16/2016_T1",1,0)) EE210xS16,
sum(if(s.courseid="IITBombayX/ME209xS16/2016_T1",1,0)) ME209xS16,
sum(if(s.courseid="IITBombayX/CS101.1xS16/2016_T1",1,0)) CS101xS16,
sum(if(s.courseid="IITBombayX/HS791xS16/2016_T1",1,0)) HS791xS16,
sum(if(s.courseid="IITBombayX/EE210.1xA15/2015_T1",1,0)) EE210xA15,
sum(if(s.courseid="IITBombayX/ME209xA15/2015_T1",1,0)) ME209xA15,
sum(if(s.courseid="IITBombayX/CS101.1xA15/2015_T1",1,0)) CS101xA15
FROM SIP_studentdetails s, SIP_courselevelusers c,
SIP_t10kt_remotecenter t
WHERE s.edxis_active =1 AND s.teacherid_id = c.id
 AND t.instituteid_id = c.instituteid_id AND c.instituteid_id !=0
group by t.remotecentername ORDER BY `t`.`remotecentername` ASC
      ) query
CROSS JOIN (SELECT @cnt := 0) AS dummy
union all
 SELECT "Total","",count(distinct t.remotecenterid),
 sum(if(s.courseid="IITBombayX/CS101.1xS16/2016_T1",1,0)) CS101xS16,
sum(if(s.courseid="IITBombayX/ME209xS16/2016_T1",1,0)) ME209xS16,
sum(if(s.courseid="IITBombayX/EE210xS16/2016_T1",1,0)) EE210xS16,
sum(if(s.courseid="IITBombayX/HS791xS16/2016_T1",1,0)) HS791xS16,
sum(if(s.courseid="IITBombayX/EE210.1xA15/2015_T1",1,0)) EE210xA15,
sum(if(s.courseid="IITBombayX/ME209xA15/2015_T1",1,0)) ME209xA15,
sum(if(s.courseid="IITBombayX/CS101.1xA15/2015_T1",1,0)) CS101xA15
FROM SIP_studentdetails s, SIP_courselevelusers c,
SIP_t10kt_remotecenter t
WHERE s.edxis_active =1 AND s.teacherid_id = c.id
 AND t.instituteid_id = c.instituteid_id AND c.instituteid_id !=0    ', 'Students'' Participation for Academic Year 2015-16', 'Displays list of institutes with number of students participating in Blended Moocs program, per course for Academic Year 2015-16', '9', 'Institute-wise', NULL);


UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'Institute-wise: Students'' Participation for Academic Year 2015-16', `category` = 'Year 2015-16' WHERE `SIP_reports`.`reportid` = '48';

UPDATE `iitbxblended`.`SIP_reports` SET `category` = 'Year 2015-16' WHERE `SIP_reports`.`reportid` = '47';

UPDATE `iitbxblended`.`SIP_reports` SET `category` = 'Year 2015-16' WHERE `SIP_reports`.`reportid` = '46';

UPDATE `iitbxblended`.`SIP_reports` SET `category` = 'Year 2015-16' WHERE `SIP_reports`.`reportid` = '45';

UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS
id,"Institute Name" as''A'',"RCID" as''B'' ,"HS791xA16" as ''C''
,"EE210xA16" as''D'',"SKANI101xA" as ''E''
union all  select (@cnt
:= @cnt + 1) AS
id,query.institutename,query.remotecenterid_id,query.hs,query.ee,query.sk
from (select
b.institutename,remotecenterid_id,sum(if(courseid_id=42,teachers,0)) as
hs ,sum(if(courseid_id=45,teachers,0)) as ee,
sum(if(courseid_id=41,teachers,0)) as sk
from (SELECT
a.instituteid_id,a.remotecenterid_id,b.courseid_id,count(personid_id)
teachers FROM `SIP_t10kt_approvedinstitute` a,SIP_courselevelusers b
where  a.instituteid_id=b.instituteid_id and roleid = 5 and
a.remotecenterid_id >1000 group by
a.instituteid_id,a.remotecenterid_id,b.courseid_id ) query,
SIP_t10kt_institute b WHERE instituteid_id=b.instituteid GROUP BY
b.institutename,remotecenterid_id ORDER BY remotecenterid_id,ee
DESC,hs DESC,sk DESC) query  CROSS JOIN (SELECT @cnt := 0) AS dummy
union all
select "Total",
"",count(distinct remotecenterid_id),sum(if(courseid_id=43,teachers,0)) as hs ,
sum(if(courseid_id=45,teachers,0)) as ee,
sum(if(courseid_id=41,teachers,0)) as sk
from (SELECT
a.instituteid_id,a.remotecenterid_id,b.courseid_id,count(personid_id)
teachers FROM `SIP_t10kt_approvedinstitute` a,SIP_courselevelusers b
where  a.instituteid_id=b.instituteid_id and roleid = 5 and
a.remotecenterid_id >1000 group by
a.instituteid_id,a.remotecenterid_id,b.courseid_id ) query,
SIP_t10kt_institute b WHERE instituteid_id=b.instituteid' WHERE `SIP_reports`.`reportid` = '7';


UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS id," " as A,"HS791xA16" as''B'',"EE210xA16" as ''C'' ,"SKANI101xA" as ''D''
 union all select (@cnt := @cnt + 1) AS id,
"No. of Institutes" a, query.hs,query.ee,query.sk 
from
 (SELECT sum( if( courseid_id =42, 1, 0 ) ) as hs,
         sum( if( courseid_id =45, 1, 0 ) ) as ee,
         sum( if( courseid_id =41, 1, 0 ) ) as sk
FROM (SELECT a.instituteid_id, a.remotecenterid_id, b.courseid_id, count( personid_id ) teachers
FROM `SIP_t10kt_approvedinstitute` a, SIP_courselevelusers b
WHERE a.instituteid_id = b.instituteid_id AND roleid =5
AND a.remotecenterid_id >1000
GROUP BY a.instituteid_id, a.remotecenterid_id, b.courseid_id )q)
query CROSS JOIN (SELECT @cnt := 0) AS dummy;
' WHERE `SIP_reports`.`reportid` = '8';









