from iitbx_settings import *

question_types=["<choiceresponse>","<optionresponse>","<multiplechoiceresponse>","<numericalresponse ","<stringresponse ","<drag_and_drop_input","<imageresponse","<formularesponse","<customresponse","<jsmeresponse>","<schematicresponse>"]
def init():
       global prefix_url
       prefix_url="https://iitbombayx.in/c4x/IITBombayX/"
       global infix_url 
       infix_url="/asset/"
  

def dbedxapp_openconnection():
     cnxedxapp = MySQLdb.connect(user=user,passwd=passwd,host=mysql_host,db=mysql_schema)
     return cnxedxapp

def mongo_openconnection():
     global client
     client = MongoClient(mongodb)
     global db 
     db= client.edxapp
     global collection
     collection = db.modulestore
     return collection

@transaction.atomic
def delete_grade_information(cid):
       gradepolicy.objects.filter(courseid=cid).delete()
       gradescriteria.objects.filter(courseid=cid).delete()


@transaction.atomic

def get_course_detail(csr,org,longname):
     collection=mongo_openconnection()
     curtime = datetime.now()
     course_id=""
     blended = 0
     num_days=1000
     if str(longname) in courses:
        blended=1
     else:
        blended=0
     for course_det in collection.find({"_id.course":csr,"_id.org":org,"_id.category":"course"},{"metadata.start":1,"metadata.end":1,"metadata.enrollment_start":1,"metadata.enrollment_end":1,"metadata.course_image":1,"metadata.display_name":1,"definition.data.grading_policy":1}):         
           course_tag=course_det["_id"]["tag"]
           course_org= course_det["_id"]["org"]
           course= course_det["_id"]["course"]
           course_name= course_det["_id"]["name"]
           course_id =course_org+'/'+course+'/'+course_name
           course_disp_name=course_det["metadata"]["display_name"]
           try:
                   temp=course_det["metadata"]["end"]
                   course_end= datetime.strptime(str(temp),'%Y-%m-%dT%S:%M:%HZ')
           except:
                   course_end=date_format("9999-12-31 00:00:00","%Y-%m-%d %H:%M:%S")
          
           try:
                   course_enroll_end=course_det["metadata"]["enrollment_end"]
                   course_enroll_end=datetime.strptime(str(course_enrol_end), '%Y-%m-%dT%S:%M:%HZ')

           except:
                   course_enroll_end=course_end
           try: 
                   course_start=course_det["metadata"]["start"]
                   course_start=datetime.strptime(str(course_start), '%Y-%m-%dT%S:%M:%HZ')
           except:
                   course_start= course_end + timedelta(days=-1)
           try: 
                   course_enroll_start=course_det["metadata"]["enrollment_start"]
                   course_enroll_start=datetime.strptime(str(course_enroll_start), '%Y-%m-%dT%S:%M:%HZ')
           except:
                   course_enroll_start= course_end + timedelta(days=-1)      

           ahead_date=course_end+ timedelta(days=num_days)
           delta= ahead_date-course_end
           if  ( ahead_date-curtime ).days > 0:
                try:
                   course_image=course_det["metadata"]["course_image"]
                except:
                   course_image="No Image"
                image_url=prefix_url+course+infix_url+course_image
                try:  # if course is there update it
                      course_obj=edxcourses.objects.get(courseid=course_id)
                      courseid=course_obj.id
                      course_obj.tag=course_tag
                      course_obj.org=course_org
                      course_obj.course=course
                      course_obj.name=str(course_name)
                      course_obj.courseid=course_id
                      course_obj.coursename=course_disp_name
                      course_obj.enrollstart=course_enroll_start      
                      course_obj.enrollend=course_enroll_end
                      course_obj.coursestart=course_start
                      course_obj.courseend=course_end
                      course_obj.image=image_url
                      course_obj.blended_mode=blended
                      try:
                        course_obj.save()
                      except Exception as e:
                         print "Error %s,(%s) - Insert on %s. Contact Software team."%(e.message,str(type(e)),course_id) 
                      try:
                         delete_grade_information(course_id)
                         if (get_grade_policy_criteria(course_obj) == -1) :
                             print "Issue in getting grade policy and criteria"
                      except Exception as e:
                          print "Error %s,(%s) - Update on %s. Contact Software team."%(e.message,str(type(e)),course_id)
                          return "-1"
                except Exception as e: # else insert the courses 
                    course_obj=edxcourses(tag=course_tag, org=course_org, course=course, name=course_name, courseid=course_id, coursename=course_disp_name, enrollstart=course_enroll_start, enrollend=course_enroll_end, coursestart=course_start, courseend=course_end,image=image_url,blended_mode=blended)
                    course_obj.save()
                    if( get_grade_policy_criteria(course_obj) == -1):
                        print "Issue in getting grade policy and criteria"
                try: 
                       if (insert_admin_courseleveluser(course_id) == -1):
                          print "Issue in inserting admin courseleveluser"
                except Exception as e:
                       print "Error %s,(%s) insert of course level users on %s. Contact Software team."%(e.message,str(type(e)),course_id)
                       return "-1"
     return course_id



