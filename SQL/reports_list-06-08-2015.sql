UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select  0 AS id,"Course" as "A","Total" as "B","Enrolled" as "C","Unenrolled" as "D" union all SELECT ( @cnt := @cnt +1 ) AS id, query.Course_Id,query.Total,query.enrolled,query.unenrolled FROM( SELECT edxapp.student_courseenrollment.course_id AS Course_Id, sum(if(edxapp.student_courseenrollment.is_active=1,1,0))  as "enrolled" , sum(if(edxapp.student_courseenrollment.is_active=0,1,0)) as "unenrolled",count(*) as "Total"  FROM edxapp.student_courseenrollment  WHERE  edxapp.student_courseenrollment.course_id in (''IITBombayX/ME209xA15/2015_T1'',''IITBombayX/EE210.1xA15/2015_T1'',''IITBombayX/CS101.1xA15/2015_T1'')   group by edxapp.student_courseenrollment.course_id order by Total) AS query CROSS JOIN ( SELECT @cnt :=0 ) AS dummy 
' WHERE `SIP_reports`.`reportid` = '4';


UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS id,"Module_id" as "A","Access_Count" as "B" union all SELECT (@cnt := @cnt +1) AS id, query.Module_id,query.Access_Count FROM(SELECT edxapp.courseware_studentmodule.module_id AS Module_id,count(*) AS Access_Count FROM edxapp.courseware_studentmodule WHERE edxapp.courseware_studentmodule.module_type = ''course'' AND edxapp.courseware_studentmodule.module_id in  ( "i4x://IITBombayX/CS101.1xA15/course/2015_T1",  "i4x://IITBombayX/ME209xA15/course/2015_T1",  "i4x://IITBombayX/EE210.1xA15/course/2015_T1")  group by module_id order by Access_Count DESC) AS query CROSS JOIN (SELECT @cnt :=0) AS dummy' WHERE `SIP_reports`.`reportid` = '5';


UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS id,"Course" as''A'',"RCID" as''B'' ,"Institute Name" as ''C'' ,"Email" as''D'',"Name" as ''E'' ,"#Students" as ''F'' union all  select (@cnt := @cnt + 1) AS id,query.course,query.rcid,query.institutename,query.email,query.name,query.student from  (SELECT  e.course, ai.remotecenterid_id rcid ,i.institutename,p.email,concat(p.firstname," ", p.lastname) name ,count(*) student FROM `SIP_studentdetails` s, SIP_courselevelusers c,SIP_edxcourses e,SIP_t10kt_institute i, SIP_personinformation p,SIP_t10kt_approvedinstitute  ai where s.teacherid_id=c.id and c.personid_id=p.id and p.instituteid_id =i.instituteid and  p.instituteid_id !=0 and  e.id=c.courseid_id and  p.instituteid_id= ai.instituteid_id group by c.courseid_id, e.course, p.email,p.firstname, p.lastname,p.instituteid_id ,i.institutename,ai.remotecenterid_id order by student DESC ) query  CROSS JOIN (SELECT @cnt := 0) AS dummy;' WHERE `SIP_reports`.`reportid` = '6';

INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`) VALUES ('7', '0', 'select 0 AS id,"Institiute Name" as''A'',"RCID" as''B'' ,"CS101.1x" as ''C'' ,"ME209.1x" as''D'',"EE210.1x" as ''E'' union all  select (@cnt := @cnt + 1) AS id,query.institutename,query.remotecenterid_id,query.cs,query.me,query.ee from (select b.institutename,remotecenterid_id,sum(if(courseid_id=6,teachers,0)) as cs ,sum(if(courseid_id=7,teachers,0)) as me,sum(if(courseid_id=8,teachers,0)) as ee  from (SELECT a.instituteid_id,a.remotecenterid_id,b.courseid_id,count(personid_id) teachers FROM `SIP_t10kt_approvedinstitute` a,SIP_courselevelusers b where  a.instituteid_id=b.instituteid_id and roleid = 5 and a.instituteid_id >1000 group by a.instituteid_id,a.remotecenterid_id,b.courseid_id ) query, SIP_t10kt_institute b WHERE instituteid_id=b.instituteid GROUP BY b.institutename,remotecenterid_id ORDER BY cs DESC,me DESC,ee DESC) query  CROSS JOIN (SELECT @cnt := 0) AS dummy;', 'Teachers'' Summary Report', 'List of number of teachers participating in course institute wise.', '5');


INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`) VALUES ('8', '0', 'select 0 AS id,"CS101.1x" as''A'',"ME209.1x" as''B'' ,"EE210.1x" as ''C'' union all  select (@cnt := @cnt + 1) AS id,query.cs,query.me,query.ee from (SELECT sum( if( courseid_id =6, 1, 0 ) ) as cs, sum( if( courseid_id =7, 1, 0 ) ) as me, sum( if( courseid_id =8, 1, 0 ) ) as ee FROM (SELECT a.instituteid_id, a.remotecenterid_id, b.courseid_id, count( personid_id ) teachers FROM `SIP_t10kt_approvedinstitute` a, SIP_courselevelusers b WHERE a.instituteid_id = b.instituteid_id AND roleid =5 AND a.instituteid_id >1000 GROUP BY a.instituteid_id, a.remotecenterid_id, b.courseid_id )q)query  CROSS JOIN (SELECT @cnt := 0) AS dummy;', 'Courses Participation Report', 'Participation Count in each course', '2');


