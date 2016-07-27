update SIP_courselevelusers set roleid=-1*roleid where  personid_id = (select id from SIP_personinformation where email ='gagan.v.sati@gmail.com');