@transaction.atomic
def get_grade_policy_criteria(course_obj):
  
  collection=mongo_openconnection()
 
  course=course_obj.courseid.split('/')[1]
  try:
     for course_det in collection.find({"$and": [{"_id.category":"course"},{"_id.course":course_obj.course },{"_id.org":course_obj.org}]}):
        course_grading_policy= course_det["definition"]["data"]["grading_policy"]["GRADER"]
        for coursepolicy in course_grading_policy :
            min_count=coursepolicy["min_count"]
            weight=coursepolicy["weight"]
            ptype=coursepolicy["type"]
            drop_count=coursepolicy["drop_count"]
            short_label=coursepolicy["short_label"]
            grade_policy_obj=gradepolicy(courseid=course_obj, min_count=min_count, weight=weight ,type=ptype, drop_count=drop_count, short_label=short_label)
            grade_policy_obj.save()

            cutoffs=course_det["definition"]["data"]["grading_policy"]["GRADE_CUTOFFS"]
            for key,value in cutoffs.iteritems():
                grade_criteria_obj=gradescriteria(courseid=course_obj,grade=key,cutoffs=value)
                grade_criteria_obj.save()

     return 0
  except Exception as e:
     print "Error %s - Fetching grade criteria and Policy from mongodb for course %s "%(e.message,course_obj.courseid)
     return -1

@transaction.atomic
def insert_admin_courseleveluser(courseid):
    try:
      try:
         course_obj=edxcourses.objects.get(courseid=courseid)
      except Exception as e:
         print "Error %s,(%s) - Fetching course object for " %(e.message,str(type(e)),courseid)
         return -1
      try:
         instituteid=T10KT_Institute.objects.get(instituteid=0)
      except Exception as e:
         print "Error %s,(%s) -Fetching Institute object for " %(e.message,str(type(e)),courseid)
         return -1
      
      if Courselevelusers.objects.filter(personid_id=1,instituteid=instituteid,courseid_id=course_obj.id,roleid=5).exists():
         pass # No modification required for courselevelusers
      else:   #insert default teacher with personid=1 and instituteid=0 in courselevelusers table
        person_obj=Personinformation.objects.get(id=1)
        course_level_obj=Courselevelusers(personid=person_obj,instituteid=instituteid,courseid=course_obj,roleid=5,startdate="2005-01-01",enddate="4712-12-31")
        course_level_obj.save()
        return 0
    except Exception as e:
     print "Error  %s,(%s) - Insert of courseleveluser for " %(e.message,str(type(e)),courseid)
     return -1

@transaction.atomic    
def insert_modlist(disnm,motype,moid,rel_id,sort1,visible_to_staff_only,graded,long_name,weight1, count,release_date,due_date,cid,gradetype):
    
    try:
       
       mod_obj = course_modlist.objects.get(long_name=long_name)
       mod_obj.display_name = disnm
       mod_obj.module_type = motype
       mod_obj.module_id = moid
       mod_obj.long_name=long_name 
       mod_obj.related_id = rel_id
       mod_obj.order=sort1
       
       mod_obj.visible_to_staff_only=visible_to_staff_only
       mod_obj.graded=graded
       mod_obj.maxmarks=weight1
       mod_obj.questions=count
       mod_obj.startdate=release_date
       mod_obj.duedate=due_date
       mod_obj.hasproblems=0
       mod_obj.course=cid
       mod_obj.gradetype=gradetype
       mod_obj.save()
       return mod_obj.id
    except Exception as e:
       coursemod = course_modlist(display_name=disnm,module_type=motype,module_id=moid, related_id=rel_id,order=sort1, visible_to_staff_only=visible_to_staff_only, graded=graded, long_name=long_name, maxmarks=weight1, questions=count, startdate=release_date, duedate=due_date,hasproblems=0,course=cid,gradetype=gradetype)
       coursemod.save()
       return coursemod.id
 

