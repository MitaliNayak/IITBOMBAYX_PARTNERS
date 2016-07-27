ALTER TABLE `SIP_reports` ADD `category` VARCHAR( 30 ) NULL ,
ADD `rel_rep_id` INT NULL DEFAULT NULL ;


UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS id,"Email" as''A'',"Full Name" as''B'' ,"Institute Name" as''C'' ,"Course" as''D'',"IITBX Login" as''E'' ,"BMW Login" as ''F'' union all select (@cnt := @cnt + 1) AS id,query.Email,query.Full_Name,query.Institute_Name,query.Course,query.IITBX_Login,query.BMS_Login  from (SELECT p.email as Email, concat(p.firstname,'' '',p.lastname) as Full_Name, i.institutename as Institute_Name,ec.coursename as Course,if(a.email is null, "Does Not Exists","Exists") "IITBX_Login",if(l.status=0,"Does Not Activated","Activated") "BMS_Login" from SIP_personinformation p LEFT OUTER JOIN edxapp.auth_user a on lower(a.email)=lower(p.email),SIP_courselevelusers c,SIP_edxcourses ec, SIP_t10kt_institute i ,SIP_userlogin l,auth_user au where c.roleid=5 and c.courseid_id=ec.id and c.personid_id=p.id and p.instituteid_id=i.instituteid and l.user_id=au.id and p.email=au.email and i.instituteid != 0 order by i.institutename,ec.coursename) as query CROSS JOIN (SELECT @cnt := 0) AS dummy; ', `report_title` = 'Status Report of Teachers', `category` = 'Status Report' WHERE `SIP_reports`.`reportid` = '1';

UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS id,"Email" as "A","Full Name" as "B","Institute Name" as "C","BMW Login" as "D" union all SELECT ( @cnt := @cnt +1 ) AS id, query.Email, query.Full_Name, query.Institute_Name, query.BMS_Login FROM ( SELECT p.email AS Email, concat( p.firstname, '' '',p.lastname ) AS Full_Name, i.institutename AS Institute_Name, if( l.status =0, "Not Activated", "Activated" ) "BMS_Login" FROM SIP_personinformation p LEFT OUTER JOIN edxapp.auth_user a ON a.email = p.email, SIP_institutelevelusers c, SIP_t10kt_institute i, SIP_userlogin l, auth_user au WHERE c.roleid = 2 AND c.personid_id = p.id AND p.instituteid_id = i.instituteid AND l.user_id = au.id AND lower(p.email) = lower(au.email) and i.instituteid != 0 order by i.institutename ) AS query CROSS JOIN ( SELECT @cnt :=0 ) AS dummy', `report_title` = 'Status Report of Institute Heads', `category` = 'Status Report' WHERE `SIP_reports`.`reportid` = '2';

UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select  0 AS id,"Email" as "A","Full Name" as "B","Institute Name" as "C","BMW Login" as "D"
union all
SELECT (
@cnt := @cnt +1
) AS id, query.Email, query.Full_Name, query.Institute_Name, query.BMS_Login
FROM (

SELECT p.email AS Email, concat( p.firstname,'' '' ,p.lastname ) AS Full_Name, i.institutename AS Institute_Name, if( l.status =0, "Not Activated", "Activated" ) "BMS_Login"
FROM SIP_personinformation p
LEFT OUTER JOIN edxapp.auth_user a ON a.email = p.email, SIP_institutelevelusers c, SIP_t10kt_institute i, SIP_userlogin l, auth_user au
WHERE c.roleid =3
AND c.personid_id = p.id
AND p.instituteid_id = i.instituteid
AND l.user_id = au.id
AND lower(p.email) = lower(au.email)
and i.instituteid != 0 order by i.institutename
) AS query
CROSS JOIN (

SELECT @cnt :=0
) AS dummy', `report_title` = 'Status Report of Program Coordinators', `category` = 'Status Report' WHERE `SIP_reports`.`reportid` = '3';


UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'MOOCS Participation Summary Report', `comments` = 'MOOCS Participation Summary Report', `category` = 'MOOCS Users' WHERE `SIP_reports`.`reportid` = '4';


UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'MOOCS Participants Course Access Summary Report',
`category` = 'MOOCS Users' WHERE `SIP_reports`.`reportid` = '5';

UPDATE `iitbxblended`.`SIP_reports` SET `sqlquery` = 'select 0 AS id,"Course" as "A","Access Count" as "B" union all SELECT (@cnt := @cnt +1) AS id, query.course_id,query.Access_Count FROM(SELECT edxapp.courseware_studentmodule.course_id AS course_id,count(*) AS Access_Count FROM edxapp.courseware_studentmodule WHERE edxapp.courseware_studentmodule.module_type = ''course'' AND edxapp.courseware_studentmodule.module_id in  ( "i4x://IITBombayX/CS101.1xA15/course/2015_T1",  "i4x://IITBombayX/ME209xA15/course/2015_T1",  "i4x://IITBombayX/EE210.1xA15/course/2015_T1")  group by module_id order by Access_Count DESC) AS query CROSS JOIN (SELECT @cnt :=0) AS dummy
' WHERE `SIP_reports`.`reportid` = '5';

UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'Institute-wise:Teachers'' Participation Report',
`category` = 'Institute' WHERE `SIP_reports`.`reportid` = '7';

UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'Institute wise: Course Participation Report',
`category` = 'Institute' WHERE `SIP_reports`.`reportid` = '8';


UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'Teacher wise: Students'' Upload',
`category` = 'Students' WHERE `SIP_reports`.`reportid` = '6';

UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'MOOCS Participation: Gender-wise User Profile',
`category` = 'MOOCS Users' WHERE `SIP_reports`.`reportid` = '9';

UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'MOOCS Users: Age-group wise User Profile',
`category` = 'MOOCS Users' WHERE `SIP_reports`.`reportid` = '10';

UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'MOOCs Users: Level of Education',
`category` = 'MOOCS Users' WHERE `SIP_reports`.`reportid` = '11';

UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'MOOCs Users :Geographical Diversity of Users',
`category` = 'MOOCS Users' WHERE `SIP_reports`.`reportid` = '12';

UPDATE `iitbxblended`.`SIP_reports` SET `category` = 'Activity' WHERE `SIP_reports`.`reportid` = '13';

UPDATE `iitbxblended`.`SIP_reports` SET `report_title` = 'Institute wise:Student''s Participation Summary Report',
`category` = 'Institute' WHERE `SIP_reports`.`reportid` = '14';

UPDATE `iitbxblended`.`SIP_reports` SET `category` = 'Activity' WHERE `SIP_reports`.`reportid` = '6';
