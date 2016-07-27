from django.contrib.sessions.models import Session
from tracking.models import Visitor
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from SIP.views import *
#import pytz 
from pytz import timezone
class Concurrentloginrestrict(object):
      def process_request(self,request):
        if request.user.is_authenticated():
          userip=request.META.get('REMOTE_ADDR','')
          try:
              lastlogin=request.user.last_login
          except:
                lastlogin=datetime(4712,12,31,0,0).replace(tzinfo=timezone('UTC'))
          print (datetime.now(timezone('UTC'))-lastlogin).total_seconds(),datetime.now(timezone('UTC')),"hello",lastlogin
          if 0<=(datetime.now(timezone('UTC'))-lastlogin).total_seconds()<5:#unicode(lastlogin)[:19]==unicode(timezone.now())[:19]:
              oldvisitorobj=Visitor.objects.filter(user=request.user).exclude(ip_address=userip)
              for i in oldvisitorobj:
                  Session.objects.filter(session_key=i.session_key).delete()
                  i.user=None
                  i.save()
                  
                  
          