@transaction.atomic      
def open_module(csr,org,csr_id,mlist,sortorder,start,end,cid):
  runtime = datetime.now()
  weight=0
  has_problem=0
  count=0
  totalques=0
  totalmarks=0
  dict={}
  count=0 
  weight=0
  childgraded=0
  for mod in mlist:
       mtype=mod.split('/')[4]
       mid=mod.split('/')[5]
       sortorder=sortorder+1
       for moddetails in collection.find({"_id.course":csr,"_id.org":org,"_id.category":mtype,"_id.name":mid},{"metadata.display_name":1,"definition.children":1,"_id.name":1, "metadata.graded":1,"metadata.visible_to_staff_only":1,"metadata.format":1,"metadata.start":1,"metadata.due":1,"definition.data.data":1,"metadata.weight":1}):
            try:
               dname=moddetails["metadata"]["display_name"].encode('utf-8')
            except:
               dname=""
            try:
               gradetype=moddetails["metadata"]["format"]
            except:
               gradetype=""
            try:
               
               due_date=moddetails["metadata"]["due"]
               due_date=datetime.strptime(str(due_date), '%Y-%m-%dT%S:%M:%HZ')
            except:
               due_date=end
            try:
               release_date= moddetails["metadata"]["start"]
               release_date=datetime.strptime(str(release_date), '%Y-%m-%dT%S:%M:%HZ')

            except Exception as e :
               release_date=start
            try:
               if moddetails['metadata']['visible_to_staff_only'] == True:
                      visible_to_staff_only=1 
            except:
               visible_to_staff_only=0 
            try:
               if moddetails['metadata']['graded'] ==True:
                  graded=1
            except:
               graded=0 
            if mtype == 'problem':
             has_problem=1
             try:
               definition_data=moddetails['definition']['data']['data'].encode('utf-8')
               try:
                   weight=moddetails["metadata"]["weight"]
                   count=1
               except Exception as e:
                   count=0;weight=0
                   for type in question_types:
                      weight+=definition_data.count(type)
                      count+=definition_data.count(type)
               totalques=totalques+1
               totalmarks=totalmarks+weight
             except Exception as ex:
                   print ex.__class__.__name__,str(ex.message)
            else:
                    weight=0
                    count =0
            insert_id=insert_modlist(dname,mtype,moddetails["_id"]["name"],csr_id,sortorder,visible_to_staff_only,graded,mod,weight, count,release_date,due_date,cid,gradetype) 
            try:
               clist=moddetails["definition"]["children"]
            except:
               clist=[]
            if len(clist) !=0:
                result=open_module(csr,org,insert_id,clist,sortorder,start,end,cid)
                
                sortorder=result['sortorder'] 
                # Update Verticals and  Sequentials that have graded problems with maxmarks and number of questions
  dict['graded']=graded
  dict['questions']=totalques
  dict['maxmarks']=totalmarks
  dict['sortorder']=sortorder
  dict['has_problem']=has_problem
  return dict        



