update SIP_errorcontent
set error_message="Your old password did not match. Please enter again."
where id=45;

update SIP_errorcontent
set error_message="Password didn't match. Please enter again."
where id=46;

update SIP_errorcontent
set error_message="Your old and new password can't be same. Please enter again."
where id=49;
