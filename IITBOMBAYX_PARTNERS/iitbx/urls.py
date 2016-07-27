from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^studentprofile/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'iitbx.views.studentprofile',name='studentprofile'),
     url(r'^postalinfo/$', 'iitbx.views.postalinfo',name='postalinfo'),
     url(r'^weeklyreport/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'iitbx.views.weeklyreport',name='weeklyreport'),
     url(r'^problemwiseevaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.problemwiseevaluation',name='problemwiseevaluation'),
     url(r'^problemwisedata$','iitbx.views.problemwisedata',name='problemwisedata'),
     url(r'^problemwisedetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.problemwisedetails',name='problemwisedetails'),
     url(r'^problemwisedetailsreport/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.problemwisedetailsreport',name='problemwisedetailsreport'),
     url(r'^problemwisereport/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.problemwisereport',name='problemwisereport'),  
     url(r'^problem_sequential','iitbx.views.problem_sequential',name='problem_sequential'),  
     url(r'^problem_unittype','iitbx.views.problem_unittype',name='problem_unittype'), 
     url(r'^assignmentdetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.assignmentdetails',name='assignmentdetails'),
     url(r'^assignmentmultipleoptions/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<aid>[0-9]+|-[0-9])/(?P<part>[0-9]+|-[0-9])/$','iitbx.views.assignmentmultipleoptions',name='assignmentmultipleoptions'), 
      url(r'^assignmentmarksdata/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.assignmentmarksdata',name='assignmentmarksdata'), 
    url(r'^assignmentmarksdetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.assignmentmarksdetails',name='assignmentmarksdetails'),   
    url(r'^courseenrollment/$', 'iitbx.views.courseenrollment',name='courseenrollment'),  
    url(r'^gradesumary/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.gradesumary',name='gradesumary'),  
    url(r'^nongradedevaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.nongradedevaluation',name='nongradedevaluation'),   
    url(r'^nongradedassignmentsummary/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.nongradedassignmentsummary',name='nongradedassignmentsummary'), 
    url(r'^nongradedanswers/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<aid>[0-9]+|-[0-9])/(?P<pid>[0-9]+|-[0-9])/(?P<score>\d+\.\d+|[0-9]+)/$','iitbx.views.nongradedanswers',name='nongradedanswers'),
    url(r'^nongradedmultipleoptions/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<aid>[0-9]+|-[0-9])/(?P<part>[0-9]+|-[0-9])/$','iitbx.views.nongradedmultipleoptions',name='nongradedmultipleoptions'), 
    url(r'^nongradedproblemwiseevaluation/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.nongradedproblemwiseevaluation',name='nongradedproblemwiseevaluation'),
    url(r'^nongradedproblemwisedata$','iitbx.views.nongradedproblemwisedata',name='nongradedproblemwisedata'),
    url(r'^nongradedproblemwisedetails/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.nongradedproblemwisedetails',name='nongradedproblemwisedetails'),
     url(r'^discussionforumdata/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.discussionforumdata',name='discussionforumdata'),
    #######course_module structure###############
    url(r'^course_chapter/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.course_chapter',name='course_chapter'),
    url(r'^chapter_sequential','iitbx.views.chapter_sequential',name='chapter_sequential'),
    url(r'^sequential_unittype','iitbx.views.sequential_unittype',name='sequential_vertical'),
    url(r'^vertical_module','iitbx.views.vertical_module',name='vertical_module'),
    url(r'^display_type','iitbx.views.display_type',name='display_type'),
    url(r'^problem_compare','iitbx.views.problem_compare',name='problem_compare'),
    #######course_module structure############### 
    url(r'^closedcoursegrade/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'iitbx.views.closedcoursegrade',name='closedcoursegrade'),
    ########closed course grades from csv #######
    url(r'^closed_courses_grades_report/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.closed_courses_grades_report',name='closed_courses_grades'),
#######For comparing two problems############
    url(r'^problemwiseevaluation_comparision/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/(?P<evalflag>[0-9])/$','iitbx.views.problemwiseevaluation_comparision',name='problemwiseevaluation_comparision'),
    url(r'^problemcompare_report/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.problemcompare_report',name='problemcompare_report'),
    url(r'^certified_participant/$', 'iitbx.views.certified_participant',name='certified_participant'),
    url(r'^managerhome/$', 'iitbx.views.managerhome',name='managerhome'),
    url(r'^invited_participant/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.invited_participant',name='invited_participant'),
    url(r'^inviteduserlist/(?P<courseid>[\w{}\.\-\/]{1,40})/$','iitbx.views.inviteduserlist',name='inviteduserlist'),
    url(r'^problemcomparegraph/(?P<courseid>[\w{}\.\-\/]{1,40})/(?P<pid>[0-9]+|-[0-9])/$','iitbx.views.problemcomparegraph',name='problemcomparegraph'),
    ######For discusson_forum########
    url(r'^discussionforum_user_participation_count/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'iitbx.views.discussionforum_user_participation_count',name='discussionforum_user_participation_count'),
    url(r'^discussionforum_user_date_wise_count/(?P<courseid>[\w{}\.\-\/]{1,40})/$', 'iitbx.views.discussionforum_user_date_wise_count',name='discussionforum_user_date_wise_count'),
    #################################
 ]