def get_student_course_enrollment(course):
    try:
        edx_course_obj=edxcourses.objects.get(courseid=course)

    except Exception as e:
         print "Error  %s,(%s) - EdxCourse object for course %s doesnot exists"%(e.message,str(type(e)),course)
         return   [-1]
    try:
        person_info_obj=Personinformation.objects.get(id=1)
    except Exception as e:
         print "Error  %s,(%s) -Personinformation object for default user doesnot exist while finding enrollments for %s"%(e.message,str(type(e)),course)
         return  [-1] 
    try:   
            course_level_obj=Courselevelusers.objects.get(courseid=edx_course_obj,personid=person_info_obj)
    except Exception as e:
            print "Error  %s,(%s) -Courselevel default user is not present for %s "%(e.message,str(type(e)),course)
            return [-1]   
   
    try:
       cnx=dbedxapp_openconnection()
       mysql_csr=cnx.cursor()
    except Exception as e:
      print "Error  %s,(%s) -Establishing mysql connection"%(e.message,str(type(e)))
      return [-1]

    insertuser=0
    insertstudent=0
    updatestudent=0
    erroruser=0
    errorstudent=0    
    errorupdate=0
    runtime = datetime.now()
    
    # query to fetch new users enrolled to the course after the last run and insert into student details
    mysql_csr.execute("select b.user_id,a.username,a.email ,b.created,b.is_active,b.mode from auth_user a,student_courseenrollment b where  b.course_id= %s and b.user_id=a.id and not exists (select * from iitbxblended.SIP_studentdetails  s where s.courseid=b.course_id and b.user_id=s.edxuserid_id)",(course,))

    
    studrecords=mysql_csr.fetchall()
    for record in studrecords :
       try:
         auth_usr_obj=iitbx_auth_userobjects.get(edxuserid=record[0])
       except Exception as e:
           try:
             auth_usr_obj=iitbx_auth_user(edxuserid=record[0],username=record[1],email=record[2])
             auth_usr_obj.save()
             insertuser=insertuser+1 
           except Exception as e:
             print" Error  %s,(%s) -Inserting new user %s" %(e.message,str(type(e)),record) 
             erroruser=erroruser+1
             continue
       try:  
         stud_det=studentDetails(edxuserid=auth_usr_obj, courseid=course,edxcreatedon=record[3],edxis_active=record[4], edxmode=record[5],teacherid=course_level_obj,roll_no=0,last_update_on=runtime,last_updated_by=person_info_obj)
         stud_det.save()
         insertstudent=insertstudent+1
       except Exception as e: 
         print "Error  %s,(%s) -Inserting studentdetails %s "%(e.message,str(type(e)), record[0])
         errorstudent=errorstudent+1
         continue
      
    #query to fetch users who have changed their enrollment option
    mysql_csr.execute("select b.user_id,a.username,a.email ,b.created,b.is_active,b.mode from auth_user a,student_courseenrollment b where  b.course_id=%s and b.user_id=a.id and exists (select * from iitbxblended.SIP_studentdetails  s where s.courseid=b.course_id and b.user_id=s.edxuserid_id and b.is_active != s.edxis_active)",(course,))
    updated_student_enroll=mysql_csr.fetchall()     
    for record in updated_student_enroll :
       try:
          edxuser=iitbx_auth_user.objects.get(edxuserid=record[0])  
       except Exception as e:
          print" Error  %s,(%s) -Get existing user %s"%(e.message,str(type(e)), record) 
          erroruser=erroruser+1
          continue
       try: 
          update_stud_det=studentDetails.objects.get(edxuserid=edxuser,courseid=edx_course_obj.courseid)
          update_stud_det.edxis_active=record[4]
          update_stud_det.save()
          updatestudent=updatestudent+1 
       except Exception as e:
          print"Error  %s,(%s) -Updating studentdetails %s"%(e.message,str(type(e)), record)
          errorupdate=errorupdate+1
          continue 
    return [insertuser,insertstudent,updatestudent,erroruser,errorstudent,errorupdate]    


@transaction.atomic
def course_modules(course_id,org,cid):
    csr=edxcourses.objects.get(courseid=course_id).course
    result={}
    sortby=0   
    for csr_name in collection.find({"_id.course":csr,"_id.org":org,"_id.category":"course"} ,{"metadata.display_name":1, "metadata.visible_to_staff_only":1,"definition.children":1,"metadata.start":1,"metadata.end":1}): 
         sortby=sortby+1
         try:
            temp=csr_name["metadata"]["end"]
            course_end= datetime.strptime(str(temp),'%Y-%m-%dT%S:%M:%HZ')
         except:
            course_end=date_format("9999-12-31 00:00:00","%Y-%m-%d %H:%M:%S")
         try: 
                   course_start=csr_name["metadata"]["start"]
                   course_start=datetime.strptime(str(course_start), '%Y-%m-%dT%S:%M:%HZ')
         except:
                   course_start= course_end + timedelta(days=-1)
         csr_id=insert_modlist((csr_name["metadata"]["display_name"].encode('utf-8')),"course",course_id,"0",sortby,0,0,csr,0,0,course_start,course_end,cid,"")
         if len(csr_name["definition"]["children"]) !=0:
                result=open_module(csr,org,csr_id,csr_name["definition"]["children"],sortby,course_start,course_end,cid,)