INSERT INTO `SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`) VALUES ('9', '0', '
select 0 AS id,"Male" as''A'',"Female" as''B'' ,"Others" as ''C'' ,"No_Data" as''D'' union all  select (@cnt := @cnt + 1) AS id,query.Male,query.Female ,query.Others ,query.No_Data  from (SELECT course_id,
sum(if(gender=''Male'',1,0))  as Male ,
sum(if(gender=''Female'',1,0))  as Female,
sum(if(gender=''Others'',1,0))  as Others,
sum(if(gender=''ND'',1,0))  as No_Data
from
(SELECT a.user_id, a.course_id, if( b.gender = ''m'', "Male", if( b.gender = ''f'', "Female", if( b.gender = ''o'', "Others", "ND" ) ) ) Gender
FROM edxapp.student_courseenrollment a, edxapp.auth_userprofile b
WHERE a.course_id
IN (
''IITBombayX/ME209xA15/2015_T1'', ''IITBombayX/EE210.1xA15/2015_T1'', ''IITBombayX/CS101.1xA15/2015_T1''
)
AND a.user_id = b.user_id
)  users group by course_id)query  CROSS JOIN (SELECT @cnt := 0) AS dummy;', 'Enrollment based on Gender', 'Enrollment count  based on Gender', '4');


INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`) VALUES ('10', '0', 'select 0 AS id,"course id" as A,"Under 18" as''B'',"18-30" as''C'' ,"30-60" as ''D'' ,"Above 60" as''E'',"ND" as ''F'' union all  select (@cnt := @cnt + 1) AS id,query.course_id,query.p,query.q,query.r,query.s,query.t from (SELECT course_id,sum(if(age_group ="under 18",1,0)) p,
sum(if(age_group ="18-30",1,0)) q,
sum(if(age_group ="30-60",1,0)) r,
sum(if(age_group ="above 60",1,0)) s,
sum(if(age_group ="ND",1,0)) t
from
(SELECT a.user_id, a.course_id, if( year_of_birth <1955, "above 60", if( year_of_birth <1985, "30-60", if( year_of_birth <1997, "18-30", if( year_of_birth <2015, "under 18", "ND" ) ) ) ) "age_group"
FROM edxapp.student_courseenrollment a, edxapp.auth_userprofile b
WHERE a.course_id
IN (
''IITBombayX/ME209xA15/2015_T1'', ''IITBombayX/EE210.1xA15/2015_T1'', ''IITBombayX/CS101.1xA15/2015_T1''
)
AND a.user_id = b.user_id
)  users group by course_id)query  CROSS JOIN (SELECT @cnt := 0) AS dummy;
', 'Enrollment based on age group', 'Enrollment based on age group', '6');



INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`) VALUES ('11', '0', 'select 0 AS id,"course_id" as A,"Associates" as "B","Bachelors" as "C","Masters" as "M","Doctrate" as "D","School" as "E","Others" as "F","No_Data" as "G" union all select (@cnt:= @cnt+1) as id,query.course_id,query.p,query.q,query.r,query.s,query.t,query.u,query.v from
(SELECT course_id,
sum(if(level_of_education=''a'',1,0)) p,
sum(if(level_of_education=''b'',1,0)) q ,
sum(if(level_of_education=''m'',1,0)) r,
sum(if(level_of_education=''p'',1,0)) s ,
sum(if(level_of_education in (''el'',''hs'',''jhs''),1,0)) t,
sum(if(level_of_education=''other'',1,0)) u ,
sum(if(level_of_education not in (''el'',''hs'',''jhs'',''a'',''b'',''m'',''p'',''other''),1,0)) v
from
(SELECT a.user_id, a.course_id,level_of_education 
FROM edxapp.student_courseenrollment a, edxapp.auth_userprofile b
WHERE a.course_id
IN (
''IITBombayX/ME209xA15/2015_T1'', ''IITBombayX/EE210.1xA15/2015_T1'', ''IITBombayX/CS101.1xA15/2015_T1''
)
AND a.user_id = b.user_id
)  users group by course_id)query  CROSS JOIN (SELECT @cnt := 0) AS dummy;', 'Enrollment based on levelof education', 'Enrollment based on levelof education', '8');


INSERT INTO `iitbxblended`.`SIP_reports` (`reportid`, `usertype`, `sqlquery`, `report_title`, `comments`, `num_cols`) VALUES ('12', '0', 'select 0 AS id,"course_id" as "A","cities" as "B","states" as "C", "Districts" as "D","Disclosed AdharId" as "E" union all select (@cnt:=@cnt+1) as id, query.course_id,query.p,query.r,query.s,query.t from ( SELECT course_id,
count(distinct City)  as p,
count(distinct State)  as r,
count(distinct pincode)  as s ,count(distinct aadhar_id) as t
from
(SELECT a.user_id, a.course_id, e.name "City", d.name "State", c.pincode, c.aadhar_id
FROM edxapp.student_courseenrollment a, edxapp.auth_userprofile b, edxapp.student_mooc_person c, edxapp.student_mooc_state d, edxapp.student_mooc_city e
WHERE a.course_id
IN (
''IITBombayX/ME209xA15/2015_T1'', ''IITBombayX/EE210.1xA15/2015_T1'', ''IITBombayX/CS101.1xA15/2015_T1''
)
AND a.user_id = b.user_id
AND a.user_id = c.user_id
AND c.state_id = d.id
AND c.city_id = e.id
)  users group by course_id)query CROSS JOIN (SELECT @cnt :=0) AS dummy;', 'Enrollment based geographic areas', 'Enrollment based geographic areas', '5');

