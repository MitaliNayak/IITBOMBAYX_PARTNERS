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

def mongo_cs_comments_service():
     global client
     client = MongoClient(mongodb)
     global db 
     db= client.cs_comments_service
     global collection
     collection = db.contents
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
                   course_end=datetime.strptime("9999-12-31 00:00:00","%Y-%m-%d %H:%M:%S")
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

           ahead_date=course_end + timedelta(days=num_days)
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
     return course_id


@transaction.atomic
def get_grade_policy_criteria(course_obj):
  collection=mongo_openconnection()
  course=course_obj.courseid.split('/')[1]
  try:
     for course_det in collection.find({"$and": [{"_id.category":"course"},{"_id.course":course_obj.course },{"_id.org":course_obj.org}]}):
        try:
           course_grading_policy= course_det["definition"]["data"]["grading_policy"]["GRADER"]
        except:
           course_grading_policy=[]
        if len(course_grading_policy) == 0 :
         for coursepolicy in course_grading_policy :
            try:
                min_count=coursepolicy["min_count"]
            except:
                min_count=0
            try:
                weight=coursepolicy["weight"]
            except:
                weight=0
            try:
                ptype=coursepolicy["type"]
            except:
                ptype="NA"
            try:
                drop_count=coursepolicy["drop_count"]
            except:
                drop_count=0
            try:
                short_label=coursepolicy["short_label"]
            except:
                short_label="NA"
            grade_policy_obj=gradepolicy(courseid=course_obj, min_count=min_count, weight=weight ,type=ptype, drop_count=drop_count, short_label=short_label)
            grade_policy_obj.save()
        try:
                cutoffs=course_det["definition"]["data"]["grading_policy"]["GRADE_CUTOFFS"]
        except:
                cutoffs={}
        if cutoffs != {} :
              for key,value in cutoffs.iteritems():
                grade_criteria_obj=gradescriteria(courseid=course_obj,grade=key,cutoffs=value)
                grade_criteria_obj.save()
     return 0
  except Exception as e:
      print "Error %s - Fetching grade criteria and Policy from mongodb for course %s "%(e.message,course_obj.courseid)
      return -1





@transaction.atomic    
def insert_modlist(disnm,motype,moid,rel_id,sort1,visible_to_staff_only,graded,long_name,weight1, count,release_date,due_date,cid,gradetype, discussion_id):
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
       mod_obj.discussion_id=discussion_id
       mod_obj.save()
       return mod_obj.id
    except Exception as e:
       coursemod = course_modlist(display_name=disnm,module_type=motype,module_id=moid, related_id=rel_id,order=sort1, visible_to_staff_only=visible_to_staff_only, graded=graded, long_name=long_name, maxmarks=weight1, questions=count, startdate=release_date, duedate=due_date,hasproblems=0,course=cid,gradetype=gradetype,discussion_id=discussion_id)
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
       for moddetails in collection.find({"_id.course":csr,"_id.org":org,"_id.category":mtype,"_id.name":mid},{"metadata.display_name":1,"definition.children":1,"_id.name":1, "metadata.graded":1,"metadata.visible_to_staff_only":1,"metadata.format":1,"metadata.start":1,"metadata.due":1,"definition.data.data":1,"metadata.weight":1,"metadata.discussion_id":1}):
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
            if mtype == 'discussion':
               discussion_id = moddetails["metadata"]["discussion_id"]
            else:
               discussion_id = None
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
            
            #insert_id=insert_modlist(dname,mtype,mod_details["_id"]["name"],csr_id,sortby,visible_to_staff_only,graded,mod)
            insert_id=insert_modlist(dname,mtype,moddetails["_id"]["name"],csr_id,sortorder,visible_to_staff_only,graded,mod,weight, count,release_date,due_date,cid,gradetype,discussion_id) 
            try:
               clist=moddetails["definition"]["children"]
            except:
               clist=[]
            if len(clist) !=0:
                result=open_module(csr,org,insert_id,clist,sortorder,start,end,cid)
                
                sortorder=result['sortorder'] 
                # Update Verticals and  Sequentials that have graded problems with maxmarks and number of questions
                # update verticals with number of  
  dict['graded']=graded
  dict['questions']=totalques
  dict['maxmarks']=totalmarks
  dict['sortorder']=sortorder
  dict['has_problem']=has_problem
  return dict        

@transaction.atomic
def course_modules(course_id,org,cid):
    collection=mongo_openconnection()
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
         csr_id=insert_modlist((csr_name["metadata"]["display_name"].encode('utf-8')),"course",course_id,"0",sortby,0,0,course_id,0,0,course_start,course_end,cid,"","")
         if len(csr_name["definition"]["children"]) !=0:
                result=open_module(csr,org,csr_id,csr_name["definition"]["children"],sortby,course_start,course_end,cid,)