@transaction.atomic
def print_courseware(csr,org,cid):
    evallist=[];qlist=[]
    grades_dict={}
    updated_problem_count=0
    inserted_problem_count=0
    error_updated_count=0
    dict={}
    evaluation_dict=collections.OrderedDict()
    
    try:
       course_obj=edxcourses.objects.get(id=cid)
    except:
       return -1
    gradedprob=0
    curtime = datetime.now() 
    ques_dict={} 
    modlist=course_modlist.objects.get(module_id= csr,course=cid,visible_to_staff_only=0)
    chlist=course_modlist.objects.filter(related_id= modlist.id,course=cid,visible_to_staff_only=0).order_by('order','related_id')
         
    for chap in chlist:
       ecount=0  # keep track on evaluation order
       seqlist=course_modlist.objects.filter(related_id= chap.id,course=cid,visible_to_staff_only=0).order_by('order','related_id') 
       for seq in seqlist:
           gradedprob=0 
           qlist=[]
           count=0
           heading = ["Rollno","Username","Email"]
           headlist=[]
           total=0
           not_attempt={}
           quest=[]
           q_dict={}
           tcount=0
           ecount=ecount+1
           na=[]  
           vertlist=course_modlist.objects.filter(related_id=seq.id,course=cid,visible_to_staff_only=0).order_by('order','related_id')
           evaluations_type={}
           grade_total=0
           for vert in vertlist:
            if (seq.graded==1) or (vert.graded==1) :
              pass               
            else:
              # Search for Non graded Problems
              problist=course_modlist.objects.filter(related_id=vert.id,course=cid,visible_to_staff_only=0,module_type='problem').order_by('order','related_id')
              for prob in problist:
                    gradedprob=-1
                    count=count+1 
                    total=total+prob.maxmarks                               
                    qlist.append([prob.maxmarks,prob.long_name,prob.display_name.encode('utf-8'),prob.questions])
                  
                    quest.append(prob.long_name)
                    q_dict[prob.long_name]=prob.maxmarks    
               
           if(gradedprob==1):
               pass
           elif gradedprob==-1:
             try:
                   evaluations_obj=gen_evaluations.objects.get(course=course_obj, sectionid=seq.module_id)
                   evaluations_obj.sec_name=seq.display_name.encode('utf-8')
                   evaluations_obj.release_date=seq.startdate
                   evaluations_obj.due_date=seq.duedate
                   total_marks=total
                   evaluations_obj.save()
             except Exception as e:
                   evaluations_obj=gen_evaluations(course=course_obj, sectionid=seq.module_id,sec_name=seq.display_name.encode('utf-8') ,type=seq.gradetype ,release_date=seq.startdate, due_date=seq.duedate, total_weight=0,grade_weight=0,total_marks=total)
                   evaluations_obj.save()
             for qid in qlist:
                    try:
                       problem_obj=gen_questions.objects.get( qid=qid[1])
                       problem_obj.q_weight=qid[0]
                       problem_obj.q_name=qid[2]
                       problem_obj.prob_count=qid[3]
                       problem_obj.save()
                       updated_problem_count=updated_problem_count+1
                    except Exception as e:
                       questions_obj=gen_questions(course=course_obj, eval=evaluations_obj, qid=str(qid[1]), q_name=qid[2], q_weight=qid[0], prob_count=qid[3])
                       questions_obj.save()  
            

   
