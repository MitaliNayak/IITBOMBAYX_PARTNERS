import pymongo
import MySQLdb
import argparse,re,datetime
import sys, getopt,os
import django
import time
from django.db import transaction
from datetime import date, timedelta,datetime
from collections import *
import collections
import dateutil.parser
from django.utils import timezone
#Please add the full project folder pwd
#project_dir="bmwinfo/IITBOMBAYX_PARTNERS"
project_dir=os.path.dirname(os.path.realpath(__file__))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE']='IITBOMBAYX_PARTNERS.settings'
django.setup()
num_days=4

from pymongo import MongoClient
from django.db import models,transaction
from django.core.mail.message import EmailMultiAlternatives
from SIP.models import *
from iitbx.models import *
from managerapp.models import *

mysql_host="localhost"
#please enter mysq username password
user="iitbxblended"
passwd="11tbx@123"
mysql_schema="edxapp"
mongodb='mongodb://localhost:27017/'
courses=["i4x/IITBombayX/CS101.1xA15/2015_T1","i4x/IITBombayX/ME209xA15/2015_T1","i4x/IITBombayX/EE210.1xA15/2015_T1","i4x/IITBombayX/CS101.1xS16/2016_T1","i4x/IITBombayX/EE210xS16/2016_T1","i4x/IITBombayX/ME209xS16/2016_T1","i4x/IITBombayX/HS791xS16/2016_T1","i4x/IITBombayX/SKANI101xA/2016_T2","i4x/IITBombayX/HS791xA16/2016-17","i4x/IITBombayX/EE210xA16/2016-17","i4x/IITBombayX/ME209xA16/2016-2017"]