@transaction.atomic
def print_courseware(csr,org,cid):
    sequences_dict=collections.OrderedDict()
    discussions_dict=collections.OrderedDict()
    try:
       course_obj=edxcourses.objects.get(id=cid)
    except:
       return -1
    curtime = datetime.now() 
    modlist=course_modlist.objects.get(module_id = str(csr),course=cid,visible_to_staff_only=0)
    chlist=course_modlist.objects.filter(related_id= modlist.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id')
         
    for chap in chlist:
       seqlist=course_modlist.objects.filter(related_id= chap.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id') 
       for seq in seqlist:
           vertlist=course_modlist.objects.filter(related_id=seq.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime).order_by('order','related_id')
           for vert in vertlist:
            discussion_list=course_modlist.objects.filter(related_id=vert.id,course=cid,visible_to_staff_only=0,startdate__lte=curtime,module_type='discussion').order_by('order','related_id')
            for discussion in discussion_list:
                #Creating dictionary for discussion.
                '''
                      '45bb1c9c751945a18a62df9479604248':                         
                      {
                        'seq_name': 'Lecture 1: Introductory Topics', 
                        'details'  : [{'id':'4faa607b5a354baa8734acee94765d8f','name': 'Introduction'},         
                                      {'id':'4a617a31b7c644db9c8f2695af128c54','name':'Thermodynamic Systems'},  
                                      {'id':'36e87eb0a56a4211a18e60b944e7443c','name':'Properties and State'}]}
                '''
                if discussion.display_name.encode('utf-8') == "":
                   if vert.display_name.encode('utf-8') == "":
                       display_name=seq.display_name.encode('utf-8')
                   else:
                       display_name=vert.display_name.encode('utf-8') 
                else:
                      display_name=discussion.display_name.encode('utf-8') 
                sequence_dict=sequences_dict.setdefault(str(seq.module_id),{})
                sequence_dict.setdefault("seq_name",seq.display_name.encode('utf-8'))
                dis_detail_list=sequence_dict.setdefault("details",[])
                discussions_dict.setdefault("id",discussion.discussion_id)
                discussions_dict.setdefault("name",display_name)
                dis_detail_list.append(discussions_dict)
                discussions_dict={}                
            
    discussion_dashboard(sequences_dict,course_obj.courseid)   

#############################################Discussion Dashboard ############################################
def discussion_dashboard(sequences_dict,courseid):
      collection=mongo_cs_comments_service()
      #sequence_dict
      '''
                '45bb1c9c751945a18a62df9479604248':                         
                      {
                        'seq_name': 'Lecture 1: Introductory Topics', 
                        'details'  : [{'id':'4faa607b5a354baa8734acee94765d8f','name': 'Introduction'}, {'id':'4a617a31b7c644db9c8f2695af128c54','name':'Thermodynamic Systems'}, {'id':'36e87eb0a56a4211a18e60b944e7443c','name':'Properties and State'}]}
      '''
      discussion_ids=[]
      curtime = datetime.now()
      course_id=edxcourses.objects.get(courseid=courseid).id
      discussion_dict={}
      curtime = datetime.now()
      discussion_dict["discussion_count"]=0;discussion_dict["open_question_count"]=0;discussion_dict["closed_question_count"]=0
      for seq_keys,seq_values in sequences_dict.iteritems():
           sequence_name=seq_values["seq_name"]
           for discussions in seq_values["details"]:
              discussion_name=discussions["name"]
              for ids,names in discussions.iteritems():
                  comments_ids=[]
                  if( ids == 'id') :
                    for keys,values in collection.aggregate( [ {"$match": {"commentable_id":names, "course_id":str(courseid)} }, {"$group": {"_id":{"closed":"$closed","_type":"$_type","thread_type":"$thread_type"},"thread_type_count":{"$sum":1},"data":{"$push":{"comment_id":"$_id"}} } } ]).iteritems():
                      if keys == "result":
                         for value in values:
                           try: 
                            if value["_id"]["thread_type"] == "discussion":
                                discussion_count=value["thread_type_count"]
                                discussion_dict["discussion_count"]=discussion_count
                            elif value["_id"]["thread_type"] == "question" and value["_id"]["closed"] == False:
                                open_question_count=value["thread_type_count"]
                                discussion_dict["open_question_count"]=open_question_count
                            elif value["_id"]["thread_type"] == "question" and value["_id"]["closed"] == True:
                                closed_question_count=value["thread_type_count"]
                                discussion_dict["closed_question_count"]=closed_question_count
                           except KeyError as e:
                                continue
                           for comment in value["data"]:
                                comments_ids.append(comment["comment_id"])
                    discussion_id=names
                  if comments_ids != []:
                
                    try:   
                     gen_repout_obj=gen_repout.objects.get(reportid=3,num_cols=4,A=courseid,B=sequence_name,C=discussion_name, D=discussion_id,E =comments_ids,F=discussion_dict["discussion_count"],G=discussion_dict["open_question_count"],H=discussion_dict["closed_question_count"])       
                    except:
                     gen_repout_obj=gen_repout(reportid=3,num_cols=4,A=courseid,B=sequence_name,C=discussion_name, D=discussion_id,E =comments_ids,F=discussion_dict["discussion_count"],G=discussion_dict["open_question_count"],H=discussion_dict["closed_question_count"])
                     gen_repout_obj.save()
                      
      return 0
        
#############################################Discussion Dashboard ############################################
def main(argv):
        init()
        collection=mongo_openconnection()
        curtime = datetime.now()
        course_id=""
        for course in collection.find({"_id.category":"course"},{"_id.course":1,"_id.org":1,"_id.tag":1,"_id.name":1}):
         longname=course["_id"]["tag"]+"/"+course["_id"]["org"]+"/"+course["_id"]["course"]+"/"+course["_id"]["name"]
         course_id=get_course_detail(course["_id"]["course"],course["_id"]["org"],longname)
         print course_id
         course_obj=edxcourses.objects.get(courseid=course_id)
         try:
                ahead_date=course_obj.courseend + timedelta(days=num_days)
         except:
                ahead_date="9999-12-31 24:00:00"
         try:
                coursestart=str(course_obj.coursestart)
         except:
                coursestart="1111-01-01 24:00:00"
         try:
                enrollend=str(course_obj.enrollend)
         except:
                enrollend="9999-12-31 24:00:00" 
         #if (coursestart < str(curtime)) and (str(curtime) < str(ahead_date)):
         course_modules(course_obj.courseid,course_obj.org,course_obj.id)
         print_courseware(course_obj.courseid,course_obj.org,course_obj.id)


if __name__ == "__main__":
    main(sys.argv[1:])


#end main