@transaction.atomic    
def create_headings_practice_problems(course_obj,eval_dict):
      headers=["RollNumber","Username","Email Id","Progress <br>in %"] ;tooltip=[];grades_policy_dict=collections.OrderedDict()
      for keys,values in eval_dict.iteritems():
          #Creating dictinary of grade policy
          '''
          'Graded Quiz':{'min_count': '6', 'drop_count': '2', 'weight': 0.4}, 
          'Graded Programming Assignment': 'min_count': '4', 'drop_count': '1', 'weight': 0.3},
          'Final Exam': {'min_count': '1', 'drop_count': '0', 'weight': 0.3}
          '''
          grade_types=gradepolicy.objects.get(courseid=course_obj,type=keys)
          grade_policy_dict=grades_policy_dict.setdefault(keys,OrderedDict({}))
          min_count_dict=grade_policy_dict.setdefault("min_count",str(grade_types.min_count))
          drop_count_dict=grade_policy_dict.setdefault("drop_count",str(grade_types.drop_count))
          weight_dict=grade_policy_dict.setdefault("weight",grade_types.weight)
          for key,value in values.iteritems():
              total=value['total']
              # To get the order of individual sections
              key_order=(values.keys().index(key))+1
              headers.append(str(grade_types.short_label+str(key_order)+" "+str(total)+"Pts"))
              tt='TT'+str(course_obj.courseid)
              evaluations_obj=evaluations.objects.filter(course_id=course_obj,sectionid=key).values("sec_name").distinct()
              section_name=evaluations_obj[0]["sec_name"]
              tooltip.append(str(section_name))
              #res=",".join(map(str,eval_out))
              header=",".join(map(str,headers))
              tooltip_header=",".join(map(str,tooltip))
 
      try:
          header_objs=gen_headings.objects.get(section=course_obj.courseid)
          header_objs.heading=header
          header_objs.save()
      except:
          header_objs=gen_headings(section=course_obj.courseid,heading=header)  
          header_objs.save()
      #For tooltip
      try:
         header_objs=gen_headings.objects.get(section=tt)
         header_objs.heading=tooltip_header
         header_objs.save()
      except:
         header_objs=gen_headings(section=tt,heading=tooltip_header)  
         header_objs.save()
      
      return grades_policy_dict


@transaction.atomic
def get_marks_practice_problems(course_obj,evaluations_obj,quest,q_dict,not_attempt,count,grades_dict):
    updateeval=1;inserteval=0;
    #students_obj=studentDetails.objects.filter(courseid=course_obj.courseid,edxuserid__edxuserid__in=[31982,31840,33625,113312,117634,105045])  # For testing
    students_obj=studentDetails.objects.filter(courseid=course_obj.courseid)
    #students_obj=studentDetails.objects.filter(courseid=course_obj.courseid,edxuserid__edxuserid=31982)
    print grades_dict,"GRADES_DICT"
    for student in students_obj:
        eval_out=["NA"]*count
        total_marks=0
        marks_obtained=0
        marks_obj=CoursewareStudentmodule.objects.filter(student__id=student.edxuserid.edxuserid,course_id=course_obj.courseid,module_id__in=quest,grade__isnull=False)
        for marks in marks_obj:
            marks_obtained=marks.grade/marks.max_grade*q_dict[marks.module_id]
            eval_out[not_attempt[marks.module_id]]=marks_obtained
            total_marks=total_marks+marks_obtained
        #res=",".join(map(str, eval_out.values()))
        res=",".join(map(str,eval_out))
        try:
                   marks_obj=gen_markstable.objects.get(edxuserid=student.edxuserid.edxuserid,section=evaluations_obj.sectionid)
                   marks_obj.eval=res
                   marks_obj.total=total_marks
                   marks_obj.save()
                   updateeval = updateeval +1
        except Exception as e:
                   marks_obj=gen_markstable(edxuserid=student.edxuserid.edxuserid,section=evaluations_obj.sectionid,eval=res,total=total_marks)
                   marks_obj.save() 
                   inserteval=inserteval+1 
        #Creating dictionary for student grades
        '''
         '17':{
               'Graded Quiz':{'aa70ddd71a334da286ffdf248432e2aa': {'obtained_marks': 9.0,'total_marks':10.0},
                              '0db4e13e3838441ca99f2763a422f2ab': {'obtained_marks': 0.0,'total_marks':10.0}}
               'Graded Programming Assignment':
                            {'d47b9626818e41dea3ba94cc1d076d72': {'obtained_marks': 0.0,'total_marks':10.0}, 
                             '5409d445cd954c2199a7b1d74376ff79': {'obtained_marks': 0.0,'total_marks':10.0}}
               'Final Exam':{'a52581465469418bb9ae0666633b93bf': {'obtained_marks': 0.0,'total_marks':15.0}, 
                             '41dd3824d6c24123bd977d805bb4a499': {'obtained_marks': 0.0,'total_marks':15.0}}
              }
        '''
        grade_dict=grades_dict.setdefault(str(student.edxuserid.edxuserid),OrderedDict({})) 
        g_dict=grade_dict.setdefault(str(evaluations_obj.type),OrderedDict({}))
        grd_dict=g_dict.setdefault(str(evaluations_obj.sectionid),{})
        g_dict=grd_dict.setdefault("obtained_mark",total_marks)
        total_dict=grd_dict.setdefault("total_mark",float(evaluations_obj.total_marks))


