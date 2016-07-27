update SIP_courselevelusers set roleid=-1*roleid where  personid_id = (select id from SIP_personinformation where email ='pankajksa@nitrkl.ac.in');
update SIP_courselevelusers set roleid=-1*roleid where  personid_id = (select id from SIP_personinformation where email ='nareshkumarnathan@gmail.com');
update SIP_courselevelusers set roleid=-1*roleid where  personid_id = (select id from SIP_personinformation where email ='satish.salunkhe@nmims.edu');
update SIP_courselevelusers set roleid=-1*roleid where  personid_id = (select id from SIP_personinformation where email ='nidhi.sharda@nmi.edu');
UPDATE SIP_studentdetails SET teacherid_id = '9' WHERE SIP_studentdetails.id =12403;
UPDATE SIP_studentdetails SET teacherid_id = '8' WHERE SIP_studentdetails.id =17164;
