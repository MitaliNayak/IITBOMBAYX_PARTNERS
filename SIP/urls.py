from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^$', 'SIP.views.sessionlogin',name='course'),
     url(r'^get_multi_roles/', 'SIP.views.get_multi_roles',name='get_multi_roles'),
     url(r'^set_single_role/(?P<role>[0-9])/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<cid>[0-9]{1,40})$', 'SIP.views.set_single_role',name='set_single_role'),	
    url(r'^teacher/$','SIP.views.teacherhome'),
    url(r'^studentdetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+)/$','SIP.views.studentdetails'),
	url(r'^updatestudent/(?P<pid>[0-9]+)/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<t_id>[0-9]+)/$','SIP.views.Update'),
    url(r'^movestudents$','SIP.views.movestudents'),
    url(r'^downloadcsv1/(?P<course>[a-zA-Z0-9./-]+)/(?P<id>[0-9]+)/$','SIP.views.downloadcsv',name='downloadcsv'),
    url(r'^upload/(?P<code>[0-9])/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'SIP.views.upload'),
    url(r'^upload/uploaded/', 'SIP.views.uploaded'),
    url(r'^downloadcsv/(?P<code>[0-9])/$', 'SIP.views.output_csv'),
	url(r'^unenroll/(?P<pid>[0-9-]+)/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<t_id>[0-9]+)/$','SIP.views.unenrollstudent'),
	url(r'^report/(?P<option>[a-z]+)/(?P<course>[\w{}\.\-\/]{1,40})/$','SIP.views.report'),
   	url(r'^teacherlist/(?P<courseid>[\w{}\.\-\/]{1,40})/$','SIP.views.teacherlist'),
    url(r'^ccourses/',views.ccourse, name='ccourses'),
    url(r'^blendedadmin_home/','SIP.views.blendedadmin_home',name='blendedadmin_home'),
    url(r'^blendedadmin/(?P<report_id>[0-9./-]+)/$','SIP.views.blendedadmin',name='blendedadmin'),
	
 

]