@transaction.atomic
def student_grades_practice_problems(course_obj,grades_dict,evaluation_dict,grades_policy_dict):
    #print grades_policy_dict
    drop_count=0;min_count=0
    for keys,values in grades_dict.iteritems():
      #print keys # student edxuserid
      res=[];marks_list=[];total=0.0
      for key, value in values.iteritems():
        grades_list=[]
        #print key  #grade type
        for i, j in grades_policy_dict.iteritems():
             if i == key:
                min_count= int(j["min_count"])
                drop_count= int(j["drop_count"])
                weight= float(j["weight"])
                
        for k,v in value.iteritems():
          studentdetails_obj=studentDetails.objects.get(courseid=course_obj.courseid,edxuserid=keys)
          total_grade=0.0
          marks_list.append(v['obtained_mark'])
          grades_list.append(float(v['obtained_mark']/v['total_mark']))
        if len(grades_list) > min_count:
           length=len(grades_list)
           q_count=length-drop_count
        else :
           q_count=min_count-drop_count
        grades_list=sorted(grades_list,reverse=True)[:q_count]
        sum_grade=sum(grades_list)
        avg_grade=sum_grade/q_count
        grade_weight=(sum(grades_list)/q_count)*weight
        total=total+grade_weight
      res=",".join(map(str,marks_list))
      try:
           gradestable_obj=gen_gradestable.objects.get(edxuserid=studentdetails_obj.edxuserid.edxuserid,course=course_obj.courseid)
           gradestable_obj.grade=round(total*100+0.05)
           gradestable_obj.eval=res
           gradestable_obj.save() 
      except Exception as e:
           gradestable_obj=gen_gradestable(edxuserid=studentdetails_obj.edxuserid.edxuserid,course=course_obj.courseid,grade=round(total*100+0.05),eval=res)
           gradestable_obj.save()


def main(argv):
        init()
        collection=mongo_openconnection()
        curtime = datetime.now()
        #For closed courses
        #course_list=['IITBombayX/WEE210.1x/2015-16']
        course_list=["IITBombayX/CS101.1xA15/2015_T1","IITBombayX/ME209xA15/2015_T1","IITBombayX/EE210.1xA15/2015_T1","IITBombayX/BMWCS101.1x/2015_T1","IITBombayX/BMWEE210.1x/2015_T1","IITBombayX/BMWME209.x/2015_T1","IITBombayX/ET601Tx/2015-16","IITBombayX/FLFCS101x/2015_FT1","NVAforIA/PATH372.11x/2015-16","NVAforIA/PATH372.2x/2015-16","IITBombayX/WHS791x/2015-16","IITBombayX/CS101.1x/2015-16","TISS/SKANI101x/2015-16","NVAforIA/PATH372.1x/2015-16","IITBombayX/WME209x/2015-16","IITBombayX/WEE210.2x/2015-16","IITBombayX/WEE210.1x/2015-16","IITBombayX/WCS101.1x/2015-16","IITBombayX/ME209x/2015-16","IITBombayX/EE210.2x/2015-16","IITBombayX/EE210.1x/2015-16"]
        # To check for practice problem
        for course in course_list:
            print course
            course_details=course.split("/")
            longname='i4x'+"/"+course_details[0]+"/"+course_details[1]+"/"+course_details[2]
            course_id=get_course_detail(course_details[1],course_details[0],longname)
            get_student_course_enrollment(course)
            course_obj=edxcourses.objects.get(courseid=course)
            course_modules(course_obj.courseid,course_obj.org,course_obj.id)
            print_courseware(course_obj.courseid,course_obj.org,course_obj.id)

if __name__ == "__main__":
    main(sys.argv[1:])


#end main
