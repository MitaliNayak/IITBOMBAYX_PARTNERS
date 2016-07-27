from iitbx_settings import *

def dbedxapp_openconnection():
     cnxedxapp = MySQLdb.connect(user=user,passwd=passwd,host=mysql_host,db=mysql_schema)
     return cnxedxapp


@transaction.atomic
def email_change():
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error  %s,(%s) -Establishing mysql connection"%(e.message,str(type(e)))
      return [-1]
    enrollment_count=0
    mysql_csr.execute(''' select a.id,a.email as "new_email",a.username,i.email as "old_email" from iitbxblended.SIP_iitbx_auth_user i ,edxapp.auth_user a where a.username=i.username and i.email != a.email''')
    auth_users=mysql_csr.fetchall()
    for auth_user in auth_users:
       try:
           iitbx_auth_user_obj=iitbx_auth_user.objects.get(edxuserid=auth_user[0],username=auth_user[2],email=auth_user[3])
           iitbx_auth_user_obj.email=auth_user[1]
           enrollment_count=enrollment_count+1
           iitbx_auth_user_obj.save()
       except Exception as e:
           print "No changes detected",str(e.message),e.__class__.__name__
    return enrollment_count


def main(argv):

        changed_emails_count=0
        changed_emails_count=email_change()   
        print "The number of email ids changed ",changed_emails_count
        

if __name__ == "__main__":
    main(sys.argv[1:])
